from copy import deepcopy
lst = [[1, 2, 3], [3, 4, 5]]
a = deepcopy(lst)
a.append(5)
print(a, lst)
print()