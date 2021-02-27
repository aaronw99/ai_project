import pandas as pd
from transform import Transform

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

def calculate_state_quality(state, country):
    return 0

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
    
    def generateSuccessors(self, state):
        successors = []
        my_resources = state[self.myCountry]
        #generate possible transforms
        for template in self.transform_templates:
            #check maximum possible multipler
            multiplier = calculate_transform_max_multiplier(my_resources, template)
            #print(multiplier)
            for i in range(1, multiplier + 1):
                transform = Transform(state, self.myCountry, template, i)
                successors.append([transform.execute(), transform.toString()])
        #generate possible transfers
        for country in state:
            if country != self.myCountry:
                theirResources = state[country]
                
        return successors
    
    def getExpectedUtility(self, state, length):
        #calculate eu for self.myCountry
        startQuality = calculate_state_quality(self.startState, self.myCountry)
        endQuality = calculate_state_quality(state, self.myCountry)
        #add the expected utility function here
        return 0
        

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
print("Testing world ctor")
startState = world.getStartState()
print(startState)

print("Testing calculate_transform_max_multiplier")
my_resources = startState["Atlantis"]
print(my_resources)
print(calculate_transform_max_multiplier(my_resources, alloys))
print(calculate_transform_max_multiplier(my_resources, housing))

print("Testing transform")
transform = Transform(startState, myCountry, alloys, 1)
print(transform.toString())
newState = transform.execute()

print(newState)
print(startState) #IMPORTANT: notice that execute operates on a deep copy of the state

print("Testing generateSuccessors")
successors = world.generateSuccessors(startState)
#this should print out 100 since only 100 variations of the alloy transform can be applied
#on the initial state for Atlantis
print(len(successors))
#this is the format of a single entry in the output
print(successors[2])





