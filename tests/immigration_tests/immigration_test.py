import sys
sys.path.append('../')
from immigration import Immigration
from immigration_nb import models 
from world import World
from templates import housing, alloys, electronics, farms, factories

transform_templates = [housing, alloys, electronics, farms, factories]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)
startState = world.getStartState()

imm1 = Immigration(state = startState, country_from="Brobdingnag", cf_model="Libya", cycle=-5, models=models)
print(imm1.toString())
