-- Harbor Rush client entry. Same shape as the server: Init on all, then Start on all.
local Controllers = script.Parent.Controllers

local controllers = {
	require(Controllers.HudController),
}

for _, controller in controllers do
	controller:Init()
end
for _, controller in controllers do
	controller:Start()
end
