import copy 
from random import random

# The Immigration class represents the singleton immigration operation
class Immigration:

    def __init__(self, state, country_from, country_to, cf_model, cycle, models):
        self.state = copy.deepcopy(state)
        self.country_from = country_from

        # 1980 is the first year in the dataset
        self.cycle = cycle + 1979
        self.models = models
        self.country_to = country_to
        self.cf_model = cf_model

        # multiply model value in dictionary with number of millions of people
        self.level = round(abs(self.models[cf_model](self.cycle)) * self.state[self.country_from]["R1"])
    
    def execute(self):
        self.state[self.country_to]["R1"] += self.level / 1000000
        self.state[self.country_from]["R1"] -= self.level / 1000000
        return self.state

    def get_level(self):
        return round(self.level)

    # randomize_level
    # this multiplies the level by a given multiplier and 
    # reverses flow of immigration according to a chance varable
    # @multiplier(float): is multiplied to the level
    # @reverseChance(float): a float between 0 and 1 that represents 
    #   chances of reversing the immigration flow
    def randomize_level(self, multiplier, reverseChance):
        if random() < reverseChance:

            # swap country_from and country_to
            self.country_from, self.country_to = self.country_to, self.country_from

            # regenerate level using new country_from population to scale
            self.level = (abs(self.models[self.cf_model](self.cycle)) * self.state[self.country_from]["R1"])
        
        self.level *= multiplier
        self.level = round(self.level)


    def __str__(self):
        string = f"(IMMIGRATION FROM {self.country_from} TO {self.country_to}: {self.level} people)"
        return string
