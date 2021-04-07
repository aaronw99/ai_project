import numpy as np

# The Mine class represents the mine operation
# As difficulty of the mine increases, the amount of turns to complete the action increases, but the potential payout increases
class Mine:
    def __init__(self, player, resource, difficulty = 1):
        self.player = player
        self.resource = resource
        self.difficulty = difficulty
    
    def execute(self, world):
        self.player.free = True
        upper_limit = 50 * self.difficulty
        skewed = 20

        pers = np.arange(1, upper_limit, 1)
        # Make the last n elements 10x more likely 
        # The mining country is likely to get a big payout, but chance is still involved and the country can get a lower payout
        prob = [1.0] * (len(pers) - (skewed)) + [10.0] * skewed
        # Normalising to 1.0
        prob /= np.sum(prob)
        payout = np.random.choice(pers, 1, p = prob)
        world[self.country][self.resource] = world[self.country][self.resource] + payout.item(0)
    
    def toString(self):
        string = "(MINE " + self.country + " RESOURCE (" + self.resource + ") "
        string = string + "DIFFICULTY (" + str(self.initial_difficulty) + "))"
        return string
