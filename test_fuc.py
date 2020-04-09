def recur(i):
    if i == 0:
        return 0
    if i == 1:
        return 1
    return recur(i-1) + recur(i -2)

print(recur(10))