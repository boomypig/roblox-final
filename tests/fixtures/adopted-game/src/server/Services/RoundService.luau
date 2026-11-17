-- RoundService: owns the round state (waiting, running, ended) and the time left.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage.Shared.Config)
local RoundTimer = require(ReplicatedStorage.Shared.RoundTimer)

local RoundService = {}

function RoundService:Init()
	local remotes = ReplicatedStorage:FindFirstChild("Remotes")
	if not remotes then
		remotes = Instance.new("Folder")
		remotes.Name = "Remotes"
		remotes.Parent = ReplicatedStorage
	end
	self.roundState = Instance.new("RemoteEvent")
	self.roundState.Name = "RoundState"
	self.roundState.Parent = remotes
end

function RoundService:Start()
	task.spawn(function()
		while true do
			if #Players:GetPlayers() >= Config.MinPlayers then
				local left = Config.RoundSeconds
				while left > 0 do
					self.roundState:FireAllClients("running", left)
					task.wait(1)
					left = RoundTimer.tick(left, 1)
				end
				self.roundState:FireAllClients("ended", 0)
			end
			task.wait(Config.IntermissionSeconds)
		end
	end)
end

return RoundService
