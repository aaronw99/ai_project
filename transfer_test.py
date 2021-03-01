from  transfer import Transfer
from world import World

country1 = "Atlantis"
country2 = "Brobdingnag"

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
print(startState)
startstate = world.getStartState

transfer = Transfer(startState, country1, country2, ("R1", 5))
print(transfer.toString())
newstate = transfer.execute()
print(newstate)