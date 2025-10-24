from utils import *

def create_sorter(dir):
    def reset_pos(j):
        if dir == North:
            go_to(get_pos_x(), j)
        else:
            go_to(j, get_pos_y())
    def sort():
        for i in range(SIZE):
            is_sorted = True
            for j in range(SIZE - i - 1):
                reset_pos(j)
                if measure() > measure(dir):
                    is_sorted = False
                    swap(dir)
                move(dir)
            if is_sorted:
                return
    return sort

def multi_cactus(limit=1000):
    if num_items(Items.Cactus) >= limit:
        return

    def reset():
        set_ground_single(Grounds.Soil, Entities.Cactus)
    def action():
        plant(Entities.Cactus)
        try_watering()

    for_all_row(reset)
    row_sort = create_sorter(East)
    col_sort = create_sorter(North)

    while num_items(Items.Cactus) < limit:
        home()
        for_each_row_fast(row_sort)
        home()
        for_each_col_fast(col_sort)
        harvest()
        for_all_row(action)

if __name__ == "__main__":
    multi_cactus(1000000)
