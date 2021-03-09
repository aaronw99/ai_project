from transfer import Transfer
from world import World
from templates import housing, alloys, electronics, farms, factories

country1 = "Atlantis"
country2 = "Brobdingnag"

transform_templates = [housing, alloys, electronics, farms, factories]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)
startState = world.getStartState()
print(startState)
startstate = world.getStartState()

transfer = Transfer(startState, country1, country2, ("R1", 5))
print(transfer.toString())
newstate = transfer.execute()
print(newstate)
