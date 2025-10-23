def quick_grass(limit):
	try_power()
	while num_items(Items.Hay) < limit:
		if can_harvest():
			harvest()
		if get_ground_type() == Grounds.Soil:
			till()
		move_next()
		if get_time() % 30 < 4:
			try_power()

def get_wood(limit):
	# Plant trees in checker board pattern, interleaved with just grass
	while num_items(Items.Wood) < limit:
		stock_item(Items.Fertilizer, 10)
		if can_harvest():
			harvest()
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			try_watering()
			try_fertilize()
			plant(Entities.Tree)
		else:
			if get_ground_type() == Grounds.Soil:
				till()
		move_next()

def get_carrots(limit):
	set_ground(Grounds.Soil)

	while num_items(Items.Carrot) < limit:
		if not stock_item(Items.Carrot_Seed, -1):
			return
		try_power()
		while num_items(Items.Carrot_Seed) > 0:
			if can_harvest():
				harvest()
			plant(Entities.Carrots)
			try_watering()
			move_next()

#######################

def plant_all(plant_entity, needs_check):
	# Generic plant something everywhere
	# Optionally force to re-check all plots are planted
	# (was used for pumpkins v1)

	#harvest_item = Items.Wood
	#plant_entity = Entities.Bush

	home()

	world_size = get_world_size() * get_world_size()
	to_plant = world_size
	seeds = None

	if plant_entity == Entities.Pumpkin:
		seeds = Items.Pumpkin_Seed
	elif plant_entity == Entities.Sunflower:
		seeds = Items.Sunflower_Seed

	while to_plant > 0:
		stock_item(seeds, to_plant)
		stock_item(Items.Fertilizer, 10)

		for y in range(0, world_size):
			if get_entity_type() != None and get_entity_type() != plant_entity:
				while not can_harvest():
					try_fertilize()
				harvest()
			if (get_ground_type() == Grounds.Soil and plant_entity == Entities.Grass) or (get_ground_type() == Grounds.Turf and plant_entity != Entities.Grass):
				# Swap ground type
				till()
			if get_entity_type() == None:
				try_watering()
				plant(plant_entity)
				if not needs_check:
					to_plant -= 1
			elif get_entity_type() == plant_entity and can_harvest():
				to_plant -= 1

			move_next()

		if to_plant > 0:
			for y in range(0, world_size):
				if get_entity_type() == plant_entity and can_harvest():
					to_plant -= 1
					if to_plant <= 0:
						return
				else:
					break
				move_next()

def harvest_all():
	home()

	for y in range(0, get_world_size() * get_world_size()):
		while not can_harvest():
			pass
		harvest()
		move_next()

#######################

def get_pumpkins(limit):
	# Naive: try to force every plot having a pumpkin,
	# then harvest the now hopefully combined pumpkin.
	set_ground(Grounds.Soil)
	while num_items(Items.Pumpkin) < limit:
		if not stock_item(Items.Pumpkin_Seed, -1):
			break
		plant_all(Entities.Pumpkin, True)
		harvest()

def is_or_plant():
	if get_entity_type() != Entities.Pumpkin:
		try_watering()
		plant(Entities.Pumpkin)
		return False
	return can_harvest()

def get_pumpkins_v2(limit):
	set_ground(Grounds.Soil)

	while num_items(Items.Pumpkin) < limit:
		if not stock_item(Items.Pumpkin_Seed, -1):
			return
		# First plant all
		plant_all(Entities.Pumpkin, False)

		if not stock_item(Items.Pumpkin_Seed, -1):
			return

		# Then check which plots don't have pumpkin yet
		leftover_pos = []
		for y in range(get_world_size()):
			for x in range(get_world_size()):
				if not is_or_plant():
					leftover_pos.append([x, y])
				move(East)
			move(North)

		# Finally retry failed plots
		while len(leftover_pos) > 0:
			pos = leftover_pos.pop(0)
			go_to(pos[0], pos[1])
			if not is_or_plant():
				if not stock_item(Items.Pumpkin_Seed, 10):
					return
				leftover_pos.append(pos)

		harvest()

#######################

def insert_sorted(li, x, y, value):
	# Insert [x,y] so that values are sorted (ascending)
	if len(li) == 0 or value > li[len(li)-1][0]:
		li.append([value, x, y])
	else:
		for i in range(0, len(li)):
			if value > li[i][0]:
				continue
			li.insert(i, [value, x, y])
			break
	return li

def harvest_most_power():
	home()
	try_power()

	sorted_positions = []

	# First initialise all positions sorted by number of petals
	for y in range(0, get_world_size()):
		for x in range(0, get_world_size()):
			if can_harvest() and get_entity_type() != Entities.Sunflower:
				harvest()
			insert_sorted(sorted_positions, x, y, measure())
			move(East)
		try_power()
		move(North)

	# Then harvest starting from most to least petals
	try_power()
	while len(sorted_positions) > 0:
		max_pos = sorted_positions.pop()
		go_to(max_pos[1], max_pos[2])
		harvest()
		plant(Entities.Carrots)


def get_sunflowers(limit):
	#limit=1000
	set_ground(Grounds.Soil)
	stock_item(Items.Carrot_Seed, -1)

	while num_items(Items.Power) < limit:
		if num_items(Items.Carrot) < 100:
			break

		plant_all(Entities.Sunflower, False)
		harvest_most_power()
		stock_item(Items.Carrot_Seed, -1)

#######################

def has_treasure(dig):
	if get_entity_type() == Entities.Treasure:
		if dig == True:
			harvest()
		return True
	return False

def try_go_to(x, y):
	# Move just 1 plot to x, y
	cx = get_pos_x()
	cy = get_pos_y()
	if cx < x:
		move(East)
	elif cx > x:
		move(West)
	if cy < y:
		move(North)
	elif cy > y:
		move(South)

def get_next_move(x, y, visited, visit_limit):
	size = get_world_size()
	dirs = [[x+1,y], [x,y-1], [x-1,y], [x,y+1]]

	for i in range(len(dirs)):
		nx = dirs[i][0]
		ny = dirs[i][1]
		if nx < 0 or ny < 0 or nx > size-1 or ny > size-1:
			continue  # Continue on out of bounds
		if visited[nx][ny] > visit_limit:
			continue  # Continue if target has higher penalty
		try_go_to(nx, ny)
		if get_pos() == [x, y]:
			continue  # Not moved (hedge wall)
		return [nx, ny]
	return None	 # No moves below visit_limit

def move_through_maze():
	# Check for treasure in case it spawned on drone's position
	if has_treasure(True):
		return

	# set up visited grid
	size = get_world_size()
	visited = []  # list[list[int]] with size*size

	for x in range(size):
		visited.append([])
		for y in range(size):
			visited[x].append(0)

	x = get_pos_x()
	y = get_pos_y()
	visited[x][y] = 1

	# Depth-First search by keeping track of visited plots
	while True:
		visit_limit = 0
		while True:
			npos = get_next_move(x, y, visited, visit_limit)
			if npos == None:
				# If no moves, penalise current position
				visited[x][y] += 1
				# And try again with higher limit
				visit_limit += 1
				try_power()
				continue
			else:
				break

		if has_treasure(True):
			return
		x = npos[0]
		y = npos[1]
		visited[x][y] += 1

def a_maze_ing(limit):
	clear()

	while num_items(Items.Gold) < limit:
		if num_items(Items.Pumpkin) < 100:
			do_a_flip()
			return

		stock_item(Items.Fertilizer, 10)

		# Setup maze
		try_watering()
		try_fertilize()
		plant(Entities.Bush)

		while not can_harvest():
			# Let it grow
			use_item(Items.Fertilizer)
			stock_item(Items.Fertilizer, 10)

		while get_entity_type() != Entities.Hedge and not has_treasure(False):
			# Grow to hedge
			use_item(Items.Fertilizer)
			stock_item(Items.Fertilizer, 1)

		# Find the treasure
		try_power()
		move_through_maze()

#######################

def move_next():
	# Move to next
	# This works because move lets you wrap around
	move(North)
	if get_pos_y() == 0:
		move(East)

def home():
	# Reset to 0, 0
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def go_to(x, y):
	# Move to x, y
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def get_pos():
	return [get_pos_x(), get_pos_y()]

def set_ground(ground):
	try_power()
	for y in range(0, get_world_size() * get_world_size()):
		if can_harvest():
			harvest()
		if get_ground_type() != ground:
			till()
		move_next()

def can_afford(item, qty):
	for r in get_cost(item):
		if num_items(r[0]) < (r[1] * qty):
			return False
	return True

def stock_item(item, to_plant):
	if to_plant < 0:
		to_plant = get_world_size() * get_world_size()
	if not can_afford(item, to_plant):
		return False
	to_buy = to_plant - num_items(item)
	if item != None and to_buy > 0:
		trade(item, to_buy)
	return True

def try_power():
	if num_items(Items.Power) > 50:
		use_item(Items.Power)
		use_item(Items.Power)
		use_item(Items.Power)

def try_fertilize():
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

def try_watering():
	if num_items(Items.Water_Tank) > 0 and get_water() < 0.2:
		use_item(Items.Water_Tank)

def water_plots(buy_only):
	water_tanks = 100
	carrots_req = water_tanks * 5

	if num_items(Items.Carrot) < carrots_req or num_items(Items.Water_Tank) > 50:
		return

	stock_item(Items.Empty_Tank, water_tanks)
	if buy_only:
		return
	while num_items(Items.Water_Tank) > 0 and get_water() < 0.2:
		use_item(Items.Water_Tank)
		move_next()

#######################

def main():
	# clear()

	wanted = [
		[Items.Hay     , 85000  ],
		[Items.Wood    , 100000 ],
		[Items.Carrot  , 100000 ],
		[Items.Pumpkin , 100000 ],
		[Items.Power   , 15000  ],
		[Items.Gold	   , 10000  ]
	]
	want_unlock = Unlocks.Speed

	while True:
		water_plots(True)

		for want in wanted:
			item = want[0]
			qty  = want[1]
			if num_items(item) > qty:
				continue
			if item == Items.Hay:
				quick_grass(qty)
			elif item == Items.Wood:
				get_wood(qty)
			elif item == Items.Carrot:
				get_carrots(qty)
			elif item == Items.Pumpkin:
				#get_pumpkins(qty)
				get_pumpkins_v2(qty)
			elif item == Items.Power:
				get_sunflowers(qty)
			elif item == Items.Gold:
				a_maze_ing(qty)

		if can_afford(want_unlock, 1):
			unlock(want_unlock)
		else:
			# Increase the wanted qty to the unlock reqs
			for req in get_cost(want_unlock):
				for want in wanted:
					if want[0] == req[0] and want[1] < req[1]:
						want[1] = req[1]