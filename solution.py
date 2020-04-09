import itertools
import copy


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
    gird [[[1, 1, 'o'], [3, 1, 'o'], [5, 1, 'o']], [[1, 3, 'o'], [3, 3, 'o'], [5, 3, 'o']], [[1, 5, 'o'], [3, 5, 'o'], [5, 5, 'o']]]
    blocks [['A', 2]]
    start_points [[5, 0, -1, 1]]
    intersect_points {(3, 6)}
    '''
    return gird, blocks, start_points, intersect_points

def get_blocks_list(blocks):
    block_list = []
    for block in blocks:
        for i in range(block[1]):
            block_list.append(block[0])
    # print(block_list)
    return block_list

max_x = 0
max_y = 0

def in_grid(x, y):
    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False


def cal_lazor(point):
    lazor_points = []
    lazor_points.append(tuple(point))
    lazor_pass_grid = []
    x = point[0]
    dx = point[2]
    y = point[1]
    dy = point[3]
    while in_grid(x + dx, y + dy):
        x += dx
        y += dy
        lazor_points.append((x, y, dx, dy))
        # print([x, y, dx, dy])
        if x % 2 == 1:
            if in_grid(x, y + 1):
                lazor_pass_grid.append((x, y+ 1))
            if in_grid(x, y - 1):
                lazor_pass_grid.append((x, y- 1))
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    '''
    lazor_points [[2, 7, 1, -1], [3, 6, 1, -1], [4, 5, 1, -1], [5, 4, 1, -1], [6, 3, 1, -1], [7, 2, 1, -1], [8, 1, 1, -1]]
    lazor_pass_grid [[3, 7], [3, 5], [5, 5], [5, 3], [7, 3], [7, 1]]
    '''
    return lazor_points, lazor_pass_grid

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
intersect_points = {}

def check_solution(block_position_list, lazor_points, lazor_pass_grid):
    # read the file
    # gird, blocks_type, start_points, intersect_points = read_bff('easy.bff')
    # find all passed points, check if they contains all intersect_points
    '''
    block_position_list [[1, 3], [5, 5]]
    lazor_points [(5, 0, -1, 1), (4, 1, -1, 1), (3, 2, -1, 1), (2, 3, -1, 1), (2, 3, 1, 1), (3, 4, 1, 1), (4, 5, 1, 1)]
    lazor_pass_grid [(3, 3), (3, 1), (1, 5), (1, 3), (3, 5), (3, 3), (5, 5)]

    intersect_points {(3, 6)}
    '''
    if len(block_position_list)<= 0 or len(lazor_points) <= 0 or len(lazor_pass_grid) <= 0:
        return False
    
    # print(lazor_points[-1])
    last_lazor_points, last_lazor_pass_grid = cal_lazor(cal_reflect_start(lazor_points[-1]))
    if lazor_points[-1] == (4, 5, 1, 1):
        print('===')
        print(lazor_points)
        print(last_lazor_points)
    # lazor_points.extend(last_lazor_points)
    # lazor_pass_grid.extend(last_lazor_pass_grid)

    # find if lazor_points in intersect_points
    count = 0
    copy_intersect_points = intersect_points.copy()
    for point in lazor_points + last_lazor_points:
        temp = (point[0], point[1])
        if temp in copy_intersect_points:
            copy_intersect_points.remove(temp)
    if len(copy_intersect_points) == 0:
        return True
    return False

# find = False

def find_block_position(blocks, index, start_point, block_position_list, lazor_points, lazor_pass_grid):
    # if find == True:
    #     return
    # print('blocks', blocks)
    # print('index', index)
    # print('start_point', start_point)
    # print('block_position_list', block_position_list)
    '''
    blocks ['A', 'A']
    index 0
    start_point [5, 0, -1, 1]
    block_position_list []
    '''
    
    # check if current block_position_list is a correct solution 
    # print('block_position_list', block_position_list)
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    # print('----------------------------------------------')
    '''
    block_position_list [[3, 1], [5, 3]]
    lazor_points [[4, 1, -1, 1], [5, 2, 1, -1], [6, 3, 1, 1]]
    lazor_pass_grid [[5, 3], [5, 1]]    
    '''
    check_solution(block_position_list, lazor_points, lazor_pass_grid)


    if index == len(blocks):
        # if check_solution():
        #     # 把solution打印出来
        #     print()
        # print('block_position_list', block_position_list)
        '''
        block_position_list [[3, 1], [5, 1]]
        block_position_list [[3, 1], [5, 3]]
        block_position_list [[3, 3], [3, 1]]
        block_position_list [[3, 3], [1, 1]]
        block_position_list [[1, 3], [3, 3]]
        block_position_list [[1, 3], [3, 5]]
        block_position_list [[1, 3], [5, 5]]
        block_position_list [[1, 5], [1, 3]]
        '''
        # find if current position is correct solution
        # check_solution(block_position_list)
        return
    
    # print(start_point)
    new_lazor_points, new_lazor_pass_grid = cal_lazor(start_point)
    # print('lazor_points', lazor_points)
    # print('lazor_pass_grid', lazor_pass_grid)
    '''
    lazor_points [[5, 0, -1, 1], [4, 1, -1, 1], [3, 2, -1, 1], [2, 3, -1, 1], [1, 4, -1, 1], [0, 5, -1, 1]]
    lazor_pass_grid [[3, 3], [3, 1], [1, 5], [1, 3]]
    '''
    for i, lazor_point in enumerate(new_lazor_points):
        # print(lazor_point) # [5, 0, -1, 1]
        block_position = []
        if lazor_point[0] % 2 == 0:
            block_position.append(lazor_point[0] + lazor_point[2])
            # block_position[0] += lazor_point[2]
        else:
            block_position.append(lazor_point[0])
        if lazor_point[1] % 2 == 0:
            block_position.append(lazor_point[1] + lazor_point[3])
            # block_position[1] += lazor_point[3]
        else:
            block_position.append(lazor_point[1])
        
        # continue
        if not in_grid(block_position[0], block_position[1]):
            continue
        
        # if len(lazor_points) > 0 and lazor_point == lazor_points[-1]:
        #     continue
        
        block_position_list.append(block_position)
        # print(block_position) # [5, 1]
        new_reflect_point = cal_reflect_start(lazor_point)
        # print(new_reflect_point)
        # print(lazor_points)
        # lazor_points.extend(new_lazor_points[:i+1])
        # lazor_pass_grid.extend(new_lazor_pass_grid[:i+1])
        # print('======',temp)

        # print('block_position_list', block_position_list)
        # print('lazor_points', lazor_points + new_lazor_points[:i+1])
        # print('lazor_pass_grid', lazor_pass_grid  + new_lazor_pass_grid[:i+1])
        # print('----------------------------------------------')

        # check if block_position_list can solve the problem 
        if check_solution(block_position_list, lazor_points + new_lazor_points[:i+1], lazor_pass_grid+ new_lazor_pass_grid[:i+1]):
            # find = True
            print('block_position_list=======', block_position_list)
            return

        # lazor_points = list(set(lazor_points))
        # lazor_pass_grid = list(set(lazor_pass_grid))

        find_block_position(blocks, index+1, new_reflect_point, block_position_list, lazor_points + new_lazor_points[:i+1], lazor_pass_grid + new_lazor_pass_grid[:i+1])
        # trackback
        block_position_list.pop()
        # length_points = len(lazor_points) - (i+1)
        # lazor_points = lazor_points[:length_points -1]
        # length_pass = len(lazor_pass_grid) - (i+1)
        # lazor_pass_grid = lazor_pass_grid[:length_pass-1]
        # print('```````````````````````````````````````````')
        # print('lazor_points', lazor_points)
        # print('lazor_pass_grid', lazor_pass_grid)
        # print('```````````````````````````````````````````')


def find_solution(file):
    
    # read the file
    gird, blocks_type, start_points, intersect_points_1 = read_bff(file)
    global intersect_points
    intersect_points = intersect_points_1
    # find permutations of blocks 
    blocks_list = get_blocks_list(blocks_type)

    # initialize the range of x and y 
    global max_x, max_y
    max_x = len(gird[0]) * 2
    max_y = len(gird) * 2

    # permutation_blocks = set(itertools.permutations(blocks_list))
    # print(permutation_blocks)

    # print(blocks_list)
    # find all possible positions of blocks 
    # for blocks in blocks_list:
    find_block_position(blocks_list, 0, start_points[0], [], [], [])

    # then calculate if this position is a possible solution

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
    find_solution('easy.bff')
    # pos1 = [[3, 1], [5, 3]]
    # check_solution(pos1)
    # cal_lazor([5, 0, -1, 1])
    # print(intersect_points)
