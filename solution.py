import itertools


def read_bff(file):
    f = open(file)
    line = f.readline()

    gird = []
    blocks = []
    start_points = []
    intersect_points = set()
    while line:
        # grid
        if line == 'GRID START\n':
            line = f.readline()
            y = 1
            while line != 'GRID STOP\n':
                # dictionary {coordinate: block type}
                temp = line.split()
                row = []
                for x, block in enumerate(temp):
                    # row.append({[x, y], block})
                    row.append([(x + 1) * 2 - 1, y, block])
                    # print(row)
                y += 2
                line = f.readline()
                gird.append(row)
        
        # block types and number
        while line.startswith(('A', 'B', 'C')):
            line = line.split()
            blocks.append([line[0], int(line[1])])
            line = f.readline()
        
        # lazor start point
        while line.startswith('L'):
            line = line.split()
            start_points.append([int(line[i]) for i in range(1, len(line))])
            line = f.readline()
        
        # intersect points 
        while line.startswith('P'):
            line = line.split()
            intersect_points.add((int(line[1]), int(line[2])))
            line = f.readline()
        
        line = f.readline()
    f.close()
    print('gird', gird)
    print('blocks', blocks)
    print('start_points', start_points)
    print('intersect_points', intersect_points)

    '''
    gird [[[1, 1, 'o'], [3, 1, 'o'], [5, 1, 'o'], [7, 1, 'o']], [[1, 3, 'o'], [3, 3, 'o'], [5, 3, 'o'], [7, 3, 'o']], [[1, 5, 'o'], [3, 5, 'o'], [5, 5, 'o'], [7, 5, 'o']], [[1, 7, 'o'], [3, 7, 'o'], [5, 7, 'o'], [7, 7, 'o']]]
    blocks [['A', 2], ['C', 1]]
    start_points [[2, 7, 1, -1]]
    intersect_points {(3, 0), (2, 5), (4, 3), (4, 7)}
    '''
    return gird, blocks, start_points, intersect_points

def get_blocks_list(blocks):
    block_list = []
    for block in blocks:
        for i in range(block[1]):
            block_list.append(block[0])
    # print(block_list)
    return block_list

def in_grid(x, y, max_x, max_y):
    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False

max_x = 0
max_y = 0
def cal_lazor(point):
    lazor_points = []
    lazor_points.append(point)
    lazor_pass_grid = []
    x = point[0]
    dx = point[2]
    y = point[1]
    dy = point[3]
    while in_grid(x, y, max_x-1, max_y-1):
        x += dx
        y += dy
        lazor_points.append([x, y, dx, dy])
        if x % 2 == 1:
            if in_grid(x, y +1, max_x, max_y):
                lazor_pass_grid.append([x, y+ 1])
            if in_grid(x, y -1, max_x, max_y):
                lazor_pass_grid.append([x, y- 1])
    print('lazor_points', lazor_points)
    print('lazor_pass_grid', lazor_pass_grid)
    '''
    lazor_points [[2, 7, 1, -1], [3, 6, 1, -1], [4, 5, 1, -1], [5, 4, 1, -1], [6, 3, 1, -1], [7, 2, 1, -1], [8, 1, 1, -1]]
    lazor_pass_grid [[3, 7], [3, 5], [5, 5], [5, 3], [7, 3], [7, 1]]
    '''
    return lazor_points, lazor_pass_grid

def cal_reflect_start(point):
    if point[0] % 2 == 0:
        point[2] *= -1
    if point[1] % 2 == 0:
        point[3] *= -1
    return point

'''
def perm_solution(blocks, blocks_index, intersect_points, lazor_points, lazor_pass_grid, lazor, visited):
    if len(intersect_points) == 0:
        return True
    
    # iterate every points in lazor_line
    for point in lazor_points:
        new_start_point = cal_reflect_start(point)
        new_lazor_points, new_lazor_pass_grid = cal_lazor(point)
        perm_solution(blocks[1:], 1, intersect_points, )
'''


def find_solution(file):
    gird, blocks, start_points, intersect_points = read_bff(file)
    blocks_list = get_blocks_list(blocks)

    

    '''
    for start_point in start_points:
        global max_x, max_y
        max_x = len(gird[0]) * 2
        max_y = len(gird) * 2
        lazor_points, lazor_pass_grid = cal_lazor(start_point)
        permutation_blocks = set(itertools.permutations(blocks_list))
        # print(permutation_blocks)
        # for perm in permutation_blocks:
        #     # for block in perm:
        #         # 找到所有的几个bloack在空间中的放置方法！！！内积
        #     if perm_solution(perm, intersect_points):
        #         return
    '''

if __name__ == "__main__":
    # read_bff('mad_1.bff')
    find_solution('mad_1.bff')
