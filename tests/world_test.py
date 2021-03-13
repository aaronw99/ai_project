import sys
sys.path.append('../')

from world import World
from transfer import Transfer
from transform import Transform
from templates import housing, alloys, electronics, farms, factories
import utils

transform_templates = [housing, alloys, electronics, farms, factories]
myCountry = "Atlantis"
initialStatePath = "../test_initial_states/initial_state_5.xlsx"
resourceWeightPath = "../resources.xlsx"
world = World(myCountry, transform_templates, initialStatePath, resourceWeightPath)
startState = world.getStartState()
print("start state: ", startState)

print("sq: ", utils.calculate_state_quality(startState, myCountry, "../resources.xlsx"))

print("max multiplier: ", utils.calculate_transform_max_multiplier(startState[myCountry], factories))

# =============================================================================
# transform = Transform(startState, myCountry, factories, 1)
# newState = transform.execute()
# print(newState)
# 
# print(utils.calculate_state_quality(newState, myCountry, "../resources.xlsx"))
# =============================================================================

# =============================================================================
# trades = generate_trades(startState, myCountry)
# print(len(trades))
# for trade in trades:
#     print(trade.toString())
# =============================================================================
    
# =============================================================================
# transfer = Transfer(startState, myCountry, "Erewhon", ("R6", 1270))
# newState = transfer.execute()
# print("start: ", startState, "sq:",
#       calculate_state_quality(startState, myCountry))
# print("end: ", newState, "sq:", calculate_state_quality(newState, myCountry))
# print("eu:", world.getExpectedUtility(newState, 1))
# 
# nextState = world.getSuccessors(startState)
# print(len(nextState))
# print(nextState[1][0])
# print(nextState[1][1])
# print(nextState)
# for state in nextState:
#     print(state[1], ": ", world.getExpectedUtility(state[0], 1))
# =============================================================================
