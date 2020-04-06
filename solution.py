def read_bff(file):
    f = open(file)
    line = f.readline()

    gird = []
    blocks = []
    start_points = []
    intersect_points = []
    while line:
        # grid
        if line == 'GRID START\n':
            print('#')
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
            print(line)
        
        # lazor start point
        while line.startswith('L'):
            line = line.split()
            start_points.append([int(line[i]) for i in range(1, len(line))])
            line = f.readline()
        
        # intersect points 
        while line.startswith('P'):
            line = line.split()
            intersect_points.append([int(line[i]) for i in range(1, len(line))])
            line = f.readline()
        
        line = f.readline()
    f.close()
    print('gird', gird)
    print('blocks', blocks)
    print('start_points', start_points)
    print('intersect_points', intersect_points)
    return gird, blocks, start_points, intersect_points

def find_solution(file):
    gird, blocks, start_points, intersect_points = read_bff(file)
    

if __name__ == "__main__":
    read_bff('mad_1.bff')
    # find_solution('mad_1.bff')