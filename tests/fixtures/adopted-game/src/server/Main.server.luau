-- Harbor Rush server entry. Requires every service, then calls Init on all, then Start on all.
local Services = script.Parent.Services

local services = {
	require(Services.RoundService),
	require(Services.CoinService),
}

for _, service in services do
	service:Init()
end
for _, service in services do
	service:Start()
end

print("[HarborRush] server started")
