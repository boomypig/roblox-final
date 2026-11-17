"""HTTP client for unofficial endpoints: timeouts, retries with backoff, polite pacing, optional cache."""

from __future__ import annotations

import hashlib
import json
import logging
import random
import time
from pathlib import Path
from typing import Any

import requests

from . import config

log = logging.getLogger(__name__)

RETRY_STATUSES = {429, 500, 502, 503, 504}


class FetchError(Exception):
    """A request failed for good: retries exhausted, a non-retryable status, or a non-JSON body."""


class Client:
    def __init__(
        self,
        delay: float = config.POLITE_DELAY_SECONDS,
        timeout: float = config.TIMEOUT_SECONDS,
        max_retries: int = config.MAX_RETRIES,
        cache_dir: Path | None = None,
        session: requests.Session | None = None,
        sleep=time.sleep,
    ) -> None:
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.cache_dir = cache_dir
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": config.USER_AGENT, "Accept": "application/json"})
        self.requests_made = 0
        self._sleep = sleep
        self._last_request_at = 0.0

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        cache_path = self._cache_path(url, params)
        if cache_path is not None and cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))
        payload = self._get_with_retries(url, params)
        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def _get_with_retries(self, url: str, params: dict[str, Any] | None) -> Any:
        last_error = "no attempt made"
        for attempt in range(self.max_retries + 1):
            self._wait_politely()
            wait: float | None = None
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
                self.requests_made += 1
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if resp.status_code == 200:
                    try:
                        return resp.json()
                    except ValueError as exc:
                        raise FetchError(f"{url}: body is not JSON ({exc})") from exc
                if resp.status_code not in RETRY_STATUSES:
                    raise FetchError(f"{url}: HTTP {resp.status_code}: {resp.text[:200]}")
                last_error = f"HTTP {resp.status_code}"
                wait = _retry_after_seconds(resp)
            if attempt == self.max_retries:
                break
            if wait is None:
                wait = config.BACKOFF_BASE_SECONDS * (2**attempt) + random.uniform(0, 1)
            log.warning("%s failed (%s); retry %d/%d in %.1fs", url, last_error, attempt + 1, self.max_retries, wait)
            self._sleep(wait)
        raise FetchError(f"{url}: gave up after {self.max_retries + 1} attempts ({last_error})")

    def _wait_politely(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.delay:
            self._sleep(self.delay - elapsed)
        self._last_request_at = time.monotonic()

    def _cache_path(self, url: str, params: dict[str, Any] | None) -> Path | None:
        if self.cache_dir is None:
            return None
        # sessionId is random per run; leaving it in would make every key unique.
        stable = {k: v for k, v in (params or {}).items() if k != "sessionId"}
        key = hashlib.sha1(f"{url}?{json.dumps(stable, sort_keys=True)}".encode()).hexdigest()
        return self.cache_dir / f"{key}.json"


def _retry_after_seconds(resp: requests.Response) -> float | None:
    value = resp.headers.get("Retry-After")
    if value is None:
        return None
    try:
        return min(float(value), config.MAX_RETRY_AFTER_SECONDS)
    except ValueError:
        return None
