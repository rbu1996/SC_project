'''
This is the second version of Lazor Group Porject. 
Author: Ride Bu

Basic idea:
Put blocks to all possible positions and compute all potential board. 
Iterate all these boards. Compute the light path in board. If all target points
are passed, we find the solution. Print out the solution. 

Some improvements compared with the v1.0. 
1. v1.0 can only solve the situation of one lazor L and block 'A'. But v2.0 can solve
all potential boards. 
2. v1.0 choose the coordinate of block according to the light path. The coordinate of 
next block depends on the previous one. The board is produced step by step. But in v2.0, 
the board is given in the begining. What we do is to check if the board is a correct solution. 
3. v1.0 uses recursion. If the grid is very large, recursion may cause stack overflow problem. 
But v2.0 will not have the same problem. 
4. In v2.0 dictionary type is used to show the corresponding relationship between block and grid 
coordinate. The time complexity of search a coordinate is O(1). Time efficieny is improved. 
'''

import itertools

def read_bff(file):
    '''
    Compared with version 1.0. 
    I changed the data type of output grid and target_points to set. 
    This small change can greatly improve the algroithm performance. 
    The check_position() search the elements in the grid and target_points many times. 
    If I use the list type, the time complexity of every search is O(n). 
    But for set type, the time greatly reduce to O(1)
    '''
    f = open(file)
    line = f.readline()

    grid = set()
    blocks = []
    start_points = []
    target_points = set()
    max_x = 0
    max_y = 0

    while line:
        # grid
        if line == 'GRID START\n':
            line = f.readline()
            y = 1
            while line != 'GRID STOP\n':
                temp = line.split()
                max_x = max(max_x, len(temp))
                # row = []
                for x, block in enumerate(temp):
                    if block == 'o':
                        grid.add(((x + 1) * 2 - 1, y))
                    # print(row)
                y += 2
                line = f.readline()
                # grid.append(row)
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
            start_points.append(tuple([int(line[i])
                                       for i in range(1, len(line))]))
            line = f.readline()

        # intersect points
        while line.startswith('P'):
            line = line.split()
            target_points.add((int(line[1]), int(line[2])))
            line = f.readline()

        line = f.readline()
    f.close()
    print('grid', grid)
    print('blocks', blocks)
    print('start_points', start_points)
    print('target_points', target_points)
    print('max_x', max_x * 2)
    print('max_y', max_y - 1)
    '''
    grid {(7, 3), (3, 5), (1, 3), (3, 3), (5, 5), (7, 1), (3, 1), (5, 7), (7, 7), (3, 7), (1, 5), (7, 5), (1, 7), (5, 1), (1, 1), (5, 3)}
    blocks ['A', 'A', 'A', 'A']
    start_points [(5, 0, -1, 1)]
    target_points {(5, 6), (5, 4), (3, 4), (3, 6)}
    '''

    return grid, blocks, start_points, target_points, max_x * 2, max_y - 1

def find_all_positions(blocks, grid):
    '''
    This will find all potential board. 
    For example, permutation of blocks [A, A, B] is ([A, A, B], [A, B, A], [B, A, A]). 
    The combination of grid coordinate is {[(1, 2), (1, 3), (1, 4)], [(1, 2), (1, 3), (2, 1)] ...}. 
    itertools.product() computes the cartesian product of input iterables.
    The result is {[A, A, B], [(1, 2), (1, 3), (1, 4)]}. Every block corresponds to a coordinate. 
    It represents all potential boards
    '''
    perm_blocks = itertools.permutations(blocks, len(blocks))
    comb_grid = itertools.combinations(grid, len(blocks))
    temp = [list(set(perm_blocks)), list(comb_grid)]
    res = itertools.product(*temp)
    return res


def in_grid(x, y):
    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False


def cal_lazor(point, grid):
    # print('point', point)
    # print('grid', grid)
    lazor_points = []
    # lazor_points.append(point)
    lazor_pass_grid = set()
    x = point[0]
    dx = point[2]
    y = point[1]
    dy = point[3]
    while in_grid(x, y):
        lazor_points.append((x, y, dx, dy))
        # print('xxx', x)
        if x % 2 == 1:
            if (x, y + dy) in grid:
                lazor_pass_grid.add((x, y + dy))
        if x % 2 == 0:
            if (x + dx, y) in grid:
                lazor_pass_grid.add((x + dx, y))
        x += dx
        y += dy
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    return lazor_points, lazor_pass_grid


def get_intersect_point(intersect_grid, lazor_points, reflect_point):
    '''
    This will compute the intersect point coordinate between block and light path.
    '''
    possible_intersect_point = set()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for int_grid in intersect_grid:
        # print('int_grid', int_grid)
        for i in range(4):
            possible_intersect_point.add(
                (int_grid[0] + dx[i], int_grid[1] + dy[i], reflect_point[2], reflect_point[3]))
        # print('possible_intersect_point', possible_intersect_point)
    for point in lazor_points:
        if point in possible_intersect_point:
            # print('point', point)
            return point


def get_intersect_grid(intersect_point):
    '''
    This will compute the intersect grid coordinate between block and light path.
    '''
    grid = (0, 0)
    x = intersect_point[0]
    y = intersect_point[1]
    dx = intersect_point[2]
    dy = intersect_point[3]
    if x % 2 == 1:
        grid = (x, y + dy)
    if x % 2 == 0:
        grid = (x + dx, y)
    # print('grid', grid)
    return grid


def cal_reflect_start(point):
    dx = point[2]
    dy = point[3]
    if point[0] % 2 == 0:
        dx *= -1
        # dx = point[2] * -1
    if point[1] % 2 == 0:
        dy *= -1
        # dy = point[3] * -1
    return (point[0], point[1], dx, dy)


def pass_goal(lazor_points, copy_goal_points, reflect_point):
    for lazor_point in lazor_points:
        point = (lazor_point[0], lazor_point[1])
        # print('pass_goal point', point)
        if point in copy_goal_points:
            copy_goal_points.remove(point)
            # print('remove point')
        if point == (reflect_point[0], reflect_point[1]):
            # print('break')
            break


# position is a dir {index : block}
def check_position(position, grid, start_points, goal_points):
    # position {(1, 1): 'B', (3, 1): 'B'}
    copy_goal_points = goal_points.copy()
    # reflect_point = start_points[0]
    # print('===================')
    # print('position', position)

    # print('start_points', start_points)
    # start_points.pop()
    # print('start_poinst remove', start_points)
    for start_point in start_points:
        # python中的数组可以动态append。如果是透明块，可以直接把新产生的光线append到start_pointz
        # 这样相当于又多一个光线出发。多一个光线！

        # initialize
        reflect_point = start_point
        count = 0
        
        while True:
            lazor_points, lazor_pass_grid = cal_lazor(reflect_point, grid)
            # print('reflect_point', reflect_point)
            # print('lazor_points', lazor_points)
            # print('lazor_pass_grid', lazor_pass_grid)

            # the intersect area between lazor path and potential board 
            intersect_grids = lazor_pass_grid & set(position.keys())
            # print('intersect_grids', intersect_grids)
            if len(intersect_grids) == 0:
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                # print('break')
                break
            # if several blocks are in the same lazor line, only consider the closest one
            else:
                # find the position that is cloest to reflect_point
                intersect_point = get_intersect_point(intersect_grids, lazor_points, reflect_point)
                intersect_grid = get_intersect_grid(intersect_point)
                # print('position[intersect_grid]', position[intersect_grid])
                # consider three different blocks 'A', 'B' and 'C'
                if position[intersect_grid] == 'A':
                    reflect_point = cal_reflect_start(intersect_point)
                    # calculate passed goal
                    # print('lazor_points', lazor_points)
                    pass_goal(lazor_points, copy_goal_points, reflect_point)
                    # print(position[intersect_grid], 'reflect')
                    # print('A reflect grid', intersect_grid)
                if position[intersect_grid] == 'B':
                    reflect_point = cal_reflect_start(intersect_point)
                    pass_goal(lazor_points, copy_goal_points, reflect_point)
                    # print(position[intersect_grid])
                    # print(intersect_grid)
                    break

                # new_start_point = (intersect_point[0] + intersect_point[2], intersect_point[1] + intersect_point[3], intersect_point[2], intersect_point[3])
                # if new_start_point in start_points:
                #     continue
                if position[intersect_grid] == 'C':
                    new_start_point = (intersect_point[0] + intersect_point[2], intersect_point[1] +
                                       intersect_point[3], intersect_point[2], intersect_point[3])
                    # print('new_start_point', new_start_point)

                    if new_start_point in start_points:
                        continue
                   
                    reflect_point = cal_reflect_start(intersect_point)
                    pass_goal(lazor_points, copy_goal_points, reflect_point)

                    # print(position[intersect_grid], 'reflect')
                    # print('lazor_points', lazor_points)
                    # print(intersect_grid)
                    # print('new_start_point', new_start_point)
                    # pass_goal(lazor_points, copy_goal_points, new_start_point)
                    start_points.append(new_start_point)

                    # print(position[intersect_grid], '投射')
                    # print('lazor_points', lazor_points)
                    # print(intersect_grid)
                    break

            # print('copy_goal_points', copy_goal_points)

    # if all goal points are passed, return the ture. Stop the iterate.
    if len(copy_goal_points) == 0:
        print('Success! ')
        return True
    # else:
    #     print('Fail!')
    return False


max_x = 0
max_y = 0


def find_solution(file):
    global max_x, max_y
    # read the file
    grid, blocks, start_points, intersect_points, max_x, max_y = read_bff(file)

    # find all possible combination between blocks and its position in grid
    all_poss_posi = find_all_positions(blocks, grid)
    # print(list(all_poss_posi))
    # cal_lazor(start_points[0], grid)
    count = 0
    # position = {(5, 3): 'A', (5, 5): 'C'}
    # check_position(position, grid, start_points, intersect_points)

    for temp in all_poss_posi:
        # print('temp', temp)
        position = {}
        for i, index in enumerate(temp[1]):
            position[index] = temp[0][i]
            # print('i', i, index)
        count += 1
        # print(count)
        if check_position(position, grid, start_points, intersect_points):
            print('position===', position)
            return

    # print(count)
    # print(max_x, max_y)
    # position {(7, 3): 'A', (5, 9): 'A', (7, 5): 'A', (3, 9): 'A', (5, 3): 'A'}


if __name__ == "__main__":
    find_solution('vertices_2.bff')