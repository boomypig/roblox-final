-- Scoring: coin arithmetic. Pure: no Instances, no services.
local Scoring = {}

function Scoring.add(have: number, amount: number, max: number): number
	if amount <= 0 then
		return have
	end
	return math.min(have + amount, max)
end

return Scoring
