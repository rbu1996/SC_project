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

def pass_goal(lazor_points, copy_goal_points, reflect_point):
    for lazor_point in lazor_points:
        print(lazor_point)
        if len(reflect_point) != 0:
            if (lazor_point[0], lazor_point[1]) == (reflect_point[0], reflect_point[1]):
                break
        else:
            if lazor_point in copy_goal_points:
                copy_goal_points.remove(lazor_point)

# file = 'mul_lazor.bff'
# grid, blocks, start_points, intersect_points, max_x, max_y = read_bff(file)

# reflect_point = (3, 2, -1, -1)
# lazor_points, lazor_pass_grid = cal_lazor(reflect_point, grid)

# print('lazor_points', lazor_points)
# print('lazor_pass_grid', lazor_pass_grid)


lazor_points = [(4, 5, -1, 1), (3, 6, -1, 1)]
reflect_point = ()
copy_goal_points = {(3, 6)}
pass_goal(lazor_points, copy_goal_points, reflect_point)



