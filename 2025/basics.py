from utils import *

def get_grass(limit=100000):
    try_power()

    for i in range(SIZE):
        if get_ground_type() != Grounds.Grassland:
            if can_harvest():
                harvest()
            till()
        move(North)

    while num_items(Items.Hay) < limit:
        if can_harvest():
            harvest()
        move(North)
        try_power(30)

def get_wood(limit=100000, fertilize=False):
    try_power()

    while num_items(Items.Wood) < limit:
        if can_harvest():
            harvest()
        p = get_pos_x() + get_pos_y()
        if p % 2 == 0:
            plant(Entities.Tree)
            try_watering()
            if fertilize:
                try_fertilize()
        else:
            plant(Entities.Bush)
        move_next()
        try_power(30)

def get_carrots(limit=10000):
    if num_items(Items.Carrot) >= limit:
        return
    try_power()
    set_ground(Grounds.Soil, Entities.Carrot)
    while num_items(Items.Carrot) < limit:
        if can_harvest():
            harvest()
        plant(Entities.Carrot)
        #try_watering()
        #try_fertilize()
        move_next()
        try_power(5)

def get_pumpkins(limit=100000):
    try_power()
    home()

    while num_items(Items.Pumpkin) < limit:
        try_power()
        set_ground(Grounds.Soil, Entities.Pumpkin)
        try_power()
        home()

        leftover_pos = []
        for y in range(SIZE):
            for x in range(SIZE):
                if not is_or_plant(Entities.Pumpkin):
                    leftover_pos.append((x, y))
                move(East)
            move(North)

        try_power()

        while len(leftover_pos) > 0:
            pos = leftover_pos.pop(0)
            go_to(pos[0], pos[1])
            if not is_or_plant(Entities.Pumpkin):
                leftover_pos.append(pos)

        harvest()

if __name__ == "__main__":
    get_grass(20000000)
    get_wood(750000)
    get_carrots(150000)
    get_pumpkins(100000)
