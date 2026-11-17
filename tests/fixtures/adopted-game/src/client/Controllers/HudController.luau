-- HudController: shows the round state and time left.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local HudController = {}

function HudController:Init()
	self.remotes = ReplicatedStorage:WaitForChild("Remotes", 10)
end

function HudController:Start()
	if not self.remotes then
		return
	end
	local roundState = self.remotes:WaitForChild("RoundState", 10)
	if not roundState then
		return
	end
	roundState.OnClientEvent:Connect(function(state: string, left: number)
		print(`[Hud] {state} {left}`)
	end)
end

return HudController
