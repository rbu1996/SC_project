'''
This is the thrid version of Lazor Group Porject. 
Author: Ride Bu

Basic idea:
I use a Block() class to describe the blocks. The rest part is the same with v2.0. 

Some improvements compared with the v2.0. 
1. Use a class to describe different blocks 'A', 'B', 'C'. 
2. Solved a endless loop bug. 
3. Fixed blocks are considered. Add the coordinate and block type pair to possible position dictinary. 
'''
import itertools

class Block():
    def __init__(self, block_type):
        self.block_type = block_type
        
    def lazor_end(self, nei_block):
        if nei_block == 'A' or nei_block == 'B':
            return True
        return False
    
    def block_reflect_lazor(self, lazor_points, copy_goal_points, new_reflect_point, intersect_point, start_points):
        pass_goal(lazor_points, copy_goal_points, new_reflect_point)
        # print('new_reflect_point==', new_reflect_point)
        # print('copy_goal_points', copy_goal_points)

        if self.block_type == 'A':
            # print('A')
            return True
        elif self.block_type == 'B':
            # print('B')
            return False
        else:
            new_x = intersect_point[0] + intersect_point[2]
            new_y = intersect_point[1] + intersect_point[3]
            new_start_point = (new_x, new_y) + intersect_point[2:]
            pass_goal(lazor_points, copy_goal_points, new_start_point)
            if new_start_point not in start_points:
                start_points.append(new_start_point)
            return True


def read_bff(file):
    f = open(file)
    line = f.readline()

    grid = set()
    blocks = []
    start_points = []
    intersect_points = set()
    fixed_block = {}
    max_x = 0
    max_y = 0

    while line:
        # grid
        if line == 'GRID START\n':
            line = f.readline()
            y = 1
            while line != 'GRID STOP\n':
                temp = line.split()
                max_x = max(max_x,len(temp))
                for x, block in enumerate(temp):
                    if block == 'o' or block == 'A' or block == 'B' or block == 'C':
                        grid.add(((x + 1) * 2 - 1, y))
                        # fixed block 
                        if block == 'A' or block == 'B' or block == 'C':
                            fixed_block[((x + 1) * 2 - 1, y)] = Block(block)
                y += 2
                line = f.readline()
            max_y = y
        
        # block types and number
        while line.startswith(('A', 'B', 'C')):
            line = line.split()
            for i in range(int(line[1])):
                blocks.append(line[0])
            line = f.readline()
        
        # lazor start point
        while line.startswith('L'):
            line = line.split()
            start_points.append(tuple([int(line[i]) for i in range(1, len(line))]))
            line = f.readline()
        
        # intersect points 
        while line.startswith('P'):
            line = line.split()
            intersect_points.add((int(line[1]), int(line[2])))
            line = f.readline()
        
        line = f.readline()
    f.close()
    # print('grid', grid)
    # print('blocks', blocks)
    # print('start_points', start_points)
    # print('intersect_points', intersect_points)
    # print('max_x', max_x * 2)
    # print('max_y', max_y - 1)
    # print('fixed_block', fixed_block)
    return grid, blocks, start_points, intersect_points, fixed_block, max_x * 2, max_y - 1


def find_all_positions(blocks, grid):
    # print('blocks', blocks)
    # print('grid',grid)
    perm_blocks = itertools.permutations(blocks, len(blocks))
    comb_grid = itertools.combinations(grid, len(blocks))
    temp = [list(set(perm_blocks)), list(comb_grid)]
    res = itertools.product(*temp)
    # print(res)
    # print(list(res))
    return list(res)

def in_grid(x, y):
    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False


def cal_lazor(point, grid):
    # print('point', point)
    # print('grid', grid)
    lazor_points = []
    lazor_pass_grid = set()
    x = point[0]
    dx = point[2]
    y = point[1]
    dy = point[3]
    # print(grid)
    while in_grid(x, y):
        # print('(x,y)', x, y)
        lazor_points.append((x, y, dx, dy))
        if x % 2 == 1:
            if (x, y+dy) in grid:
                lazor_pass_grid.add((x, y+dy))
        if x % 2 == 0:
            if (x + dx, y) in grid:
                lazor_pass_grid.add((x+dx, y))
        x += dx
        y += dy
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    return lazor_points, lazor_pass_grid


def get_intersect_point(intersect_grid, lazor_points, start_point):
    # print('intersect_grid', intersect_grid)
    # print('lazor_points', lazor_points)
    # print('start_point', start_point)
    possible_intersect_point = set()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for int_grid in intersect_grid:
        for i in range(4):
            possible_intersect_point.add((int_grid[0] + dx[i], int_grid[1] + dy[i]) + start_point[2:])
    for point in lazor_points:
        if point in possible_intersect_point:
            # print('pp', point)
            return point
    
def get_intersect_grid(intersect_point):
    # print('intersect_point', intersect_point)
    grid = (0, 0)
    x = intersect_point[0]
    y = intersect_point[1]
    dx = intersect_point[2]
    dy = intersect_point[3]
    if x % 2 == 1:
        grid = (x, y+dy)
    if x % 2 == 0:
        grid = (x + dx, y)
    # print('grid', grid)
    return grid

def cal_reflect_start(point):
    # print('pppoint', point)
    dx = point[2]
    dy = point[3]
    if point[0] % 2 == 0:
        dx *= -1
    if point[1] % 2 == 0:
        dy *= -1
    # print((point[0], point[1], dx, dy))
    return (point[0], point[1], dx, dy)

# 计算光路上是否有通过goal的，如果有，把goal里面的remove
def pass_goal(lazor_points, copy_goal_points, reflect_point):
    for lazor_point in lazor_points:
        point = lazor_point[:2]
        if point in copy_goal_points:
            copy_goal_points.remove(point)
        if point == reflect_point[:2]:
            break
        

def check_position(position, grid, start_points, goal_points):
    print('position', position)
    print('grid', grid)
    print('start_points', start_points)
    print('goal_points', goal_points)
    copy_goal_points = goal_points.copy()
    copy_start_points = start_points.copy()

    
    # 用end_lazor 来表示光线的最末尾。如果末尾超过了grid的范围，那这个光线的路程结束了
    for start_point in copy_start_points: 
        print('-----------------')
        
        count = 0
        while True:
            # count += 1
            # if count == 5:
            #     print('=====')
            #     return True
            # print('start_point', start_point)
            lazor_points, lazor_pass_grid = cal_lazor(start_point, grid)
            print('start_point=====', start_point)
            print('position', [(key, val.block_type) for key, val in position.items()])
            intersect_grids = lazor_pass_grid & position.keys()
            print('intersect_grid', intersect_grids)
            print('lazor_points', lazor_points)
            print('lazor_pass_grid', lazor_pass_grid)
            # print('intersect_grids', intersect_grids)
            # print(set(position.keys()))
            if len(intersect_grids) == 0:
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                break
            else:
                intersect_point = get_intersect_point(intersect_grids, lazor_points, start_point)
                intersect_grid = get_intersect_grid(intersect_point)
                new_reflect_point = cal_reflect_start(intersect_point)
                print('new_reflect_point', new_reflect_point)
                if intersect_point[:2] == start_point[:2]:
                    print('euqla')
                    nei_x = intersect_point[0] * 2 - intersect_grid[0]
                    nei_y = intersect_point[1] * 2 - intersect_grid[1]
                    nei_grid = (nei_x, nei_y)
                    print('neighbor', nei_grid)
                    if nei_grid in position.keys():
                        print(position[nei_grid].block_type)
                        # print(a)
                        pos = position[nei_grid]
                        if pos.lazor_end(pos.block_type):
                            break
                        else:
                            break
                            new_temp = (new_reflect_point[0] + new_reflect_point[2], new_reflect_point[1] + new_reflect_point[3])
                            copy_start_points.append(new_temp + new_reflect_point[2:])
                
                if position[intersect_grid].block_reflect_lazor(lazor_points, copy_goal_points, new_reflect_point, intersect_point, copy_start_points):
                    # print('++++++++++++++')
                    start_point = new_reflect_point
                else:
                    break
                
    if len(copy_goal_points) == 0:
        # print('Find the solution!')
        # print(start_point)
        return True
    return False


max_x = 0
max_y = 0

def find_solution(file):
    global max_x, max_y
    # read the file
    grid, blocks, start_points, intersect_points, fixed_block, max_x, max_y = read_bff(file)
    print(read_bff(file))
    # find all possible combination between blocks and its position in grid 
    print(blocks)
    print(grid)
    all_poss_posi = find_all_positions(blocks, grid)
    count = 0
    
    for temp in all_poss_posi:
        block_position = {}
        for i, index in enumerate(temp[1]):
            block_position[index] = Block(temp[0][i])
        
        position=block_position.copy()
        position.update(fixed_block)
        # print([(key, val.block_type) for key, val in position.items()])
        if check_position(position, grid, start_points, intersect_points):
            print('Solution ===')
            for index, clas in block_position.items():
                print(index, clas.block_type)
            return

if __name__ == "__main__":
    find_solution('mad_1.bff')
    # {(7, 3): 'A', (1, 5): 'A', (5, 1): 'C'}