import itertools
import copy

class Solution_Info:
    def __init__(self, x, y, z):
        self.block_position_list = x
        self.lazor_points = y
        self.lazor_pass_grid = z
        

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


intersect_points = {}
intersect_info = {}

def check_solution(block_position_list, lazor_points, lazor_pass_grid):
    
    if len(block_position_list)<= 0 or len(lazor_points) <= 0 or len(lazor_pass_grid) <= 0:
        return False

    # print(lazor_points[-1])
    last_lazor_points, last_lazor_pass_grid = cal_lazor(cal_reflect_start(lazor_points[-1]))
    if lazor_points[-1] == (4, 5, 1, 1):
        print('===')
        print(lazor_points)
        print(last_lazor_points)
    
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

# 只能解决一个start_point
def find_block_position(blocks, index, start_point, block_position_list, lazor_points, lazor_pass_grid):

    print('----------------------------')
    print('start_point', start_point)
    print('block_position_list', block_position_list)
    print('lazor_points', lazor_points)
    print('lazor_pass_grid', lazor_pass_grid)
    print('----------------------------')

    if check_solution(block_position_list, lazor_points , lazor_pass_grid):
        print('block_position_list=======', block_position_list)
        # return

    if index >= len(blocks):
        return
    
    '''
    gird [[[1, 1, 'o'], [3, 1, 'o'], [5, 1, 'o']], [[1, 3, 'o'], [3, 3, 'o'], [5, 3, 'o']], [[1, 5, 'o'], [3, 5, 'o'], [5, 5, 'o']], [[1, 7, 'o'], [3, 7, 'o'], [5, 7, 'o']]]
    blocks [['A', 3]]
    start_points [[1, 5, 1, 1], [1, 6, 1, -1]]
    intersect_points {(0, 5), (6, 5)}
    blocks_list ['A', 'A', 'A']
    '''

    # all start_points 

    new_lazor_points, new_lazor_pass_grid = cal_lazor(start_point)
    
    for i, lazor_point in enumerate(new_lazor_points):
        block_position = []
        if lazor_point[0] % 2 == 0:
            block_position.append(lazor_point[0] + lazor_point[2])
        else:
            block_position.append(lazor_point[0])
        if lazor_point[1] % 2 == 0:
            block_position.append(lazor_point[1] + lazor_point[3])
        else:
            block_position.append(lazor_point[1])
        
        # continue
        if not in_grid(block_position[0], block_position[1]):
            continue
        
        block_position_list.append(block_position)
        new_reflect_point = cal_reflect_start(lazor_point)
        
        find_block_position(blocks, index+1, new_reflect_point, block_position_list, lazor_points + new_lazor_points[:i+1], lazor_pass_grid + new_lazor_pass_grid[:i+1])
        # trackback
        block_position_list.pop()


def find_solution(file):
    
    # read the file
    gird, blocks_type, start_points, intersect_points_1 = read_bff(file)
    global intersect_points, intersect_info
    intersect_points = intersect_points_1
    intersect_info = {}
    # find permutations of blocks 
    blocks_list = get_blocks_list(blocks_type)

    # initialize the range of x and y 
    global max_x, max_y
    max_x = len(gird[0]) * 2
    max_y = len(gird) * 2

    
    for start_point in start_points:
        find_block_position(blocks_list, 0, start_point, [], [], [])



if __name__ == "__main__":
    # read_bff('mad_1.bff')
    find_solution('easy.bff')
    # pos1 = [[3, 1], [5, 3]]
    # check_solution(pos1)
    # cal_lazor([5, 0, -1, 1])
    # print(intersect_points)

