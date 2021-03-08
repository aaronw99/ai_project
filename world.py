import pandas as pd
from transform import Transform
from transfer import Transfer
import random

#util
def calculate_transform_max_multiplier(resources, template):  
    multiplier = -1
    inputs = template["in"]
    for r_type in inputs:
        if multiplier == -1:
            multiplier = int(resources[r_type] / inputs[r_type])
        else:
            multiplier = min(multiplier, int(resources[r_type] / inputs[r_type]))
    return multiplier

def calculate_state_quality(state: dict, country: str):
    country_resources = state[country]
    population = country_resources['R1']

    # Calculate required amounts of resources for "survival" and "comfortable" level
    survival = {'R2': 1.5, 'R3': 1, 'R4': 6, 'R5': 50, 'R6': 250, 'R7': 300, 'R8': 33, 'R9': 2.5, 'R18': 1.5, 'R19': .4, 'R20': 10, 'R21': 3,  'R22': 1}
    comfortable = {'R2': 1.5, 'R3': 1, 'R4': 6, 'R5': 50, 'R6': 250, 'R7': 300, 'R8': 33, 'R9': 2.5, 'R18': 1.5, 'R19': .4, 'R20': 10, 'R21': 3,  'R22': 1}
    for resource in survival.keys():
        survival[resource] = survival[resource] * 0.2 * population
        comfortable[resource] = comfortable[resource] * population

    resources_df = pd.read_excel('resources.xlsx')
    weighted_sum = 0.0
    below_survival = False

    for resource in country_resources.keys():
        resource_quantity = country_resources[resource]
        resource_value = resources_df[resources_df['Resources'] == resource]['Weight'].iloc[0]
        above_comfortable = False

        if resource in survival.keys():
            if resource_quantity < int(survival[resource]):
                below_survival = True
            elif resource_quantity >= int(comfortable[resource]):
                above_comfortable = True

        if above_comfortable:
            difference = resource_quantity - comfortable[resource]
            weighted_sum = weighted_sum + (comfortable[resource] * resource_value) + (difference * resource_value / 2)
        else:
            weighted_sum = weighted_sum + (resource_quantity * resource_value)

    normalized = weighted_sum / population
    if below_survival:
        return normalized - 1000
    else:
        return normalized

class World:
    def __init__(self, myCountry, transform_templates):
        self.myCountry = myCountry
        self.transform_templates = transform_templates
        data = pd.read_excel('initial_state.xlsx')
        df = pd.DataFrame(data)
        #reformats in json style
        initial_state = {}
        for index, row in df.iterrows():
            initial_state[row["Country"]] = {}
            initial_state[row["Country"]]["R1"] = row["R1"]
            initial_state[row["Country"]]["R2"] = row["R2"]
            initial_state[row["Country"]]["R3"] = row["R3"]
            initial_state[row["Country"]]["R4"] = row["R4"]
            initial_state[row["Country"]]["R5"] = row["R5"]
            initial_state[row["Country"]]["R6"] = row["R6"]
            initial_state[row["Country"]]["R7"] = row["R7"]
            initial_state[row["Country"]]["R8"] = row["R8"]
            initial_state[row["Country"]]["R9"] = row["R9"]
            initial_state[row["Country"]]["R18"] = row["R18"]
            initial_state[row["Country"]]["R19"] = row["R19"]
            initial_state[row["Country"]]["R20"] = row["R20"]
            initial_state[row["Country"]]["R21"] = row["R21"]
            initial_state[row["Country"]]["R22"] = row["R22"]
            initial_state[row["Country"]]["R1'"] = row["R1'"]
            initial_state[row["Country"]]["R5'"] = row["R5'"]
            initial_state[row["Country"]]["R6'"] = row["R6'"]
            initial_state[row["Country"]]["R18'"] = row["R18'"]
            initial_state[row["Country"]]["R19'"] = row["R19'"]
            initial_state[row["Country"]]["R20'"] = row["R20'"]
            initial_state[row["Country"]]["R21'"] = row["R21'"]
            initial_state[row["Country"]]["R22'"] = row["R22'"]
        self.startState = initial_state
        
    def getStartState(self):
        return self.startState
    
    def getSuccessors(self, state):
        successors = []
        myResources = state[self.myCountry]
        #generate random transforms for self.myCountry
        for template in self.transform_templates:
            #check maximum possible multipler
            max_multiplier = calculate_transform_max_multiplier(myResources, template)
            #print(max_multiplier)
            if max_multiplier:
                transform = Transform(state, self.myCountry, template, random.randint(1, max_multiplier))
                successors.append([transform.execute(), transform.toString()])
        #generate possible transfers
        for country in state:
            if country != self.myCountry:
                theirResources = state[country]
                #for each resource in self.myCountry, randomly generate some transfer operations
                for r_type in myResources:
                    amount = myResources[r_type]
                    if amount and r_type != "R1":
                        transfer = Transfer(state, self.myCountry, country, (r_type, random.randint(1, amount)))
                        #print(transfer.toString())
                        successors.append([transfer.execute(), transfer.toString()])
                #for each resource in other countries randomly generate some transfer operations
                for r_type in theirResources:
                    amount = myResources[r_type]
                    if amount and r_type != "R1":
                        transfer = Transfer(state, country, self.myCountry, (r_type, random.randint(1, amount)))
                        #print(transfer.toString())
                        successors.append([transfer.execute(), transfer.toString()])
        return successors
    
    def getExpectedUtility(self, state, length):
        #calculate eu for self.myCountry
        startQuality = calculate_state_quality(self.startState, self.myCountry)
        endQuality = calculate_state_quality(state, self.myCountry)
        gamma = 1
        reward = endQuality - startQuality
        #print("start:", startQuality, "end:", endQuality, "reward:", reward)
        discounted_reward = (gamma ** length) * reward
        probability_success = 1
        failure_cost = 0
        eu = probability_success * discounted_reward + (1 - probability_success) * failure_cost
        return eu
        

# housing = {
#     "in": {'R1': 5, 'R2': 1, 'R3': 5, 'R18': 3},
#     "out": {'R1': 5, 'R19': 1, "R19'": 1}
# }
# alloys = {
#     "in": {'R1': 1, 'R2': 2},
#     "out": {'R1': 1, "R18": 1, "R18'": 5}
# }
# electronics = {
#     "in": {'R1': 1, 'R2': 3, 'R18': 2},
#     "out": {'R1': 1, "R20": 2, "R20'": 1}
# }
# transform_templates = [housing, alloys, electronics]
# myCountry = "Atlantis"
# world = World(myCountry, transform_templates)
# print("Testing world ctor")
# startState = world.getStartState()
# print(startState)

# print("Testing calculate_transform_max_multiplier")
# my_resources = startState["Atlantis"]
# print(my_resources)
# print(calculate_transform_max_multiplier(my_resources, alloys))
# print(calculate_transform_max_multiplier(my_resources, housing))

# print("Testing transform")
# transform = Transform(startState, myCountry, alloys, 1)
# print(transform.toString())
# newState = transform.execute()

# print(newState)
# print(startState) #IMPORTANT: notice that execute operates on a deep copy of the state

# print("Testing getSuccessors")
# successors = world.getSuccessors(startState)
# #this should print out 100 since only 100 variations of the alloy transform can be applied
# #on the initial state for Atlantis
# print(len(successors))
# #this is the format of a single entry in the output
# print(successors[2])

# print("Testing calculate_state_quality")
# print(calculate_state_quality(startState, 'Atlantis'))


