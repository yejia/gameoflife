#!/usr/bin/env python


import dill as pickle
import sys, time
import concurrent.futures
from gol_coro import read_grid, Grid, EMPTY, ALIVE, game_logic, Transition, Query
from pathos.multiprocessing import ProcessingPool as Pool

s = pickle.dumps(lambda x,y: x+y)
print(s)


def new_state(grid):
    def compute_state(query):
        y = query.y
        x = query.x
        n_ = grid.query(y+1, x)
        ne = grid.query(y+1, x+1)
        nw = grid.query(y+1, x-1)
        w_ = grid.query(y, x-1)
        e_ = grid.query(y, x+1)
        s_ = grid.query(y-1, x)
        se = grid.query(y-1, x+1)
        sw = grid.query(y-1, x-1)
        neighbors_states = [n_, ne, e_, se, s_, sw, w_, nw]
        count = 0
        for state in neighbors_states:
            if state == ALIVE:
                count += 1
        # grid.assign(y, x, game_logic(grid.query(query.y, query.x), count))
        # return Transition(y, x, game_logic(grid.query(query.y, query.x), count))
        return y, x, game_logic(grid.query(query.y, query.x), count)
    return compute_state

def next_gen(grid):
    nextg = Grid(grid.height, grid.width)    
    for _ in range(grid.height):
        nextg.rows.append([EMPTY]*grid.width)       

    qlist = [Query(i, j) for i in range(grid.height) for j in range(grid.width)]
    p = Pool(8)
    #** closure
    new_states = list(p.map(lambda x:new_state(grid)(x), qlist))
    for y, x, state in new_states: 
            # nextg.assign(trans.y, trans.x, trans.state)
            nextg.assign(y, x, state)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     new_states =  list(executor.map(lambda x:new_state(grid, x)(x), qlist))
    #     # print('new_states:', new_states)
    #     for y, x, state in new_states: 
    #         # nextg.assign(trans.y, trans.x, trans.state)
    #         nextg.assign(y, x, state)
    return nextg        
            

if __name__ == '__main__':
    pattern = sys.argv[1]
    grid = read_grid(pattern)    
    t1 = time.time()
    print(grid)    
    for _ in range(100):        
        grid = next_gen(grid)
        print(grid)
    t2 = time.time()
    print('Using time:', t2-t1)   

