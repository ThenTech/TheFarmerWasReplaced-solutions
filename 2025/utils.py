def move_next():
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
    moved = 0
    while get_pos_x() < x:
        moved += move(East)
    while get_pos_x() > x:
        moved += move(West)
    while get_pos_y() < y:
        moved += move(North)
    while get_pos_y() > y:
        moved += move(South)
    return moved

#####################

def await_first(drones):
    for h in drones:
        if not has_finished(h):
            wait_for(h)
            return True

def await_all(drones):
    for h in drones:
        wait_for(h)

def _create_for_each(dir, fast=False):
    size = get_world_size()
    
    def for_each(cb):
        drones = []
        for _ in range(size):
            handle = spawn_drone(cb)
            if not handle:
                # Wait for next completion, but only if not on last
                # row/col, then just do it ourselves.
                if fast and (get_pos_x() < size-1 and get_pos_y() < size-1):
                    # Or: wait for the first unfinished drone
                    # so we can spawn a new one immediately?
                    # (else the main drone could still be busy while
                    #  others have finished, blocking the spawning)
                    await_first(drones)
                    drones.append(spawn_drone(cb))
                    move(dir)
                else:
                    cb() # Either do the taks ourselves
            else:
                drones.append(handle)
                if fast:
                    move(dir)
            if not fast:  
                move(dir)
        # Sync
        await_all(drones)
    return for_each

def _create_for_all(dir, fe):
    def for_all(f):
        home()
        def row():
            for _ in range(get_world_size()):
                f()
                move(dir)
        for_each_row(row)
    return for_all
    
for_each_row = _create_for_each(North)
for_each_row_fast = _create_for_each(North, True)
for_each_col = _create_for_each(East)
for_each_col_fast = _create_for_each(East, True)

for_all_row = _create_for_all(East, for_each_row)
for_all_col = _create_for_all(North, for_each_col)

#####################

def try_watering():
    if num_items(Items.Water) > 0 and get_water() < 0.2:
        use_item(Items.Water)
        
def try_fertilize():
    if num_items(Items.Fertilizer) > 0:
        use_item(Items.Fertilizer)

def try_power(every_x_seconds=0):
    if every_x_seconds > 0 and (get_time() % every_x_seconds) < 2:
        return
    if num_items(Items.Power) > 50:
        use_item(Items.Power)

def set_ground_single(ground, and_plant=None):
    if can_harvest():
        harvest()
    if get_ground_type() != ground:
        till()
    if and_plant:
        try_watering()
        plant(and_plant)

def set_ground(ground, and_plant=None):
    def reset():
        set_ground_single(ground, and_plant)
    for_all_row(reset)
        
def is_or_plant(type):
    if get_entity_type() != type:
        harvest()
        try_watering()
        plant(type)
        return False
    return can_harvest()