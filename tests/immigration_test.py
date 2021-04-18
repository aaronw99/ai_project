import sys
sys.path.append('../')
from immigration import Immigration
from population_growth import PopulationGrowth
from immigration_nb import models 
from world import World
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant

from random import uniform

# added Canada.xlsx to tests directory as the file needs to be in the same directory

transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
myCountry = "Atlantis"

initialStatePath = "../test_initial_states/initial_state_5.xlsx"
resourceWeightPath = "../resources.xlsx"

world = World(myCountry, transform_templates, initialStatePath, resourceWeightPath)
startState = world.getStartState()


for i in range(1, 100):
    imm1 = Immigration(state=startState, country_from="Brobdingnag", country_to="Atlantis", cf_model="Libya", cycle=-i, models=models)
    multiplier = uniform(0.75,1.25)
    imm1.randomizeLevel(multiplier, 0.2)
    print(imm1.toString())
    state_after_imm = imm1.execute()
    growth = PopulationGrowth(state_after_imm, 1.5)
    newState = growth.execute()
    print(newState)
