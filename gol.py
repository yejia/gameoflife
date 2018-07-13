#!/usr/bin/env python

import sys, time
from gol_coro import read_grid, Grid, EMPTY, ALIVE


def  next_gen(grid):
    nextg = Grid(grid.height, grid.width)    
    for _ in range(grid.height):
        nextg.rows.append([EMPTY]*grid.width)       

    for i in range(grid.height):
        for j in range(grid.width):
            count_neighbors = 0
            for p in range(i-1, i+2):
                for q in range(j-1, j+2):
                    if 0<=p<grid.height and 0<=q<grid.width:
                        count_neighbors += grid.query(p, q)
            count_neighbors -= grid.query(i, j)
            if count_neighbors == 3 or count_neighbors+grid.query(i, j) == 3:                
                nextg.assign(i, j, ALIVE)
            else:
                nextg.assign(i, j, EMPTY)
            # The alternaive logic
            # if grid.query(i, j) == ALIVE:
            #     if count_neighbors < 2:
            #         nextg.assign(i, j, EMPTY)
            #     elif count_neighbors > 3:
            #         nextg.assign(i, j, EMPTY)
            # else:
            #     if count_neighbors == 3:
            #         nextg.assign(i, j, ALIVE)            
    return nextg


        


if __name__ == '__main__':
    pattern = sys.argv[1]
    
    # import gc
    # found_objects = gc.get_objects()
    # print('%d objects before' % len(found_objects))

    # import tracemalloc
    # tracemalloc.start(10)
    # time1 = tracemalloc.take_snapshot()
    
    grid = read_grid(pattern)    
    print(grid)
    t1 = time.time()
    for _ in range(1000):        
        grid = next_gen(grid)
        print(grid)
    t2 = time.time()
    print('Using time:', t2-t1)   

    # time2 = tracemalloc.take_snapshot()
    # stats = time2.compare_to(time1, 'lineno')
    # for stat in stats:
    #     print(stat)
    # print('-----------------------------------')    
    # stats = time2.compare_to(time1, 'traceback')
    # top = stats[0]
    # print('\n'.join(top.traceback.format()))
    # for stat in stats:
    #     print(stat)



    # found_objects = gc.get_objects()
    # print('%d objects after' % len(found_objects))
    # for obj in found_objects[:3]:
    #     print(repr(obj)[:100])

    # def fun():
    #     grid = read_grid(pattern)    
    #     grid = next_gen(grid)

    # from cProfile import Profile
    # from pstats import Stats
    # profiler = Profile()
    # profiler.runcall(fun)
    # stats = Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats('cumulative')
    # stats.print_stats()
    # stats.print_callers() 

