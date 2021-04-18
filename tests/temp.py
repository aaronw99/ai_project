import sys
sys.path.append('../')

from world import World
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant

transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
myCountry = "Atlantis"

initialStatePath = "../test_initial_states/initial_state_5.xlsx"
resourceWeightPath = "../resources.xlsx"

world = World(myCountry, transform_templates, initialStatePath, resourceWeightPath)
startState = world.getStartState()
for country in startState:
    print(startState[country]['R1'])
    print()