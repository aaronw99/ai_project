from scheduler import Scheduler
from world import World
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber

transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)

scheduler = Scheduler(world)
maxDepth = 3
maxSize = 10
schedule = scheduler.search(maxDepth, maxSize)
print("Best Schedule: ")
for step in schedule:
    action = step[0]
    eu = step[1]
    print(action, "EU: ", eu)

#country: {R1: 100, R2: 500, R3: 200}
# transform = Transform(country, alloys, 1) 1-100
