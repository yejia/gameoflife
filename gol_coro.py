#!/usr/bin/env python

import sys, time
from collections import namedtuple

ALIVE = 1
EMPTY = 0

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

def count_neighbors(y, x):
    n_ = yield Query(y+1, x)
    ne = yield Query(y+1, x+1)
    nw = yield Query(y+1, x-1)
    w_ = yield Query(y, x-1)
    e_ = yield Query(y, x+1)
    s_ = yield Query(y-1, x)
    se = yield Query(y-1, x+1)
    sw = yield Query(y-1, x-1)
    neighbors_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbors_states:
        if state == ALIVE:
            count += 1
    return count    



def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


TICK = object

def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK    


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state
    


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny
    
class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY]*self.width)

    def __str__(self):
        str_l = []
        for _ in range(self.width+2):
            str_l.append('*')        
        str_l.append('\n')
        for i in range(self.height):
            str_l.append('*')
            for j in range(self.width):
                if self.rows[i][j] == EMPTY:
                    str_l.append('.')                
                if self.rows[i][j] == ALIVE:
                    str_l.append('o')                
            str_l.append('*')  
            str_l.append('\n')    
        str_l.append('\n')
        for i in range(self.width+2):
            str_l.append('*')        
        str_l.append('\n')
        return ''.join(str_l)

    def query(self, y, x):
        # return self.rows[y % self.height][x % self.width]
        #if not a ball surface
        if 0<=y<self.height and 0<=x<self.width:
            return self.rows[y][x]
        else:
            return EMPTY    


    def assign(self, y, x, state):
        # self.rows[y % self.height][x % self.width] = state
        #if not a ball surface
        if 0<=y<self.height and 0<=x<self.width:
            self.rows[y][x] = state




def read_grid(filename):
    with open(filename) as f:
        lines = [line for line in f.readlines() if not (line.startswith('!') or line == '\n')]        
        height = len(lines)
        width = max([len(line) for line in lines])
        #make the matirx larger than the pattern
        size_factor = 2
        grid = Grid(height*size_factor, width*size_factor)
        for i, line in enumerate(lines):
            for j, char in enumerate(line):                
                if char == 'O':                    
                    grid.assign(height//2+i, width//2+j, ALIVE)
        return grid            








# grid = Grid(5, 9)
# grid.assign(0, 3, ALIVE)
# grid.assign(1, 4, ALIVE)
# grid.assign(2, 2, ALIVE)
# grid.assign(2, 3, ALIVE)
# grid.assign(2, 4, ALIVE)

# sim = simulate(grid.height, grid.width)
# for _ in range(5):
#     print(grid)
#     grid = live_a_generation(grid, sim)


# grid = Grid(5, 5)
# grid.assign(1, 1, ALIVE)
# grid.assign(2, 2, ALIVE)
# grid.assign(2, 3, ALIVE)
# grid.assign(3, 3, ALIVE)

# sim = simulate(grid.height, grid.width)
# for _ in range(5):
#     print(grid)
#     grid = live_a_generation(grid, sim)    


if __name__ == '__main__':
    pattern = sys.argv[1]

    # import gc
    # found_objects = gc.get_objects()
    # print('%d objects before' % len(found_objects))

    # import tracemalloc
    # tracemalloc.start(10)
    # time1 = tracemalloc.take_snapshot()

    grid = read_grid(pattern)
    t1 = time.time()
    sim = simulate(grid.height, grid.width)
    for _ in range(1000):
        # print(grid)
        grid = live_a_generation(grid, sim)    
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

    # found_objects = gc.get_objects()
    # print('%d objects after' % len(found_objects))
    # for obj in found_objects[:3]:
    #     print(repr(obj)[:100])

    
    # def fun():
    #     grid = read_grid(pattern)    
    #     sim = simulate(grid.height, grid.width)            
    #     grid = live_a_generation(grid, sim)      
    # from cProfile import Profile
    # from pstats import Stats
    # profiler = Profile()
    # profiler.runcall(fun)
    # stats = Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats('cumulative')
    # stats.print_stats()
    # stats.print_callers()

