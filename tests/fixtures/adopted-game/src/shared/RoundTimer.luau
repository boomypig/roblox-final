-- RoundTimer: counts a round down. Pure: no Instances, no services.
local RoundTimer = {}

function RoundTimer.tick(left: number, dt: number): number
	return math.max(left - dt, 0)
end

return RoundTimer
