from utils import *

DIRS = [East, South, West, North]

def has_treasure(dig=True):
    if get_entity_type() == Entities.Treasure:
        if dig == True:
            harvest()
        return True
    return False
    
def get_next_move(x, y, visited, visit_limit):
    size = get_world_size()
    npos = [(x+1,y), (x,y-1), (x-1,y), (x,y+1)]

    for i in range(4):
        nx, ny = npos[i]
        if nx < 0 or ny < 0 or nx > size-1 or ny > size-1:
            continue
        if visited[nx][ny] > visit_limit:
            continue
        if not move(DIRS[i]):
            continue  # Not moved
        return npos[i]
    return None  # No moves below visit_limit

def move_through_maze():
    if has_treasure():
        return
    # set up visited grid
    size = get_world_size()
    visited = []

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
                visited[x][y] += 1
                visit_limit += 1
                try_power()
                continue
            else:
                break

        if has_treasure():
            return
        x, y = npos
        visited[x][y] += 1

def a_maze_ing(limit):
    clear()

    substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
 
    while num_items(Items.Gold) < limit:
        if num_items(Items.Weird_Substance) < 100:
            do_a_flip()
            return

        # Setup maze
        try_watering()
        try_fertilize()
        plant(Entities.Bush)
        use_item(Items.Weird_Substance, substance)
        while not can_harvest():
            use_item(Items.Fertilizer)
        while get_entity_type() != Entities.Hedge and not has_treasure(False):
            use_item(Items.Fertilizer)
            stock_item(Items.Fertilizer, 1)

        # Find the treasure
        try_power()
        move_through_maze()
        
if __name__ == "__main__":
    a_maze_ing(1000000)