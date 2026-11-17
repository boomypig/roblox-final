-- CoinService: owns each player's coin count for the round.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage.Shared.Config)
local Scoring = require(ReplicatedStorage.Shared.Scoring)

local CoinService = {}
CoinService.coins = {}

function CoinService:Init()
	local remotes = ReplicatedStorage:FindFirstChild("Remotes")
	if not remotes then
		remotes = Instance.new("Folder")
		remotes.Name = "Remotes"
		remotes.Parent = ReplicatedStorage
	end
	self.collect = Instance.new("RemoteEvent")
	self.collect.Name = "CollectCoin"
	self.collect.Parent = remotes
end

function CoinService:Start()
	self.collect.OnServerEvent:Connect(function(player: Player, coinId: unknown)
		if type(coinId) ~= "string" or #coinId > 32 then
			return
		end
		local have = self.coins[player] or 0
		self.coins[player] = Scoring.add(have, Config.CoinValue, Config.MaxCoins)
	end)
end

return CoinService
