--!nonstrict
-- roblox-map: map_checks.lua - the map-builder's numbers after each structure it builds.
--
-- WHY THIS EXISTS. The map-builder judged a pass from screenshots and prose checklists.
-- What a screenshot cannot show is exactly what playtests kept finding: decoration that
-- players walk into, default grey Plastic left in a corner, a hiding spot an avatar does
-- not fit in, a lane narrower than a player, a stretch of floor with no refuge in reach.
-- prove.py answers those questions for a headless layout; this answers them for what
-- actually stands in Studio, in one execute_luau call, as numbers the agent reports.
--
-- HOW TO RUN. Paste this file into execute_luau (Edit datamodel) with the block between the
-- two PARAMS marker lines below replaced by the "Check parameters" block of the map's state
-- file (docs/design/maps/<name>.state.md). `scripts/map_checks.py --state <file>` does that
-- substitution for anyone with a shell. Every number in PARAMS comes from the map brief.
--
-- IT NEVER YIELDS. execute_luau drops all output of a script that yields
-- (roblox-code references/traps.md), so the floor grid widens to stay under maxSamples
-- instead of waiting between chunks.
--
-- OUTPUT. One summary line per check with its numbers, then one line per failure, capped
-- at PARAMS.failLines (30), then RESULT. The default-grey rule (Color 163,162,165 on a part
-- with Transparency < 1) is the one verify_build.lua uses; tests keep the two equal.

-- PARAMS BEGIN
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
-- PARAMS END

local CollectionService = game:GetService("CollectionService")
local DEFAULT_GREY = Color3.fromRGB(163, 162, 165)
local DEFAULT_NAMES = { Part = true, MeshPart = true, WedgePart = true, CornerWedgePart = true,
	TrussPart = true, UnionOperation = true, Union = true, Model = true }

local summary, failLines, failures = {}, {}, 0
local function fail(s)
	failures += 1
	if #failLines < (PARAMS.failLines or 30) then
		table.insert(failLines, "FAIL " .. s)
	end
end
local function say(s)
	table.insert(summary, s)
end
local function r1(n)
	return math.floor(n * 10 + 0.5) / 10
end
local function at(v)
	return `({r1(v.X)}, {r1(v.Y)}, {r1(v.Z)})`
end

local function findMap()
	if PARAMS.map then
		return workspace:FindFirstChild(PARAMS.map)
	end
	local best, bestN = nil, -1
	for _, c in ipairs(workspace:GetChildren()) do
		if c:FindFirstChild("Layout") then
			local n = #c:GetDescendants()
			if n > bestN then
				best, bestN = c, n
			end
		end
	end
	return best
end

local root = findMap()
if not root then
	return "FAIL no map: no Workspace child has a Layout folder (set PARAMS.map)\nRESULT: FAIL (1 failures)"
end
local layout = root:FindFirstChild("Layout")
local dressing = root:FindFirstChild("Dressing")
if not layout then
	return `FAIL {root:GetFullName()} has no Layout folder\nRESULT: FAIL (1 failures)`
end

local function visible(p)
	return p.Transparency < 1
end

-- The world-space half extents of a part's box.
local function halfExtents(p)
	local cf, s = p.CFrame, p.Size / 2
	local rx, ux, lx = cf.RightVector, cf.UpVector, cf.LookVector
	return Vector3.new(
		math.abs(rx.X) * s.X + math.abs(ux.X) * s.Y + math.abs(lx.X) * s.Z,
		math.abs(rx.Y) * s.X + math.abs(ux.Y) * s.Y + math.abs(lx.Y) * s.Z,
		math.abs(rx.Z) * s.X + math.abs(ux.Z) * s.Y + math.abs(lx.Z) * s.Z
	)
end

-- Floor: collidable, visible, and one face points up with room to stand on.
local function walkable(p)
	if not (p:IsA("BasePart") and p.CanCollide and visible(p)) then
		return false
	end
	local cf, s = p.CFrame, p.Size
	local axes = {
		{ math.abs(cf.RightVector.Y), s.Y, s.Z },
		{ math.abs(cf.UpVector.Y), s.X, s.Z },
		{ math.abs(cf.LookVector.Y), s.X, s.Y },
	}
	for _, a in ipairs(axes) do
		if a[1] >= PARAMS.walkableNormalY and a[2] >= PARAMS.minWalkableFace and a[3] >= PARAMS.minWalkableFace then
			return true
		end
	end
	return false
end

local function parts(folder)
	local out = {}
	if folder then
		for _, d in ipairs(folder:GetDescendants()) do
			if d:IsA("BasePart") then
				table.insert(out, d)
			end
		end
	end
	return out
end
local layoutParts, dressingParts = parts(layout), parts(dressing)

-------------------------------------------------------------------- inventory
if PARAMS.checks.inventory then
	local function count(folder)
		if not folder then
			return "missing"
		end
		local nParts, nModels, nOther = 0, 0, 0
		for _, d in ipairs(folder:GetDescendants()) do
			if d:IsA("BasePart") then
				nParts += 1
			elseif d:IsA("Model") then
				nModels += 1
			else
				nOther += 1
			end
		end
		return `{nParts} parts, {nModels} models, {nOther} other`
	end
	local others = {}
	for _, c in ipairs(root:GetChildren()) do
		if c ~= layout and c ~= dressing then
			table.insert(others, c.Name)
		end
	end
	say(`inventory {root:GetFullName()}: Layout {count(layout)}; Dressing {count(dressing)}; other children: {#others > 0 and table.concat(others, ", ") or "none"}`)

	local tags, names = {}, {}
	for _, d in ipairs(root:GetDescendants()) do
		for _, tag in ipairs(d:GetTags()) do
			tags[tag] = (tags[tag] or 0) + 1
		end
	end
	for _, c in ipairs(layout:GetChildren()) do
		names[c.Name] = (names[c.Name] or 0) + 1
	end
	local function listed(t)
		local keys = {}
		for k in pairs(t) do
			table.insert(keys, k)
		end
		table.sort(keys)
		local out = {}
		for _, k in ipairs(keys) do
			table.insert(out, `{k}={t[k]}`)
		end
		return #out > 0 and table.concat(out, ", ") or "none"
	end
	say("inventory tags: " .. listed(tags))
	say("inventory Layout children: " .. listed(names))
end

-------------------------------------------------------------------- properties
if PARAMS.checks.properties then
	local n = { plastic = 0, grey = 0, unanchored = 0, unnamed = 0, colliding = 0, noSurface = 0 }
	local function sweep(p, isDressing)
		local name = p:GetFullName()
		if visible(p) and p.Material == Enum.Material.Plastic then
			n.plastic += 1
			fail(`{name} is Plastic`)
		end
		if visible(p) and p.Color == DEFAULT_GREY then
			n.grey += 1
			fail(`{name} is default grey (163, 162, 165)`)
		end
		if not p.Anchored then
			n.unanchored += 1
			fail(`{name} is not Anchored`)
		end
		if DEFAULT_NAMES[p.Name] then
			n.unnamed += 1
			fail(`{name} still has its default name`)
		end
		if isDressing and p:GetAttribute(PARAMS.collideAttribute) ~= true
			and (p.CanCollide or p.CanTouch or p.CanQuery) then
			n.colliding += 1
			fail(`{name} is decoration with CanCollide/CanTouch/CanQuery on (set {PARAMS.collideAttribute}=true if players stand on it)`)
		end
		if not isDressing and walkable(p) then
			local s = p:GetAttribute(PARAMS.surfaceAttribute)
			if type(s) ~= "string" or s == "" then
				n.noSurface += 1
				fail(`{name} is walkable but has no {PARAMS.surfaceAttribute} attribute`)
			end
		end
	end
	for _, p in ipairs(layoutParts) do
		sweep(p, false)
	end
	for _, p in ipairs(dressingParts) do
		sweep(p, true)
	end
	say(`properties: {#layoutParts + #dressingParts} parts; Plastic {n.plastic}, default grey {n.grey}, unanchored {n.unanchored}, default names {n.unnamed}, colliding decoration {n.colliding}, walkable without {PARAMS.surfaceAttribute} {n.noSurface}`)
end

-------------------------------------------------------------------- floor grid
local samples = {}
if PARAMS.checks.lanes or PARAMS.checks.refuge then
	local lo, hi = Vector3.new(math.huge, math.huge, math.huge), Vector3.new(-math.huge, -math.huge, -math.huge)
	for _, p in ipairs(layoutParts) do
		local h = halfExtents(p)
		lo = lo:Min(p.Position - h)
		hi = hi:Max(p.Position + h)
	end
	if #layoutParts > 0 then
		local step = PARAMS.grid
		while ((hi.X - lo.X) / step + 1) * ((hi.Z - lo.Z) / step + 1) > PARAMS.maxSamples do
			step *= 1.5
		end
		local down = RaycastParams.new()
		down.FilterType = Enum.RaycastFilterType.Include
		down.FilterDescendantsInstances = { layout }
		down.RespectCanCollide = true
		local x = lo.X + step / 2
		while x < hi.X do
			local z = lo.Z + step / 2
			while z < hi.Z do
				local hit = workspace:Raycast(Vector3.new(x, hi.Y + 5, z), Vector3.new(0, -(hi.Y - lo.Y + 10), 0), down)
				if hit and hit.Normal.Y >= PARAMS.walkableNormalY then
					table.insert(samples, hit.Position)
				end
				z += step
			end
			x += step
		end
		say(`floor grid: {#samples} samples every {r1(step)} studs over {r1(hi.X - lo.X)} x {r1(hi.Z - lo.Z)} studs`)
	else
		fail("Layout has no parts, so there is no floor to sample")
	end
end

-------------------------------------------------------------------- lanes
if PARAMS.checks.lanes and #samples > 0 then
	local w = PARAMS.lane.minWidth
	local rp = RaycastParams.new()
	rp.FilterType = Enum.RaycastFilterType.Include
	rp.FilterDescendantsInstances = { root }
	rp.RespectCanCollide = true
	local function reach(origin, dir)
		local hit = workspace:Raycast(origin, dir * w, rp)
		return hit and hit.Distance or w
	end
	local narrow, narrowest = 0, math.huge
	for _, s in ipairs(samples) do
		local o = s + Vector3.new(0, PARAMS.lane.height, 0)
		local wx = reach(o, Vector3.xAxis) + reach(o, -Vector3.xAxis)
		local wz = reach(o, Vector3.zAxis) + reach(o, -Vector3.zAxis)
		local width = math.min(wx, wz)
		narrowest = math.min(narrowest, width)
		if width < w then
			narrow += 1
			fail(`lane {r1(width)} studs wide at {at(s)} (needs {w})`)
		end
	end
	say(`lanes: {narrow} of {#samples} samples narrower than {w} studs; narrowest {narrowest == math.huge and "n/a" or r1(narrowest)}`)
end

-------------------------------------------------------------------- refuge distance
if PARAMS.checks.refuge and #samples > 0 then
	local spots = {}
	for _, inst in ipairs(CollectionService:GetTagged(PARAMS.refuge.tag)) do
		if inst:IsDescendantOf(root) then
			if inst:IsA("Model") then
				table.insert(spots, inst:GetPivot().Position)
			elseif inst:IsA("BasePart") then
				table.insert(spots, inst.Position)
			end
		end
	end
	if #spots == 0 then
		fail(`no refuge: nothing in the map is tagged {PARAMS.refuge.tag}`)
		say(`refuge: 0 spots tagged {PARAMS.refuge.tag}`)
	else
		local far, worst, worstAt = 0, 0, nil
		for _, s in ipairs(samples) do
			local best = math.huge
			for _, r in ipairs(spots) do
				local d = Vector3.new(s.X - r.X, 0, s.Z - r.Z).Magnitude
				if d < best then
					best = d
				end
			end
			if best > worst then
				worst, worstAt = best, s
			end
			if best > PARAMS.refuge.maxDistance then
				far += 1
				fail(`floor at {at(s)} is {r1(best)} studs from the nearest {PARAMS.refuge.tag} (max {PARAMS.refuge.maxDistance})`)
			end
		end
		say(`refuge: {#spots} spots; {far} of {#samples} samples farther than {PARAMS.refuge.maxDistance} studs; worst {r1(worst)} at {worstAt and at(worstAt) or "n/a"}`)
	end
end

-------------------------------------------------------------------- hiding-spot sizes
if PARAMS.checks.hiding then
	local h = PARAMS.hiding
	local rp = RaycastParams.new()
	rp.FilterType = Enum.RaycastFilterType.Include
	rp.FilterDescendantsInstances = { root }
	rp.RespectCanCollide = true
	local checked, small = 0, 0
	for _, inst in ipairs(CollectionService:GetTagged(h.tag)) do
		if inst:IsDescendantOf(root) and (inst:IsA("Model") or inst:IsA("BasePart")) then
			checked += 1
			local cf = if inst:IsA("Model") then inst:GetPivot() else inst.CFrame
			local inside = inst:GetAttribute("Inside")
			local o = if typeof(inside) == "Vector3" then inside else cf.Position
			local function reach(dir)
				local hit = workspace:Raycast(o, dir * h.reach, rp)
				return hit and hit.Distance or h.reach
			end
			local width = reach(cf.RightVector) + reach(-cf.RightVector)
			local depth = reach(cf.LookVector) + reach(-cf.LookVector)
			local height = reach(Vector3.yAxis) + reach(-Vector3.yAxis)
			if width < h.minWidth or depth < h.minDepth or height < h.minHeight then
				small += 1
				fail(`{inst:GetFullName()} hiding space is {r1(width)} x {r1(depth)} x {r1(height)} studs (needs {h.minWidth} x {h.minDepth} x {h.minHeight}; set an Inside attribute if the pivot is not inside it)`)
			end
		end
	end
	if checked == 0 then
		fail(`no hiding spot: nothing in the map is tagged {h.tag}`)
	end
	say(`hiding: {checked} spots tagged {h.tag}; {small} too small for {h.minWidth} x {h.minDepth} x {h.minHeight} studs`)
end

-------------------------------------------------------------------- report
local out = { `map_checks {root:GetFullName()}` }
for _, s in ipairs(summary) do
	table.insert(out, s)
end
for _, s in ipairs(failLines) do
	table.insert(out, s)
end
if failures > #failLines then
	table.insert(out, `... and {failures - #failLines} more failures`)
end
table.insert(out, `RESULT: {failures == 0 and "PASS" or "FAIL"} ({failures} failures)`)
return table.concat(out, "\n")
