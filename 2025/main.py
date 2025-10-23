from utils import *
from basics import *
from sunflowers import get_sunflowers
from companion import companion_plant, check_cost
from maze import a_maze_ing
from multi import *
from cactus import multi_cactus
from dino import get_bones

def reset_wanted():
    return [ #             B  M  k 
        [Items.Hay     ,     5000000 ],
        [Items.Wood    ,     5000000 ],
        [Items.Carrot  ,     1700000 ],
        [Items.Pumpkin ,     5000000 ],
        [Items.Weird_Substance, 2000 ],
        [Items.Power   ,        2500 ],
        [Items.Gold    ,       20000 ],
        [Items.Cactus  ,     2600000 ],
        [Items.Bone    ,       10000 ],
    ]

def main():
    # clear()

    wanted = reset_wanted()
    want_unlock = [
        Unlocks.Cactus,
        Unlocks.Mazes,
        Unlocks.Dinosaurs,
        Unlocks.Pumpkins,
    ]

    while len(want_unlock) > 0:
        for want in wanted:
            item, qty = want
            to_get_qty = qty - num_items(item) 
            if to_get_qty <= 0:
                continue
            check_cost(item, to_get_qty)
            if item == Items.Hay:
                # get_grass(qty)
                multi_grass(qty)
            elif item == Items.Wood:
                # get_wood(qty)
                multi_wood(qty)
            elif item == Items.Weird_Substance:
                q = num_items(Items.Wood) + qty * 4
                # get_wood(q, True)
                multi_wood(q, True)
            elif item == Items.Carrot:
                # get_carrots(qty)
                multi_carrot(qty)
            elif item == Items.Pumpkin:
                multi_pumpkin(qty)
            elif item == Items.Power:
                get_sunflowers(qty)
            elif item == Items.Gold:
                a_maze_ing(qty)
            elif item == Items.Cactus:
                multi_cactus(qty)
            elif item == Items.Bone:
                get_bones(qty)

        if unlock(want_unlock[0]):
            want_unlock.pop(0)
            wanted = reset_wanted()
        else:
            costs = get_cost(want_unlock[0])
            if not costs:
                want_unlock.pop(0)
                wanted = reset_wanted()
            for req in costs:
                for want in wanted:
                    if want[0] == req and want[1] < costs[req]:
                        want[1] = costs[req]
                        break

if __name__ == "__main__":
    change_hat(Hats.Traffic_Cone)
    harvest()
    #for_all_row(harvest)
    #set_ground(Grounds.Grassland)
    main()
    #companion_plant(Items.Carrot, 200000)
    #companion_plant(Items.Wood, 2000000)

    #set_ground(Grounds.Soil, Entities.Carrot)
    #get_sunflowers(100000)