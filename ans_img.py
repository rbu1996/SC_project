import numpy as np
from PIL import Image

grid_map = [[[1, 1, 'o'], [3, 1, 'B'], [5, 1, 'o']],
            [[1, 3, 'o'], [3, 3, 'o'], [5, 3, 'o']],
            [[1, 5, 'o'], [3, 5, 'o'], [5, 5, 'o']]]

position = {(1, 1): 'A', (5, 1): 'A', (1, 5): 'A', (3, 5): 'C'}

# print(grid_map)
# print(position)
ans_list = []
max_x = 6

max_y = 6
blockSize = 50
frameSize = 5
x = int(max_x / 2)
y = int(max_y / 2)
print(x, y)
for i, row in enumerate(grid_map):
    # print(i, row)
    for j, column in enumerate(row):
        # print(j, column)
        map_key = (column[0], column[1])
        map_value = column[2]
        # print('map_key', map_key)
        # print('map_value', map_value)
        for key, values in position.items():
            # print('key', key)
            # print('values', values)
            if key == map_key:
                # column.pop()
                # column.append(values)
                column[2] = values
        ans_list.append(column[2])
        # print('col',column[2])
        # print(i)
        # ans_map[i].append(column[2])

print(grid_map)
print(position)
print(ans_list)

ans_map = np.array(ans_list).reshape(x, y)
print(ans_map)

colors = {'o': (192, 192, 192),
          'x': (105, 105, 105),
          'A': (245, 245, 245),
          'B': (0, 0, 0),
          'C': (128, 128, 128),
          'frame': (105, 105, 105)
          }
dim_x = x * (blockSize + frameSize) + frameSize
dim_y = y * (blockSize + frameSize) + frameSize
print(dim_x, dim_y)
''
img = Image.new("RGB", (dim_x, dim_y), color=colors['frame'])
'''
for i in range(ans_map):
    for j in range(ans_map):
        img.putpixel((x + i, y + j), colors[])
        print(i,j)
'''


for i, ans_row in enumerate(ans_map):
    # print(i, ans_row)
    for j, ans in enumerate(ans_row):
        print(ans)
        print(colors[ans])
        color = colors[ans]
        for x in range(blockSize):
            for y in range(blockSize):
                img.putpixel((frameSize + (frameSize + blockSize) * j + x, frameSize + (frameSize + blockSize) * i + y),
                             color
                             )

img.show()
img.save('ans_map.png')
