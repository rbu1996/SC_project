import itertools
import numpy as np
from PIL import Image
import time


class Block():
    def __init__(self, block_type):
        self.block_type = block_type

    def lazor_end(self, nei_block):
        """
        This is to find if the block is A or B, because lazor no longer moves forward when encounters A and B.

        **parameter**
            nei_block: *str*
                Type of the block in str format

        **output**
            True/ False: *boolean*
        """
        if nei_block == 'A' or nei_block == 'B':
            return True
        return False

    def block_reflect_lazor(self, lazor_points, copy_goal_points, new_reflect_point, intersect_point,
                            start_points):
        """
        This is to find if the block is A, B, or else (C). When it is A or B, lazor is reflect. When it is C, lazor can go
        through the block.

        **parameter**
            lazor_points: *list*
                List of points the lazor passes through
            copy_goal_points: *set*
                Copy of targets the lazor should pass through as solution
            new_reflect_point: *tuple*
                Points where lazor reflects and its new direction
            start_points: *list*
                Start points of lazors, and their direction
            intersect_points: *set*
                Individual points targets lazor need to hit

        **output**
            True/ False: *boolean*
        """

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
    """
    This is to read the input file, which is the game layout.
    The function defines the game panel into a grid assignment and
    defines the length of the grid in x and y direction (size).

    **parameters**
        file: *str*
            The .bff file which is the layout of the game.

    **returns**
        grid_map: *3D list*
            Grid location and if it is available for blocks
        grid: *set*
            locations of available grids.
        blocks: *list*
            Tpye A, B, or C of blocks
        start_points: *list*
            start points of lazors, and their direction
        intersect_points: *set*
            Targets lazor need to hit
        fixed_block: *dict*
            location and type of fixed A, B, or C blocks
        max_x, max_y: *int*
            maximum values of points (where the boundary of grid is)
    """

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
                    if block == 'o' or block == 'A' or block == 'B' or block == 'C':
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
    # print('grid', grid)
    # print('blocks', blocks)
    # print('start_points', start_points)
    # print('intersect_points', intersect_points)
    # print('max_x', max_x * 2)
    # print('max_y', max_y - 1)
    # print('fixed_block', fixed_block)
    # print('----file-----')
    return grid_map, grid, blocks, start_points, intersect_points, fixed_block, max_x * 2, max_y - 1


def find_all_positions(blocks, grid):
    """
    This function is to list out the combos of all the blocks and grids. 
    By narrowing the range down, we can later find out which block in which grid later which solve the game.

    **parameters**
        blocks: *list*
            Type of the blocks
        grid: *set*
            Grid points which are available

    **output**
        res: *intertools.prouduct*
            block types + grid
    """

    perm_blocks = itertools.permutations(blocks, len(blocks))
    comb_grid = itertools.combinations(grid, len(blocks))
    temp = [list(set(perm_blocks)), list(comb_grid)]
    res = itertools.product(*temp)
    return res


def in_grid(x, y):
    """
    This is to verify if the x and y are inside the grid area.

    **parameters**
        x, y: *int*
            location of a point

    **output**
        True/False: *boolean*
    """

    if x >= 0 and x <= max_x and y >= 0 and y <= max_y:
        return True
    return False


def cal_lazor(point, grid):
    """
    This is to find the grids and points which the lazer(s) pass.
    For the points, it also finds the direction of lazor when passes.

    **parameters**
        point: *tuple*
            point and the lazor direction
        grid: *set*
            locations of available grid boxes

    **output**
        lazor_points: *list*
            Points the lazer passes by and the lazor direction
        lazor_pass_grid: *set*
            Grids the lazor passes by
    """

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


def get_intersect_point(intersect_grid, lazor_points, start_point):
    """
    This is to get points that the lazor could intersect during the process.

    **parameters**
        intersect_grid: *set*
            Grids that lazor intersects
        lazor_points: *list*
            Points that the lazor intersects and the lazor direction
        start_point: *tuple*
            Where the lazor starts. It can be where the lazor is reflected or refracted which generates
            a new start

    **output**
        point: *tuple*
            Points lazor intersects and the direction of lazor when intersects
    """

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
    """
    This is to get grids that the lazor needs to intersect for intersect_point.

    **parameters**
        intersect_points: *set*
            Targets lazor need to hit

    **output**
        grid: *tuple*
            Locations of grids that the lazor needs to intersect in order to reach the intersect_point
    """

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
    """
    Find the point and new direction when the lazor is reflect.

    **parameters**
        point: *tuple*
            Points lazor intersects and reflected by block A

    **output**
        *tuple*
            New assembled points where the lazor is reflected and the new direction
    """

    dx = point[2]
    dy = point[3]
    if point[0] % 2 == 0:
        dx *= -1
    if point[1] % 2 == 0:
        dy *= -1
    return (point[0], point[1], dx, dy)


def pass_goal(lazor_points, copy_goal_points, reflect_point):
    """
    This is to remove the goal points if the lazor passes through it.

    **parameters**
        lazor_points: *list*
            Points the lazer passes by and the lazor direction
        copy_goal_points: *set*
            Copy of targets the lazor should pass through as solution
        reflect_point: *tuple*
            Individual point where lazor reflects and its new direction

    **output**
        N/A
    """

    for lazor_point in lazor_points:
        point = lazor_point[:2]
        if point in copy_goal_points:
            copy_goal_points.remove(point)
        if point == reflect_point[:2]:
            break


def check_position(position, grid, start_points, goal_points):
    """
    This is to compare the points which lazor passes through with the locations of
    pre-defined targets.
    The program breaks when the lazor is either blocked or going out of the game layout.

    **parameters**
        position: *dict*
            Possible locations for blocks
        grid: *set*
            locations of available grids
        start_points: *list*
            Points where the lazor starts
        goal_points: *set*
            Targets lazor need to hit. Same thing of intersect_points

    **output**
        True/False: *boolean*
    """

    copy_goal_points = goal_points.copy()
    copy_start_points = start_points.copy()

    for start_point in copy_start_points:
        # print('-----------------')

        count = 0
        while True:
            # print('start_point', start_point)
            lazor_points, lazor_pass_grid = cal_lazor(start_point, grid)
            # print('start_point', start_point)
            intersect_grids = lazor_pass_grid & position.keys()
            # print('intersect_grid', intersect_grids)
            # print('lazor_points', lazor_points)
            # print('lazor_pass_grid', lazor_pass_grid)
            # print('intersect_grids', intersect_grids)
            # print(set(position.keys()))
            if len(intersect_grids) == 0:
                pass_goal(lazor_points, copy_goal_points, (-1, -1, -1, -1))
                break
            else:
                intersect_point = get_intersect_point(
                    intersect_grids, lazor_points, start_point)
                intersect_grid = get_intersect_grid(intersect_point)
                new_reflect_point = cal_reflect_start(intersect_point)
                # print('new_reflect_point', new_reflect_point)
                if intersect_point[:2] == start_point[:2]:
                    nei_x = intersect_point[0] * 2 - intersect_grid[0]
                    nei_y = intersect_point[1] * 2 - intersect_grid[1]
                    nei_grid = (nei_x, nei_y)

                    if nei_grid in position.keys():
                        # print(position[nei_grid].block_type)
                        # print(a)
                        pos = position[nei_grid]
                        if pos.lazor_end(pos.block_type):
                            break
                        else:
                            break
                            new_temp = (
                                new_reflect_point[0] + new_reflect_point[2],
                                new_reflect_point[1] + new_reflect_point[3])
                            copy_start_points.append(
                                new_temp + new_reflect_point[2:])

                if position[intersect_grid].block_reflect_lazor(
                        lazor_points,
                        copy_goal_points,
                        new_reflect_point,
                        intersect_point,
                        copy_start_points):
                    # print('++++++++++++++')
                    start_point = new_reflect_point
                else:
                    break

    if len(copy_goal_points) == 0:
        print('Find the solution!')
        return True
    return False


max_x = 0
max_y = 0


def get_map(grid_map, sol_position, max_x, max_y):
    """
    This is to get the output map of the solution to prepare for txt and img output.

    **parameter**
        grid_map: *list*
            Location and availability of grid
        sol_position: *dict*
            Locations of solved blocks
        max_x:*int*
            Largest number on spot in x
        max_y:*int*
            Largest number on spot in y

    **output**
        sol_map: *list*
            List of output map
    """

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


def output_img(filename, sol_map, max_x, max_y, blockSize, frameSize):
    """
    This is to generate the img of solution.

        **parameter**
        filename: *str*
            filename of the image
        sol_map: *list*
            list of output map
        max_x:*int*
            Largest number on spot in x
        max_y:*int*
            Largest number on spot in y
        blockSize: *int*
            How many pixels each block is comprised of
        frameSize: *int*
            How mang pixels each frame (width) is comprised of 

    **output**
        *image*
        """

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


def output_txt(filename, sol_map):
    """
    This is to generate the txt file to show the solution.

        **parameter**
        filename: *str*
            filename of the image
        sol_map: *list*
            list of output map

    **output**
        *txt file*
    """

    with open('%s_sol.txt' % filename, 'w') as f:
        for row in sol_map:
            for item in row:
                f.write('%s ' % item)
            f.write('\n')


def find_solution(file, output_image, output_file):
    """
    This is to find the solution of the lazor game.
    Find locations of grid blocks when the lazor passes all the targets.
    Output the img and txt files.

    **parameters**
        file: *str*
            The name of .bff file which is the layout of the game
    **output**
        filename: *str*
            New file name 
    """

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
        if len(position) != len(blocks) + len(fixed_block):
            continue
        if check_position(position, grid, start_points, intersect_points):
            # pring the coordinate of solution board
            print('Solution == ', [(key, val.block_type)
                                   for key, val in position.items()])
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
    find_solution('mad_1.bff', output_image=False, output_file=False)
    print("--- %s seconds ---" % (time.time() - start_time))
