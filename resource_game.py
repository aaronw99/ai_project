from immigration import Immigration
from immigration_nb import populations, models
from population_growth import PopulationGrowth
from random import randint, uniform
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
from thresholds import Thresholds
from time import sleep
from world import World

print("\nWelcome to the Resource Game! You represent Atlantis, the land of opportunity.\n")
sleep(2)
print("You will be playing against 3 other countries, controlled by the computer.\n")
sleep(2)
print("You will start with all your resource levels at 50%.\n")
sleep(2)
print("Your objective is to reach comfortable levels for all resources.\n")
sleep(2)
print("Every round, you will be given 3 turns. You can either a) mine new resources, " +
"b) transform your resources, or c) ask for resources from other countries. Keep " + 
"in mind that other countries can deny your request.\n")
sleep(4)
print("Then, each CPU country will give you two options: a) offer to send over " +
"immigrants or b) demand a resource.\n")
sleep(2)
print("If you hang below survival with any resource for longer than 3 rounds, you will lose.")
sleep(2)
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

finished = False
year = 1
while not finished:
    sleep(1)
    t = Thresholds(state, myCountry)
    
    print("\nYour country currently has", t.get_population(), "million people.")

    sleep(1)
    print("\nYour resource levels:")
    print(t.get_levels())

    sleep(1)
    print("\nYour resource percentages:")
    print(t.get_percentages())

    sleep(1)
    print("\nYOUR TURN (3 rounds)")
    
    for i in range(1,4):
        sleep(1)
        print("\nRound",i,"- your three options:")
        print("\t1. Mine")
        print("\t2. Transform")
        print("\t3. Request")
        choice = input("Enter your choice here: ")

        if choice == "1":
            print("Mine operation here")
        elif choice == "2":
            print("Transform operation here")
        elif choice == "3":
            print("Request operation here")
        else: 
            print("Please enter 1, 2, or 3")
    
    sleep(1)
    print("\nOPPONENTS TURN")
    for country in country_map:

        imm = Immigration(state=state, country_from=country, 
            country_to="Atlantis", cf_model=country_map[country], 
            cycle=year, models=models)
        multiplier = uniform(0.75,1.25)
        imm.randomize_level(multiplier,0)
        imm_level = imm.get_level()

        t = Thresholds(state, country)
        req = t.get_request(t.get_most_needed(), year * 0.05)

        sleep(1)
        print("\nAs",country,"we give you 2 options: ")
        print("\t1. Accept", imm_level, "new people into your country")
        print("\t2. Give us", req, "units of", t.get_most_needed())
        choice = input("Put your choice here: ")
        if choice == "1":
            state = imm.execute()
            print("Immigration has been executed.")
        elif choice == "2":
            print("Transfer operation here")

    growth = PopulationGrowth(state, uniform(1.01,1.5))
    state = growth.execute()

    year += 1
