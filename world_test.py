from world import World
from transfer import Transfer
from world import calculate_state_quality
from templates import housing, alloys, electronics

transform_templates = [housing, alloys, electronics]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)
startState = world.getStartState()
# print(startState)
transfer = Transfer(startState, myCountry, "Erewhon", ("R6", 1270))
newState = transfer.execute()
print("start: ", startState, "sq:",
      calculate_state_quality(startState, myCountry))
print("end: ", newState, "sq:", calculate_state_quality(newState, myCountry))
print("eu:", world.getExpectedUtility(newState, 1))

#nextState = world.getSuccessors(startState)
# print(len(nextState))
# print(nextState[1][0])
# print(nextState[1][1])
# print(nextState)
# for state in nextState:
#    print(state[1], ": ", world.getExpectedUtility(state[0], 1))
