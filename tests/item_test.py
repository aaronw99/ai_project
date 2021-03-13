import sys
sys.path.append('../')
from scheduler import Item

item1 = Item(1, {}, [1, 2])
item2 = Item(2, {}, [1, 2, 3])
item3 = Item(1, {}, [3, 4])
item4 = Item(1, {}, [0])

# this should be true -> smaller utility is smaller
print(item1 < item2)
# this should be false -> equal utility and equal action is same
print(item1 < item3)
# this should be true
print(item1 <= item3)
# this should be true -> if utility is same, less action is greater
print(item1 < item4)


