# cd Software\ Carpentry/LazorProject/SC_project/


# a = []
# a.append(1)
# a.append(2)
# for i in a:
#     if i == 1:
#         a.append(5)
#     print(i)

# while True:
#     print('===')

# dir = {1: 'a', 2: 'b'}
# dir2 = {5:'d'}
# print(dict(**dir, **dir2))

# class test():
#     def __init__(self, index):
#         self.index = index
        
#     def p(self, a, b):
#         print(self.index)
#         if self.index == 5:
#             print('===')
#         print(a)
#         print(b)
#         print(hello(100))

# def hello(i):
#     return i

# tt = test(1)
# tt.p(2, 3)
t = (1,2,3,4)
print(t[1:])



'''
import itertools

blocks = ['A', 'C']
grids = {(1, 1), (1, 2), \
    (2, 1), (2, 2), \
    (3, 1), (3, 2) }

perm_b = itertools.permutations(blocks, 2)
# print(set(perm_b)) # 12

comb_g = itertools.combinations(grids, 2)
# print(list(comb_g)) # 15
# print(len(list(comb_g)))

perm = [list(set(perm_b)), list(comb_g)]
res = itertools.product(*perm)
count = 0
for r in res:
    print(r)
    count += 1

print(count) # 180
'''


'''
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (2, 1), (2, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (2, 1), (3, 1)))
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (2, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (2, 2), (3, 1)))
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (2, 2), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (1, 2), (3, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (2, 1), (2, 2), (3, 1)))
(('B', 'A', 'C', 'B'), ((1, 1), (2, 1), (2, 2), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (2, 1), (3, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 1), (2, 2), (3, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 2), (2, 1), (2, 2), (3, 1)))
(('B', 'A', 'C', 'B'), ((1, 2), (2, 1), (2, 2), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 2), (2, 1), (3, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((1, 2), (2, 2), (3, 1), (3, 2)))
(('B', 'A', 'C', 'B'), ((2, 1), (2, 2), (3, 1), (3, 2)))
(('B', 'C', 'A', 'B'), ((1, 1), (1, 2), (2, 1), (2, 2)))
(('B', 'C', 'A', 'B'), ((1, 1), (1, 2), (2, 1), (3, 1)))
(('B', 'C', 'A', 'B'), ((1, 1), (1, 2), (2, 1), (3, 2)))
(('B', 'C', 'A', 'B'), ((1, 1), (1, 2), (2, 2), (3, 1)))
'''


'''
block = ['A', 'B', 'B', 'C']
grid = [(1, 1), (1, 2), (1, 3), \
    (2, 1), (1, 2), (2, 3), \
    (3, 1), (3, 2), (3, 3), ]
perm = [block, grid]
res = itertools.product(*perm)
for r in res:
    print(r)
    print(type(r))
print(res)
'''

'''
class info:
    def __init__(self, x, y, z):
        self.block_position_list = x
        self.lazor_points = y
        self.lazor_pass_grid = z

dir = {}
info1 = info([1,2,3], 2, (0,1,0))
info2 = info([1,2], 8, (1,1,0))

dir[(0,1,0)] = info1
dir[(1,1,0)] = info2

print(dir)

for key, val in dir.items():
    print(key)
    print(val.block_position_list, val.lazor_points, val.lazor_pass_grid)
'''


'''
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
print(root.right.val)
'''


