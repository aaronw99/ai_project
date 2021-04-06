import copy
import numpy as np

# The Mine class represents the mine operation
# As difficulty of the mine increases, the amount of turns to complete the action increases, but the potential payout increases
class Mine:
    def __init__(self, state, country, resource, difficulty = 1):
        self.state = copy.deepcopy(state)
        self.country = country
        self.resource = resource
        self.initial_difficulty = difficulty
        self.turns_remaining = difficulty
    
    def execute(self):
        # There is no payout until the correct amount of turns passes
        if self.turns_remaining < 0:
            return self.state
        elif self.turns_remaining > 0:
            self.turns_remaining = self.turns_remaining - 1
            return self.state
        else:
            self.turns_remaining = -1
            upper_limit = 50 * self.initial_difficulty
            skewed = 20

            pers = np.arange(1,upper_limit,1)
            # Make the last n elements 10x more likely 
            # The mining country is likely to get a big payout, but chance is still involved and the country can get a lower payout
            prob = [1.0]*(len(pers)-(skewed)) + [10.0]*skewed
            # Normalising to 1.0
            prob /= np.sum(prob)
            payout = np.random.choice(pers, 1, p=prob)
            self.state[self.country][self.resource] = self.state[self.country][self.resource] + payout.item(0)
            return self.state
        
    def toString(self):
        string = "(MINE " + self.country + " RESOURCE (" + self.resource + ") "
        string = string + "DIFFICULTY (" + str(self.initial_difficulty) + "))"
        return string
