from immigration import Immigration
from immigration_nb import populations, models
from player import Player
from population_growth import PopulationGrowth
from random import randint, uniform
from mine import Mine
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
from thresholds import Thresholds
from transfer import Transfer
from time import sleep
from world import World

# Introduction
print("\nWelcome to the Resource Game! You represent Atlantis, the land of opportunity.\n")
sleep(2)
print("You will be playing against 3 other countries, controlled by the computer.\n")
sleep(2)
print("You will start with all your resource levels at 50%.\n")
sleep(2)
print("Your objective is to reach 100% for all resources.\n")
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

# generate initial state
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
lives = 3

# main game loop
while not finished:
    sleep(1)
    t = Thresholds(state, myCountry)
    
    print("\nYour country currently has", t.get_population(), "million people.")

    sleep(1)
    print("\nYour resource levels:")
    print(t.get_resources())

    sleep(1)
    print("\nYour resource percentages:")
    print(t.get_percentages())

    sleep(1)
    print("\nYOUR TURN (3 rounds)")
    
    # Mining operations
    # NOTE: the video demo mentioned 3 options for your turn
    # For simplicity, we've kept it 1 mining option.
    for i in range(1,4):
        sleep(1)
        print(list(t.get_percentages().keys()))
        r = input("Select one of the above resources to mine ")
        while r not in t.get_percentages().keys():
            r = input("Please choose a valid resource to mine ")
        p = Player(myCountry)
        m = Mine(p, r)
        m.execute(state)
        print("Mine operation successful")
    
    t = Thresholds(state, myCountry)

    sleep(1)
    print("\nYour resource levels:")
    print(t.get_resources())

    sleep(1)
    print("\nYour resource percentages:")
    print(t.get_percentages())

    
    sleep(1)
    print("\nOPPONENTS TURN")

    # Each country gets a chance to make a request
    for country in country_map:

        # generate immigration request
        imm = Immigration(state=state, country_from=country, 
            country_to="Atlantis", cf_model=country_map[country], 
            cycle=year, models=models)
        multiplier = uniform(0.75,1.25)
        imm.randomize_level(multiplier,0)
        imm_level = imm.get_level()

        # generate resource request
        t = Thresholds(state, country)
        most_needed = t.get_most_needed()
        req = t.get_request(most_needed, year * 0.05)

        sleep(1)
        print("\nAs",country,"we give you 2 options: ")
        print("\t1. Accept", imm_level, "new people into your country")
        print("\t2. Give us", req, "units of", most_needed)

        choice = input("Put your choice here: ")
        while choice not in ["1", "2"]:
            choice = input("Please enter 1 or 2: ")
        if choice == "1":
            state = imm.execute()
            print("Immigration has been executed.")
        elif choice == "2":
            t = Thresholds(state, myCountry)

            # check if our country has enough resources to make this transaction
            if t.is_valid_transfer(most_needed, req):
                transfer = Transfer(state, myCountry, country, (most_needed,req))
                state = transfer.execute()
                print("Transfer has been executed.")
            
            # if our country lacks the resource, force the immigration
            else:
                print("You don't have enough of this resource to complete the transfer.")
                state = imm.execute()
                print("Immigration has been executed.")
    
    t = Thresholds(state, myCountry)

    # all resources at comfortable level
    if t.is_perfect():
        print("YOU WIN!")
        finished = True
    
    # at least 1 resource under 20%
    if t.in_danger_zone():
        print("Beware, at least one of your resources is in the danger zone.")
        lives -= 1
        print("You have", lives, "lives left")
    
    if lives <= 0:
        print("YOU LOSE!")
        finished = True

    # population growth
    growth = PopulationGrowth(state, uniform(1.01,1.5))
    state = growth.execute()

    year += 1
