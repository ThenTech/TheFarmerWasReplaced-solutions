SIZE = get_world_size()

def get_pos():
    return get_pos_x(), get_pos_y()

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

def go_to_simple(x, y):
    while get_pos_x() < x:
        move(East)
    while get_pos_x() > x:
        move(West)
    while get_pos_y() < y:
        move(North)
    while get_pos_y() > y:
        move(South)

def move_dir(n, dir):
    for _ in range(n):
        move(dir)

def go_to(x, y):
    SIZE = get_world_size()
    cx, cy = get_pos()

    delta_x = (x - cx)             # 0 - 6   = -6
    delta_x_east = delta_x % SIZE  # -6 % 10 = 4
    delta_x_west = -delta_x % SIZE #  6 % 10 = 6

    if delta_x_west <= delta_x_east:
        move_dir(delta_x_west, West)
    else:
        move_dir(delta_x_east, East)

    delta_y = (y - cy)
    delta_y_north = delta_y % SIZE
    delta_y_south = -delta_y % SIZE

    if delta_y_north <= delta_y_south:
        move_dir(delta_y_north, North)
    else:
        move_dir(delta_y_south, South)


#####################

def call_arg(f, arg):
    def g():
        f(arg)
    return g

def await_first(drones):
    for h in drones:
        if not has_finished(h):
            wait_for(h)
            return True

def await_all(drones):
    for h in drones:
        wait_for(h)

def _create_for_each(dir, fast=False):
    SIZE = get_world_size()

    def for_each2(cb):
        progress = 0
        drones = []

        while progress < SIZE:
            # First spawn as many as possible
            while progress < SIZE and num_drones() < max_drones():
                drones.append(spawn_drone(cb))
                progress += 1
                move(dir)
            if progress < SIZE and num_drones() == max_drones():
                # If not done, try to do the task ourselves
                if not fast or (dir == East and get_pos_x() == SIZE-1) or (dir == North and get_pos_y() == SIZE-1):
                    cb()
                    progress += 1
                    move(dir)
                else:
                    # Or if fast, wait for the next drone, so we can immediately spawn more
                    await_first(drones)
        await_all(drones)  # Sync

    return for_each2

def _create_for_all(dir, fe):
    SIZE = get_world_size()
    def for_all(f):
        home()
        def row():
            for _ in range(SIZE):
                f()
                move(dir)
        fe(row)
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
