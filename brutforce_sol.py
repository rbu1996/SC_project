import itertools


def read_bff(file):
    f = open(file)
    line = f.readline()

    grid = set()
    blocks = []
    start_points = []
    intersect_points = set()
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
            start_points.append(tuple([int(line[i]) for i in range(1, len(line))]))
            line = f.readline()
        
        # intersect points 
        while line.startswith('P'):
            line = line.split()
            intersect_points.add((int(line[1]), int(line[2])))
            line = f.readline()
        
        line = f.readline()
    f.close()
    print('grid', grid)
    print('blocks', blocks)
    print('start_points', start_points)
    print('intersect_points', intersect_points)
    print('max_x', max_x * 2)
    print('max_y', max_y - 1)


    '''
    gird [(1, 1), (3, 1), (5, 1), (1, 3)]
    blocks ['B', 'C']
    start_points [(1, 4, 1, 1], [1, 6, 1, -1)]
    intersect_points {(0, 5), (6, 5)}
    '''

    return grid, blocks, start_points, intersect_points, max_x * 2, max_y - 1

def get_blocks_list(blocks):
    block_list = []
    for block in blocks:
        for i in range(block[1]):
            block_list.append(block[0])
    # print(block_list)
    return block_list

def find_all_positions(blocks, grid):
    perm_blocks = itertools.permutations(blocks, len(blocks))
    comb_grid = itertools.combinations(grid, len(blocks))
    temp = [list(set(perm_blocks)), list(comb_grid)]
    res = itertools.product(*temp)
    return res

def in_grid(x, y):
    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False
    '''
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    # print(grid) # {(1, 3), (3, 3), (3, 1), (1, 5), (5, 1), (1, 1), (5, 3)}
    for i in range(4):
        # print((x+dx[i], y + dy[i]))
        if (x+dx[i], y + dy[i]) in grid:
            # print('====')
            return True
    return False
    '''


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
            if (x, y+dy) in grid:
                lazor_pass_grid.add((x, y+dy))
        if x % 2 == 0:
            if (x + dx, y) in grid:
                lazor_pass_grid.add((x+dx, y))
        x += dx
        y += dy
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    '''
    lazor_points [(5, 0, -1, 1), (4, 1, -1, 1), (3, 2, -1, 1), (2, 3, -1, 1), (1, 4, -1, 1), (0, 5, -1, 1)]
    lazor_pass_grid {(5, 1), (3, 1), (3, 3), (1, 3)}
    '''
    return lazor_points, lazor_pass_grid



def calculate_dis(a, b):
    dis = 0
    for i in range(2):
        dis += (a[i] - b[i]) ** 2
    return dis

def find_closest_position(reflect_point, intersect):
    closest_position = list(intersect)[0]
    min_dis = calculate_dis(closest_position, reflect_point)
    for pos in list(intersect):
        if min_dis > calculate_dis(pos, reflect_point):
            closest_position = pos
    return closest_position

def get_intersect_point(intersect_grid, reflect_point):
    # print('reflect_point', reflect_point)
    intersect_point = set()
    intersect_grid_list = list(intersect_grid)
    # print('==', intersect_grid_list)
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for int_grid in intersect_grid_list:
        for i in range(4):
            intersect_point.add((int_grid[0] + dx[i], int_grid[1] + dy[i], reflect_point[2], reflect_point[3]))
    return intersect_point

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

# 计算光路上是否有通过goal的，如果有，把goal里面的remove
def pass_goal(lazor_points, copy_goal_points, reflect_point):
    for lazor_point in lazor_points:
        point = (lazor_point[0], lazor_point[1])
        if point in copy_goal_points:
            copy_goal_points.remove(point)
        if point == (reflect_point[0], reflect_point[1]):
            break
        

# position is a dir {index : block}
def check_position(position, grid, start_points, goal_points):
    # position {(1, 1): 'B', (3, 1): 'B'}
    copy_goal_points = goal_points.copy()
    reflect_point = start_points[0]
    # print('----------------------')
    # print(position)
    # print(start_points)
    # print(goal_points)
    # print('----------------------')

    # 用end_lazor 来表示光线的最末尾。如果末尾超过了grid的范围，那这个光线的路程结束了
    for start_point in start_points:

        # python中的数组可以动态append。如果是透明块，可以直接把新产生的光线append到start_pointz
        # 这样相当于又多一个光线出发。多一个光线！

        # initialize 
        reflect_point = start_point
        end_point = start_point
        print('----------------------')
        print('position', position)

        # while True:
        for i in range(3):
            lazor_points, lazor_pass_grid = cal_lazor(reflect_point, grid)
            # print('----------------------')
            print('reflect_point', reflect_point)
            print('lazor_points', lazor_points)
            print('lazor_pass_grid', lazor_pass_grid)
            # print('----------------------')
            # lazor走过的光路和预先设定的position的重合位置
            intersect_grid = lazor_pass_grid & set(position.keys())
            print('intersect_grid', intersect_grid)
            # 如果没有任何重合，那这个光路不用继续计算了。没有任何反射
            if len(intersect_grid) == 0:
                # 算一下是否有通过goal
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                print('++++++++break++++++++++++')
                break
            # if several blocks are in the same lazor line, only consider the closest one
            # 如果有重合，只需要计算离光点最近的面的反射
            else:
                # print('reflect_point', reflect_point)
                # find the position that is cloest to reflect_point
                # 通过之前求出来的在光路上的grid求出所有可能的反射面 （就是grid的上下左右四个面)
                intersect_point = get_intersect_point(intersect_grid, reflect_point)
                # 在所有的可能的反射面里面求出距离光点最近的 新的反射点
                closest_position = find_closest_position(reflect_point, intersect_point)
                # closest_grid = find_closest_position(reflect_point, intersect_grid)
                # 新的反射点 update reflect_point
                reflect_point = cal_reflect_start(closest_position)
                # calculate passed goal
                # 计算所有经过的goal
                print('new reflect_point', reflect_point)
                pass_goal(lazor_points, copy_goal_points, reflect_point)
            print('++')
    # 比较goal是不是全部通过了
    print('copy_goal_points', copy_goal_points)
    print()
    if len(copy_goal_points) == 0:
        print('成功了！')
        return 

    '''
    # iterator ends when all points in position dictionary is used or all intersection_points are passed
    # while len(position) != 0 and len(intersect_points) != 0:
    print('-------------')
    print('position', position)
    for i in range(1):
        # for reflect_point in reflect_points:
        lazor_points, lazor_pass_grid = cal_lazor(reflect_point, grid)

        intersect_grid = lazor_pass_grid & set(position.keys())
        # no intersection positions
        if len(intersect_grid) == 0:
            continue
        # if several blocks are in the same lazor line, only consider the closest one
        else:
            print('reflect_point', reflect_point)
            # find the position that is cloest to reflect_point
            intersect_point = get_intersect_point(intersect_grid, reflect_point)
            closest_position = find_closest_position(reflect_point, intersect_point)
            # closest_grid = find_closest_position(reflect_point, intersect_grid)
            reflect_point = cal_reflect_start(closest_position)
            # calculate passed goal
            for lazor_point in lazor_points:
                if (lazor_point[0], lazor_point[1]) == (reflect_point[0], reflect_point[1]):
                    break
                if (lazor_point[0], lazor_point[1]) in copy_intersect_points:
                    copy_intersect_points.remove((lazor_point[0], lazor_point[1]))
            print('==============')
            print('reflect_point', reflect_point)
            print('lazor_pass_grid', lazor_pass_grid)
            print('lazor_points', lazor_points)
            print('intersect', intersect_grid)
            print('closest_position', closest_position)
            print('==============')
        return 
        '''

max_x = 0
max_y = 0

def find_solution(file):
    global max_x, max_y
    # read the file
    grid, blocks, start_points, intersect_points, max_x, max_y = read_bff(file)
    
    # find all possible combination between blocks and its position in grid 
    all_poss_posi = find_all_positions(blocks, grid)

    # cal_lazor(start_points[0], grid)

    for temp in all_poss_posi:
        position = {}
        for index in temp[1]:
            position[index] = temp[0][1]
        # print(position)
        '''
        {(1, 1): 'B', (3, 1): 'B'}
        {(1, 1): 'B', (5, 1): 'B'}
        {(1, 1): 'B', (1, 3): 'B'}
        {(3, 1): 'B', (5, 1): 'B'}
        {(3, 1): 'B', (1, 3): 'B'}
        '''
        check_position(position, grid, start_points, intersect_points)

    print(max_x, max_y)
if __name__ == "__main__":
    find_solution('mul_lazor.bff')