import pandas as pd
from transform import Transform
import utils

# The World class acts as a "reactor" for the scheduler
# It generates the successors and calculates the expected utility of a partial schedule
class World:
    # __init___
    # this constructs the World object with the given parameters
    # @myCountry(str): the name of our country
    # @transform_templates(list): a list of transform templates
    # @initStatePath(str): the path to the initial state file
    # @resourceWeightPath(str): the path to the resource weight file
    def __init__(self, myCountry, transform_templates, initStatePath, resourceWeightPath):
        self.myCountry = myCountry
        self.transform_templates = transform_templates
        self.resourceWeightPath = resourceWeightPath
        data = pd.read_excel(initStatePath)
        df = pd.DataFrame(data)
        # reformats in json style
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
    
    # getStartState
    # this returns the initial state of the world
    def getStartState(self):
        return self.startState

    # getSuccessors
    # this generates a list of successor state and action pairs given a world state
    # state(dict): the world state
    def getSuccessors(self, state):
        successors = []
        myResources = state[self.myCountry]
        # generates one transform for each template
        for template in self.transform_templates:
            # since all transform templates yield positive state quality return
            # we generate the one with the maximum possible multiplier
            max_multiplier = utils.calculate_transform_max_multiplier(
                myResources, template)
            if max_multiplier:
                transform = Transform(
                    state, self.myCountry, template, max_multiplier)
                successors.append([transform.execute(), transform])
                
        # generates possible economical imports and exports
        trades = utils.generate_trades(state, self.myCountry)
        for trade in trades:
            successors.append([trade.execute(), trade])
        return successors
    
    # getExpectedUtility 
    # this calculates the expected utility for self.myCountry given a partial schedule
    # @curState(dict): the current world state
    # @nextState(dict): the world state after executing the given action
    # @length(int): the length of the partial schedule
    # @action(obj): a single transfer or transform operation
    # @multiplier(float): the multiplier for failure cost
    def getExpectedUtility(self, curState, nextState, length, action, multiplier):
        startQuality = utils.calculate_state_quality(self.startState, self.myCountry, self.resourceWeightPath)
        endQuality = utils.calculate_state_quality(nextState, self.myCountry, self.resourceWeightPath)
        # we use a gamma of 0.95 for now to represent diminishing returns
        gamma = 0.95
        reward = endQuality - startQuality
        #print("state:", nextState, "sq:", endQuality, "reward:", reward)
        discounted_reward = (gamma ** length) * reward
        probability_success = utils.calculate_success_probability(
            self.myCountry, curState, nextState, action, self.resourceWeightPath)
        failure_cost = -discounted_reward * multiplier
        #print("discounted reward:", discounted_reward, "p:", probability_success)
        eu = probability_success * discounted_reward + \
            (1 - probability_success) * failure_cost
        return eu
