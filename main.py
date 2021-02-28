from scheduler import Scheduler
from world import World

housing = {
    "in": {'R1': 5, 'R2': 1, 'R3': 5, 'R18': 3},
    "out": {'R1': 5, 'R19': 1, "R19'": 1}
}
alloys = {
    "in": {'R1': 1, 'R2': 2},
    "out": {'R1': 1, "R18": 1, "R18'": 5}
}
electronics = {
    "in": {'R1': 1, 'R2': 3, 'R18': 2},
    "out": {'R1': 1, "R20": 2, "R20'": 1}
}
transform_templates = [housing, alloys, electronics]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)

scheduler = Scheduler(world)
maxDepth = 10
maxSize = 30
schedule = scheduler.search(maxDepth, maxSize)
for step in schedule:
    action = step[0]
    eu = -step[1]
    print(action, "EU: ", eu)

