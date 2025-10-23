from utils import *

def multi_grass(limit):
    set_ground(Grounds.Grassland)   
    while num_items(Items.Hay) < limit:
        for_all_row(harvest)
        try_power(30)
    
def multi_wood(limit, fertilize=False):
    set_ground(Grounds.Grassland)
    
    def row():
        for _ in range(get_world_size()):
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
            move(East)
 
    while num_items(Items.Wood) < limit:
        home()
        try_power()
        for_each_row(row)

def multi_carrot(limit):
    set_ground(Grounds.Soil, Entities.Carrot)
    
    def action():
        if can_harvest():
            harvest()
        plant(Entities.Carrot)
        #try_watering()
        
    while num_items(Items.Carrot) < limit:
        try_power()
        for_all_row(action)

def multi_pumpkin(limit):
    try_power()
    world_size = get_world_size() 
    home()

    def action():
        y = get_pos_y()
        row = []

        # First check: fill with failed pumpkin positions
        for x in range(world_size):
            if not is_or_plant(Entities.Pumpkin):
                row.append(get_pos_x())
            move(East)
        try_power()
        while len(row) > 0:
            x = row.pop(0)
            go_to(x, y)
            if not is_or_plant(Entities.Pumpkin):
                row.append(x)
        return True

    while num_items(Items.Pumpkin) < limit:
        try_power()
        set_ground(Grounds.Soil, Entities.Pumpkin)
        try_power()
        home()
        for_each_row_fast(action)
        harvest()

if __name__ == "__main__":
    # for_all_row(harvest)
    #clear()
    multi_grass(5000000)
    # multi_wood(40000000)
    multi_carrot(4200000)
    multi_pumpkin(5000000)