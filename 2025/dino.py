from utils import *

def get_x_lim(tx, ty):
    if ty == 0:
        return max(0, tx)
    return 0

def get_y_limit(x, y, tx, ty, dir):
    s_max = get_world_size() - 1
    
    min_row = 1
    if x == s_max:
        min_row = 0
    
    if x == tx:
        if dir == North:
            if y > ty:
                # Correction if ty is South of us
                return s_max
            return ty
        elif dir == South:
            if y < ty:
                # Correction if ty is North of us
                return min_row
            return max(min_row, ty)
    else:
        if dir == North:
            return s_max
        elif dir == South:
            return min_row
    return None

def continue_dir(tx, ty, dir):
    ylim = get_y_limit(get_pos_x(), get_pos_y(), tx, ty, dir)
    if dir == South:
        while get_pos_y() > ylim:
            move(South)
    elif dir == North:
        while get_pos_y() < ylim:
            move(North)

def move_until(tx, ty):
    # Traverse entire field until x, y
    world_size = get_world_size()

    while True:
        try_power()
        x, y = get_pos_x(), get_pos_y()
        if x == tx and y == ty:
            return True
        if y >= 1 and x == (world_size-1):
            # Correction if we ended up on the last column
            continue_dir(tx, ty, South)
        elif y == (world_size-1):
            move(East)
            continue_dir(tx, ty, South)
        elif y == 1:
            # Try shortcut if entire snake is on left side
            if can_move(South):
                if tx < x:
                    # Restart in West if apple is there
                    move(South)
                    continue
                elif tx > x:
                    # Or go up to ty and then straight East
                    if ty <= 1:
                        # Correction if ty on 0 or 1 row
                        go_to(tx, 1)
                    else:
                        move(East)
                        go_to(x+1, ty)
                    go_to(tx, ty)
                    return True
            # Continue towards East
            move(East)
            continue_dir(tx, ty, North)
        elif y == 0 and x > 0:
            xlim = get_x_lim(tx, ty)
            while get_pos_x() > xlim:
                move(West)
        else:
            # Just continue until end of column
            if x % 2 == 0:
                dir = North
            else:
                dir = South
            continue_dir(tx, ty, dir)
 
    return False

def get_bones(limit):
    try_power()
    for_all_row(harvest)
    world_size = get_world_size()
    max_apples = world_size * world_size
    
    change_hat(Hats.Traffic_Cone)
    home()

    while num_items(Items.Bone) < limit:
        apples = 1
        change_hat(Hats.Dinosaur_Hat)
    
        # Safe traverse field
        while apples < max_apples:
            try_power()
            next_x, next_y = measure()
            if not move_until(next_x, next_y):
                break
            apples += 1
    
        change_hat(Hats.Traffic_Cone)


if __name__ == "__main__":
    get_bones(10000)
    