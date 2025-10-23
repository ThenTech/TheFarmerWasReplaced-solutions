from basics import *
from multi import *

ITEM2SEED = {
    Items.Hay: Entities.Grass,
    Items.Wood: Entities.Tree, # Tree
    Items.Carrot: Entities.Carrot,
    Items.Pumpkin: Entities.Pumpkin,
    # Items.Cactus: Entities.Cactus,
    # Items.Gold: Entities.Sunflower,
}

ITEM2UNLOCK = {
    Items.Hay: Unlocks.Grass,
    Items.Wood: Unlocks.Trees,
    Items.Carrot: Unlocks.Carrots,
    Items.Pumpkin: Unlocks.Pumpkins,
}

def check_cost(item, requested):
    if item not in ITEM2SEED:
        return False
    entity = ITEM2SEED[item]
    costs = get_cost(entity)
    level_mod = 1
    if item in ITEM2UNLOCK:
        level_mod = 2**(num_unlocked(ITEM2UNLOCK[item])-1)

    for other in costs:
        request_other = costs[other] * requested / level_mod
        if num_items(other) < request_other:
            if other == Items.Hay:
                multi_grass(request_other)
            elif other == Items.Wood:
                multi_wood(request_other)
            elif other == Items.Weird_Substance:
                multi_wood(num_items(other) + request_other * 4, True)
            elif other == Items.Carrot:
                multi_carrot(request_other)
            elif other == Items.Pumpkin:
                multi_pumpkin(request_other)
            else:
                print("Unknown?", other)
                return False
    return True

def swap_ground(for_item):
    # Swap ground type
    ground = get_ground_type()
    case1 = ground == Grounds.Soil and for_item == Entities.Grass
    case2 = ground == Grounds.Grassland and for_item != Entities.Grass
    if case1 or case2:
        till()   
             
def plant_x(req, want, x, y):
    go_to(x, y)
    etype = get_entity_type()
    if req == want and etype == req:
        return True
    if etype and etype != Entities.Grass:
        return False
    
    # Swap ground type
    swap_ground(req)

    if req != Entities.Grass:
        try_watering()
        plant(req)
    return True

def companion_plant(preferred_item, limit=100000):
    world_size = get_world_size()
    entity = ITEM2SEED[preferred_item]

    #if not check_cost(entity, limit - num_items(preferred_item)):
    #   return False

    try_power()
    if entity == Entities.Grass:
        set_ground(Grounds.Grassland)
    else:
        set_ground(Grounds.Soil)
        
    while num_items(preferred_item) < limit:
        try_power()
        home()
        farm = {"requested": [], "companions": []}
        done = set()
        
        for y in range(world_size):
            for x in range(world_size):
                pos = (x, y)
                if pos not in done and plant_x(entity, entity, x, y):
                    farm["requested"].append((x, y))
                    done.add((x, y))
                    companion = get_companion()
                    if companion != None:
                        i, j = companion[1]
                        if (i, j) not in done and plant_x(companion[0], entity, i, j):
                            done.add((i, j))
                            farm["companions"].append((i, j))
            try_power()
        
        while len(farm["requested"]):
            x, y = farm["requested"].pop()
            go_to(x, y)
            while not can_harvest():
                continue
            harvest()        
        while len(farm["companions"]):
            x, y = farm["companions"].pop()
            go_to(x, y)
            harvest()
            swap_ground(entity)