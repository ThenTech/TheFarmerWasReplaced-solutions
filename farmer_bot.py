def quick_grass(limit):
	try_power()
	while num_items(Items.Hay) < limit:
		if get_ground_type() == Grounds.Soil:
			till()
		if can_harvest():
			harvest()
		move_next()
		if get_time() % 30 < 10:
			try_power()

def get_wood(limit):
	while num_items(Items.Wood) < limit:
		if can_harvest():
			harvest()
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			try_watering()
			plant(Entities.Tree)
		else:
			if get_ground_type() == Grounds.Soil:
				till()
		move_next()

def get_carrots(limit):
	set_ground(Grounds.Soil)

	while num_items(Items.Carrot) < limit:
		stock_item(Items.Carrot_Seed, -1)
			
		if num_items(Items.Hay) < 100 or num_items(Items.Wood) < 100:
			break
		try_power()
		while num_items(Items.Carrot_Seed) > 0:
			if can_harvest():
				harvest()
			plant(Entities.Carrots)
			try_watering()
			move_next()

#######################

def plant_all(plant_entity, needs_check):
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
				
		for y in range(0, world_size):
			if get_entity_type() != None and get_entity_type() != plant_entity:
				while not can_harvest():
					pass
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
	set_ground(Grounds.Soil)
	while num_items(Items.Pumpkin) < limit:
		stock_item(Items.Pumpkin_Seed, -1)
			
		if num_items(Items.Carrot) < 100:
			break
		
		plant_all(Entities.Pumpkin, True)
		harvest()

#######################

def insert_sorted(li, x, y, value):
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
	
	for y in range(0, get_world_size()):
		for x in range(0, get_world_size()):
			if can_harvest() and get_entity_type() != Entities.Sunflower:
				harvest()
			insert_sorted(sorted_positions, x, y, measure())
			move(East)
		move(North)

	try_power()
	while len(sorted_positions) > 0:
		max_pos = sorted_positions.pop() 
		go_to(max_pos[1], max_pos[2])
		harvest()
		plant(Entities.Carrots)
        

def get_sunflowers(limit):
	#limit=1000
	set_ground(Grounds.Soil)
	
	while num_items(Items.Power) < limit:
		stock_item(Items.Sunflower_Seed, -1)
			
		if num_items(Items.Carrot) < 100:
			break
			
		plant_all(Entities.Sunflower, False)
		stock_item(Items.Carrot_Seed, -1)
		harvest_most_power()

#######################

def move_next():
	# Move to next
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
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def set_ground(ground):
	try_power()
	for y in range(0, get_world_size() * get_world_size()):
		if can_harvest():
			harvest()
		if get_ground_type() != ground:
			till()
		move_next()

def try_power():
	if num_items(Items.Power) > 50:
		use_item(Items.Power)
		use_item(Items.Power)
		use_item(Items.Power)

def try_watering():
	if num_items(Items.Water_Tank) > 0 and get_water() < 0.2:
		use_item(Items.Water_Tank)

def water_plots(buy_only):
	water_tanks = 100
	carrots_req = water_tanks * 5
	
	if num_items(Items.Carrot) < carrots_req:
		return
		
	stock_item(Items.Empty_Tank, water_tanks)
	if buy_only:
		return
	while num_items(Items.Water_Tank) > 0 and get_water() < 0.2:
		use_item(Items.Water_Tank)
		move_next()
        

def main():
	# clear()
	
	MIN_HAY     = 5000
	MIN_WOOD    = 10000
	MIN_CARROTS = 10000
	MIN_PUMPKIN = 10000
	MIN_SUNFLOW = 2000
	
	while True:
		water_plots(True)
		
		if num_items(Items.Hay) < MIN_HAY:
			quick_grass(MIN_HAY)
		elif num_items(Items.Wood) < MIN_WOOD:
			get_wood(MIN_WOOD)
		elif num_items(Items.Carrot) < MIN_CARROTS:
			get_carrots(MIN_CARROTS)
		elif num_items(Items.Pumpkin) < MIN_PUMPKIN:
			get_pumpkins(MIN_PUMPKIN)
		elif num_items(Items.Power) < MIN_SUNFLOW:
			get_sunflowers(MIN_SUNFLOW)
		else:
			break
	do_a_flip()
				