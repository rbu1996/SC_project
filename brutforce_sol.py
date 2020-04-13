import itertools

def read_bff(file):
    '''
    注释
    '''
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

def get_intersect_point(intersect_grid, lazor_points, reflect_point):
    possible_intersect_point = set()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for int_grid in intersect_grid:
        for i in range(4):
            possible_intersect_point.add((int_grid[0] + dx[i], int_grid[1] + dy[i], reflect_point[2], reflect_point[3]))
    for point in lazor_points:
        if point in possible_intersect_point:
            return point
    '''
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
    '''
def get_intersect_grid(intersect_point):
    grid = (0, 0)
    x = intersect_point[0]
    y = intersect_point[1]
    dx = intersect_point[2]
    dy = intersect_point[3]
    if x % 2 == 1:
        grid = (x, y+dy)
    if x % 2 == 0:
        grid = (x + dx, y)
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
    copy_start_points = start_points.copy()
    # reflect_point = start_points[0]
    print('===================')
    print('position', position)
    # print(start_points)
    # print(goal_points)
    # print('----------------------')

    # 用end_lazor 来表示光线的最末尾。如果末尾超过了grid的范围，那这个光线的路程结束了
    for start_point in copy_start_points: # 这里要做deep copy

        # python中的数组可以动态append。如果是透明块，可以直接把新产生的光线append到start_pointz
        # 这样相当于又多一个光线出发。多一个光线！

        # initialize 
        # reflect_point = start_point
        # end_point = start_point
        print('----------------------')
        # print('position', position)
        print('start_points ==', start_point)
        print()

        count = 0
        while True:
            count += 1
            # if count == 10:
            #     print('22222222222222')
            #     return 
            lazor_points, lazor_pass_grid = cal_lazor(start_point, grid)
            print('start_point', start_point)
            # print('lazor_points', lazor_points)
            # print('lazor_pass_grid', lazor_pass_grid)
            # lazor走过的光路和预先设定的position的重合位置
            intersect_grids = lazor_pass_grid & set(position.keys())
            print('intersect_grid', intersect_grids)
            # 如果没有任何重合，那这个光路不用继续计算了。没有任何改变 直的通向结束
            if len(intersect_grids) == 0:
                # 算一下是否有通过goal
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                # print('break')
                break
            # if several blocks are in the same lazor line, only consider the closest one
            # 如果有重合，只需要计算离光点最近的面的反射
            else:
                # 在这里判断intersect_grid的类型
                # 如果是 'A' 只有反射：
                # find the position that is cloest to start_point
                # 通过之前求出来的在光路上的grid求出所有可能的反射面 （就是grid的上下左右四个面)
                intersect_point = get_intersect_point(intersect_grids, lazor_points, start_point)
                intersect_grid = get_intersect_grid(intersect_point)
                new_reflect_point = cal_reflect_start(intersect_point)
                # 无限循环的起因
                # start_point 和 interest 重合。光线在两个block之间来回反射 导致了无穷循环
                if (intersect_point[0], intersect_point[1]) == (start_point[0], start_point[1]):
                    # print(a)
                    # 找到夹着start point的两个block
                    # dx = intersect_grid[0] - intersect_point[0]
                    # dy = intersect_grid[1] - intersect_point[1]
                    temp_grid = (intersect_point[0] * 2 - intersect_grid[0] , intersect_point[1] * 2 - intersect_grid[1])
                    # 如果temp_grid上面没有块 正常情况 不会死循环
                    # 如果temp_grid上面有block 分情况讨论
                    if temp_grid in position.keys():
                        # 如果grid上是A B
                        if position[temp_grid] == 'A' or position[temp_grid] == 'B':
                            # 光线被卡死了 光线结束了
                            break
                        # 如果grid上面是C
                        if position[temp_grid] == 'C':
                            # 只需要把投射光线放到start_points里面 然后结束
                            # add_start_point = (new_reflect_point[0] + , n)
                            # copy_start_points.append()
                            print(new_reflect_point, '===================')
                            # new_start_point = cal_reflect_start(new_reflect_point)
                            # print(new_start_point, '===================')
                            copy_start_points.append((new_reflect_point[0] + new_reflect_point[2], new_reflect_point[1] + new_reflect_point[3], new_reflect_point[2], new_reflect_point[3]))
                            # print(a)
                            break

                # 在所有的可能的反射面里面求出距离光点最近的 新的反射点
                # 新的反射点 update start_point
                # 如果是 A
                if position[intersect_grid] == 'A':
                    # new_reflect_point = cal_reflect_start(intersect_point)
                    # calculate passed goal
                    # 计算所有经过的goal
                    pass_goal(lazor_points, copy_goal_points, new_reflect_point)
                    start_point = new_reflect_point
                    print(position[intersect_grid], 'reflect')
                    print(intersect_grid)
                    

                # 如果是 'B' 碰到B 光线就没了
                # 和 A 的intersect point是一样的 都是相交的点
                # 后续结果是没了 没光了 直接跳出循环 （A是反射）
                if position[intersect_grid] == 'B':
                    # start_point = cal_reflect_start(intersect_point)
                    pass_goal(lazor_points, copy_goal_points, new_reflect_point)
                    start_point = new_reflect_point
                    print(position[intersect_grid])
                    print(intersect_grid)
                    break

                # 如果是'C' C碰到光线一个反射一个直的通过
                # 反射的情况直接归到A里面计算
                # 折射的情况还是直接射出去
                # new_start_point = (intersect_point[0] + intersect_point[2], intersect_point[1] + intersect_point[3], intersect_point[2], intersect_point[3])
                # if new_start_point in start_points:
                #     continue
                if position[intersect_grid] == 'C':
                    new_start_point = (intersect_point[0] + intersect_point[2], intersect_point[1] + intersect_point[3], intersect_point[2], intersect_point[3])
                    # 减少重复计算 如果new在start_point里面已经存在了 直接continue
                    if new_start_point in copy_start_points:
                        continue
                    # C 有两种情况 1 一种是光线从射到外表面 --> 外表面反射 + 投射
                    #            2 光线射到内表面 --> 不反射 只投射

                    # 反射
                    start_point = new_reflect_point
                    print('new_reflect_point', new_reflect_point)
                    # calculate passed goal
                    # 计算所有经过的goal
                    pass_goal(lazor_points, copy_goal_points, start_point)
                    # print(position[intersect_grid], 'reflect')
                    # print(intersect_grid)
                    
                    # 投射
                    # 直接通过的相当于从intersect_point + (dx dy)的位置增加一个新的光路
                    # new_start_point = (intersect_point[0] + intersect_point[2], intersect_point[1] + intersect_point[3], intersect_point[2], intersect_point[3])
                    pass_goal(lazor_points, copy_goal_points, new_start_point)
                    copy_start_points.append(new_start_point)
                    # print(position[intersect_grid], '投射')
                    # print(intersect_grid)
                    

            print('copy_goal_points', copy_goal_points)



    # 比较goal是不是全部通过了
    # print('copy_goal_points', copy_goal_points)
    # print()

    # 打印正确答案
    # ans = {(3, 3): 'A', (5, 3): 'A', (7, 5): 'A', (5, 7): 'A', (1, 7): 'A'}
    # if ans == position:
    #     print('222222222222222222222222')
    #     return True
    if len(copy_goal_points) == 0:
        print('成功了！')
        return True
    return False


max_x = 0
max_y = 0

def find_solution(file):
    global max_x, max_y
    # read the file
    grid, blocks, start_points, intersect_points, max_x, max_y = read_bff(file)
    
    # find all possible combination between blocks and its position in grid 
    all_poss_posi = find_all_positions(blocks, grid)
    print(all_poss_posi)
    # cal_lazor(start_points[0], grid)
    count = 0
    # position = {(3, 5): 'C', (5, 5): 'A', (3, 3): 'A'}
    # check_position(position, grid, start_points, intersect_points)
    
    for temp in all_poss_posi:
        # print(temp)
        position = {}
        for i, index in enumerate(temp[1]):
            position[index] = temp[0][i]
        
        count += 1
        print(count)
        if check_position(position, grid, start_points, intersect_points):
            print('position', position)
            return
        
    print(count)
    # print(max_x, max_y)
    # position {(7, 3): 'A', (5, 9): 'A', (7, 5): 'A', (3, 9): 'A', (5, 3): 'A'}

if __name__ == "__main__":
    find_solution('numbered_6.bff')
    # {(1, 2): 'A', (3, 2): 'C'}