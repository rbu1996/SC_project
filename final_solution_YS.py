import itertools
import numpy as np
from PIL import Image
import time


class Block():
    def __init__(self, block_type):
        self.block_type = block_type

    def lazor_in_block(self, nei_block):
        if nei_block == 'A' or nei_block == 'B':
            return False
        return True

    def block_reflect_lazor(self, lazor_points, copy_goal_points, new_reflect_point, intersect_point, start_points):
        pass_goal(lazor_points, copy_goal_points, new_reflect_point)

        if self.block_type == 'A':
            return True
        elif self.block_type == 'B':
            return False
        else:
            new_x = intersect_point[0] + intersect_point[2]
            new_y = intersect_point[1] + intersect_point[3]
            new_start_point = (new_x, new_y) + intersect_point[2:]
            pass_goal(lazor_points, copy_goal_points, new_start_point)
            if new_start_point not in start_points:
                start_points.append(new_start_point)
            return True


'''
YS:
我加了个 grid_map最为return, 应该是3Dlist, like this:
    [[[1, 1, 'x'], [3, 1, 'o'], [5, 1, 'o']], 
    [[1, 3, 'o'], [3, 3, 'o'], [5, 3, 'o']], 
    [[1, 5, 'o'], [3, 5, 'o'], [5, 5, 'x']]]
'''


def read_bff(file):
    f = open(file)
    line = f.readline()

    grid = set()
    grid_map = []
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
                max_x = max(max_x, len(temp))
                row = []
                for x, block in enumerate(temp):
                    row.append([(x + 1) * 2 - 1, y, block])
                    if block == 'o':
                        grid.add(((x + 1) * 2 - 1, y))
                    # fixed block
                    if block == 'A' or block == 'B' or block == 'C':
                        fixed_block[((x + 1) * 2 - 1, y)] = Block(block)
                y += 2
                line = f.readline()
                grid_map.append(row)
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
            intersect_points.add((int(line[1]), int(line[2])))
            line = f.readline()

        line = f.readline()
    f.close()
    print(grid_map)
    print(grid)
    return grid_map, grid, blocks, start_points, intersect_points, fixed_block, max_x * 2, max_y - 1


def get_blocks_list(blocks):
    block_list = []
    for block in blocks:
        for i in range(block[1]):
            block_list.append(block[0])
    print(block_list)
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


def cal_lazor(point, grid):
    lazor_points = []
    lazor_pass_grid = set()
    x = point[0]
    dx = point[2]
    y = point[1]
    dy = point[3]
    while in_grid(x, y):
        lazor_points.append((x, y, dx, dy))
        if x % 2 == 1:
            if (x, y + dy) in grid:
                lazor_pass_grid.add((x, y + dy))
        if x % 2 == 0:
            if (x + dx, y) in grid:
                lazor_pass_grid.add((x + dx, y))
        x += dx
        y += dy
    return lazor_points, lazor_pass_grid


def get_intersect_point(intersect_grid, lazor_points, start_point):
    possible_intersect_point = set()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for int_grid in intersect_grid:
        for i in range(4):
            possible_intersect_point.add(
                (int_grid[0] + dx[i], int_grid[1] + dy[i]) + start_point[2:])
    for point in lazor_points:
        if point in possible_intersect_point:
            return point


def get_intersect_grid(intersect_point):
    grid = (0, 0)
    x = intersect_point[0]
    y = intersect_point[1]
    dx = intersect_point[2]
    dy = intersect_point[3]
    if x % 2 == 1:
        grid = (x, y + dy)
    if x % 2 == 0:
        grid = (x + dx, y)
    return grid


def cal_reflect_start(point):
    dx = point[2]
    dy = point[3]
    if point[0] % 2 == 0:
        dx *= -1
    if point[1] % 2 == 0:
        dy *= -1
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
    copy_goal_points = goal_points.copy()
    copy_start_points = start_points.copy()

    # 用end_lazor 来表示光线的最末尾。如果末尾超过了grid的范围，那这个光线的路程结束了
    for start_point in copy_start_points:
        while True:
            lazor_points, lazor_pass_grid = cal_lazor(start_point, grid)
            intersect_grids = lazor_pass_grid & set(position.keys())
            if len(intersect_grids) == 0:
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                break
            else:
                intersect_point = get_intersect_point(
                    intersect_grids, lazor_points, start_point)
                intersect_grid = get_intersect_grid(intersect_point)
                new_reflect_point = cal_reflect_start(intersect_point)
                if intersect_point[:2] == start_point[:2]:
                    nei_x = intersect_point[0] * 2 - intersect_grid[0]
                    nei_y = intersect_point[1] * 2 - intersect_grid[1]
                    nei_grid = (nei_x, nei_y)

                    if nei_grid in position.keys():
                        pos = position[nei_grid]
                        if pos.lazor_in_block(pos.block_type):
                            new_temp = (
                                new_reflect_point[0] + new_reflect_point[2], new_reflect_point[1] + new_reflect_point[3])
                            copy_start_points.append(
                                new_temp + new_reflect_point[2:])
                        else:
                            break

                if position[intersect_grid].block_reflect_lazor(lazor_points, copy_goal_points, new_reflect_point, intersect_point, copy_start_points):
                    start_point = new_reflect_point
                else:
                    break

    if len(copy_goal_points) == 0:
        print('Find the solution!')
        return True
    return False


max_x = 0
max_y = 0


'''
YS:
this function gets the map of the solution，like this:
[['x' 'o' 'o']
 ['o' 'B' 'o']
 ['B' 'B' 'x']]
the output sol_map is a 2D list
'''


def get_map(grid_map, sol_position, max_x, max_y):
    sol_list = []
    x = int(max_x / 2)
    y = int(max_y / 2)

    for i, row in enumerate(grid_map):
        for j, column in enumerate(row):
            map_key = (column[0], column[1])
            for key, values in sol_position.items():
                if key == map_key:
                    column[2] = values
            sol_list.append(column[2])

    sol_map = np.array(sol_list).reshape(y, x)
    return sol_map


'''
YS:
this function outputs an image of the solution
'''


def output_img(filename, sol_map, max_x, max_y, blockSize, frameSize):

    x = int(max_x / 2)
    y = int(max_y / 2)

    colors = {'o': (192, 192, 192),
              'x': (105, 105, 105),
              'A': (245, 245, 245),
              'B': (0, 0, 0),
              'C': (128, 128, 128),
              'frame': (105, 105, 105)
              }
    dim_x = x * (blockSize + frameSize) + frameSize
    dim_y = y * (blockSize + frameSize) + frameSize
    img = Image.new("RGB", (dim_x, dim_y), color=colors['frame'])
    for n, sol_row in enumerate(sol_map):
        for m, sol in enumerate(sol_row):
            color = colors[sol]
            for i in range(blockSize):
                for j in range(blockSize):
                    pxl_x = frameSize + (frameSize + blockSize) * m + i
                    pxl_y = frameSize + (frameSize + blockSize) * n + j
                    img.putpixel((pxl_x, pxl_y), color)

    img.show()
    img.save('%s_sol.png' % filename)


'''
YS:
this function outputs a txt file of the solution
'''


def output_txt(filename, sol_map):
    with open('%s_sol.txt' % filename, 'w') as f:
        for row in sol_map:
            for item in row:
                f.write('%s ' % item)
            f.write('\n')


def find_solution(file, output_image, output_file):
    global max_x, max_y
    # read the file
    grid_map, grid, blocks, start_points, intersect_points, fixed_block, max_x, max_y = read_bff(
        file)
    if ".bff" in file:
        filename = file.split(".bff")[0]

    # find all possible combination between blocks and its position in grid
    all_poss_posi = find_all_positions(blocks, grid)

    for temp in all_poss_posi:
        block_position = {}
        sol_position = {}
        for i, index in enumerate(temp[1]):
            block_position[index] = Block(temp[0][i])
        position = block_position.copy()
        position.update(fixed_block)
        if check_position(position, grid, start_points, intersect_points):
            for index, clas in block_position.items():
                # print(index, clas.block_type)
                sol_position[index] = clas.block_type

            sol_map = get_map(grid_map, sol_position, max_x, max_y)
            # output image
            if output_image is True:
                output_img(filename, sol_map, max_x, max_y,
                           blockSize=50, frameSize=5)
            # output txt
            if output_file is True:
                output_txt(filename, sol_map)

            return


if __name__ == "__main__":
    start_time = time.time()
    find_solution('dark_1.bff', output_image=False, output_file=True)
    print("--- %s seconds ---" % (time.time() - start_time))

    # {(7, 3): 'A', (1, 5): 'A', (5, 1): 'C'}
