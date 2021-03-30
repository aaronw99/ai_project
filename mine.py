import copy
import numpy as np

# The Mine class represents the mine operation
# As difficulty of the mine increases, the potential payout is higher, but so does the potential for
# an even smaller payout. 
class Mine:
    def __init__(self, state, country, resource, difficulty = 1):
        self.state = copy.deepcopy(state)
        self.country = country
        self.resource = resource
        self.difficulty = difficulty
    
    def execute(self):
        upper_limit = 100
        lower_skewed = 20
        upper_skewed = 20
        if self.difficulty == 1:
            if self.resource == 'R2' or self.resource == 'R3':
                upper_limit = 100
                lower_skewed = 20
                upper_skewed = 20
            elif self.resource == 'R6':
                upper_limit = 50
                lower_skewed = 10
                upper_skewed = 10
        elif self.difficulty == 2:
            if self.resource == 'R2' or self.resource == 'R3':
                upper_limit = 150
                lower_skewed = 10
                upper_skewed = 20
            elif self.resource == 'R6':
                upper_limit = 100
                lower_skewed = 5
                upper_skewed = 10
        elif self.difficulty == 3:
            if self.resource == 'R2' or self.resource == 'R3':
                upper_limit = 200
                lower_skewed = 5
                upper_skewed = 20
            elif self.resource == 'R6':
                upper_limit = 150
                lower_skewed = 3
                upper_skewed = 10

        pers = np.arange(1,upper_limit,1)
        # Make each of the first and last n elements 10x more likely 
        # The mining country is likely to either get a big or small payout, not some amount in the middle
        prob = [10.0]*lower_skewed + [1.0]*(len(pers)-(lower_skewed+upper_skewed)) + [10.0]*upper_skewed
        # Normalising to 1.0
        prob /= np.sum(prob)
        payout = np.random.choice(pers, 1, p=prob)
        self.state[self.country][self.resource] = self.state[self.country][self.resource] + payout.item(0)
        return self.state
        
    def toString(self):
        string = "(MINE " + self.country + " RESOURCE (" + self.resource + ") "
        string = string + "DIFFICULTY (" + str(self.difficulty) + "))"
        return string
