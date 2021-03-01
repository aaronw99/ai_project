from world import World
from transfer import Transfer
from world import calculate_state_quality

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
startState = world.getStartState()
#print(startState)
transfer = Transfer(startState, myCountry, "Erewhon", ("R6", 1270))
newState = transfer.execute()
print("start: ", startState, "sq:", calculate_state_quality(startState, myCountry))
print("end: ", newState, "sq:", calculate_state_quality(newState, myCountry))
print("eu:", world.getExpectedUtility(newState, 1))

#nextState = world.getSuccessors(startState)
#print(len(nextState))
#print(nextState[1][0])
#print(nextState[1][1])
#print(nextState)
#for state in nextState:
#    print(state[1], ": ", world.getExpectedUtility(state[0], 1))