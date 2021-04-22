from immigration import Immigration
from immigration_nb import populations, models
from population_growth import PopulationGrowth
from random import randint, uniform
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
from world import World

print("Welcome to the Resource Game! You represent Atlantis, the land of opportunity."+
"\n\nHere are your instructions:\n\n" +
"You will start with 50% resource levels.\n\n" + 
"Every round, you will be given 3 opportunties to build new resources " +
"or ask for resources from other countries.\n\nThen, each country will " +
"offer to send over immigrants or demand a resource.\n\nYour objective " +
"is to reach comfortable levels for all resources.\n\nIf you hang below " +
"survival for any resource for longer than 3 rounds, you will lose.\n\n" +
"Good luck and have fun!")

transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
myCountry = "Atlantis"

initialStatePath = "test_initial_states/game_initial_state.xlsx"
resourceWeightPath = "resources.xlsx"

world = World(myCountry, transform_templates, initialStatePath, resourceWeightPath)
state = world.getStartState()

# dictionary that maps virtual country to real country from dataset
country_map = {}
virtual_countries = ["Brobdingnag", "Carpania", "Dinotopia", "Erewhon"]

# generate a list of 16 of the real countries used by the immigration dataset
real_countries = list(populations.keys())

# set of random indices to map virtual countries with real countries
rand_indices = set()
while len(rand_indices) < 4:
    rand_indices.add(randint(0,len(virtual_countries) - 1))

# assign real country to each virtual country
for i,num in enumerate(rand_indices):
    country_map[virtual_countries[i]] = real_countries[num]

'''
Todo:
1. Create skeleton of game with only immigrations -- done
2. Add Threshold class to constantly check thresholds
3. Have other countries randomly encompass states
4. Add slides
'''
finished = False
year = 1
while not finished:
    
    for country in country_map:
        imm = Immigration(state=state, country_from=country, 
            country_to="Atlantis", cf_model=country_map[country], 
            cycle=year, models=models)
        multiplier = uniform(0.75,1.25)
        imm.randomizeLevel(multiplier,0.1)
        print(imm)
        state = imm.execute()

    growth = PopulationGrowth(state, uniform(1.01,1.5))
    state = growth.execute()
    print(state)
    
    quit = input("Quit? ")
    if quit.lower() == 'yes':
        finished = True
    
    year += 1