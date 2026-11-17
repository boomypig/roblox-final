# Map state: <name>

The map-builder reads this file first and updates it last, every run. It is the memory between
runs: what is in Studio, how it was checked, and where a cut-off run stopped. Copy it to
`docs/design/maps/<name>.state.md` (the starter does this); the brief is `<name>.md` beside it.

Updated: <date and time of the last update>

## Folders and counts

From the last `map_checks.lua` inventory, pasted as printed. Replace it after every run; it is
what a run reads instead of touring the place.

```
<inventory lines>
```

## Check parameters

The block `map_checks.lua` runs with, between its `PARAMS BEGIN` and `PARAMS END` lines. Every
number comes from the map brief ("Gameplay geometry"); a value the brief leaves open is decided
once here and logged in "Pass log" as a judgment call.

```lua
local PARAMS = {
	map = nil, -- Workspace.<map>; nil = the Workspace child that has a Layout folder
	checks = { inventory = true, properties = true, lanes = true, refuge = false, hiding = false },
	surfaceAttribute = "Surface", -- every walkable Layout part carries this string attribute
	collideAttribute = "Collides", -- set true on a Dressing part players are meant to stand on
	walkableNormalY = 0.7, -- a face this close to straight up counts as floor
	minWalkableFace = 2, -- studs: a face narrower than this is a wall top, not floor
	grid = 4, -- studs between floor samples
	maxSamples = 4000, -- the grid widens to stay under this
	lane = { minWidth = 6, height = 3 }, -- studs; measured this high above the floor
	refuge = { tag = "HidingSpot", maxDistance = 30 }, -- studs from any floor sample
	hiding = { tag = "HidingSpot", minWidth = 3, minDepth = 3, minHeight = 5.5, reach = 20 },
	failLines = 30,
}
```

## Pass log

Newest last. One entry per finished run.

| Date | Zone | Pass | Built (paths) | Checks (RESULT, failures) | Judgment calls | Left for the user |
|---|---|---|---|---|---|---|

## Run in progress

Empty when no run is in progress. A run appends one line here after each structure, so a run
that is cut off can be resumed from the last line instead of rebuilt.

- (none)
