from utils import *

def insert_sorted(li, x, y):
    val = x + y
    size = len(li)
    if size == 0 or val > (li[size-1][0] + li[size-1][1]):
        li.append((x, y))
    else:
        for i in range(0, size):
            if val > (li[i][0] + li[i][1]):
                continue
            li.insert(i, (x, y))
            break
    return li

def add_flower(di, x, y, value):
    # Instead of keeping all of them in one list,
    # keep (15-7) lists according to petals, and
    # keep those sorted on closest positions
    if value not in di:
        di[value] = []
    insert_sorted(di[value], x, y)
    return di

def harvest_most_power():
    world_size = get_world_size()
    home()
    try_power()

    petal_set = {}

    for y in range(0, world_size):
        for x in range(0, world_size):
            add_flower(petal_set, x, y, measure())
            move(East)
        try_power()
        move(North)

    try_power()
    for petals in range(15, 6, -1):
        sorted_positions = petal_set[petals]
        while len(sorted_positions) > 0:
            x, y = sorted_positions.pop()
            go_to(x, y)
            harvest()
            plant(Entities.Carrot)
        try_power()

def get_sunflowers(limit=10000):
    home()
    set_world_size(12) # Smaller to speed things up
    
    while num_items(Items.Power) < limit:
        set_ground(Grounds.Soil, Entities.Sunflower)
        harvest_most_power()
        
    set_world_size(0)
        
if __name__ == "__main__":
    get_sunflowers(10000)