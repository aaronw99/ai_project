import sys
sys.path.append('../')

from world import World
from templates import housing, alloys, electronics, farms, factories
from mine import Mine

country1 = "Atlantis"

transform_templates = [housing, alloys, electronics, farms, factories]
myCountry = "Atlantis"
world = World(myCountry, transform_templates, '/Users/aaronwong/Desktop/code/ai_project/test_initial_states/initial_state_2.xlsx', 'resources.xlsx')
startState = world.getStartState()
print(startState)
startstate = world.getStartState

mine = Mine(startState, country1, 'R6', difficulty=2)
print(mine.toString())
newstate = mine.execute()
print(newstate)
