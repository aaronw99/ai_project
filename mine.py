import numpy as np
import pandas as pd

# The Mine class represents the mine operation
# As difficulty of the mine increases, the amount of turns to complete the action increases, but the potential payout increases
class Mine:
    def __init__(self, player, resource, difficulty = 1):
        self.player = player
        self.resource = resource
        self.difficulty = difficulty
    
    def execute(self, world):
        self.player.free = True
        population = world[self.player.name]["R1"]
        upper_limit = self.difficulty
        if population < 50:
            upper_limit = 50 * self.difficulty
        elif population > 150:
            upper_limit = 150 * self.difficulty 
        else:
            upper_limit = population * self.difficulty
        skewed = 20

        pers = np.arange(1, upper_limit, 1)
        # Make the last n elements 10x more likely 
        # The mining country is likely to get a big payout, but chance is still involved and the country can get a lower payout
        prob = [1.0] * (len(pers) - (skewed)) + [10.0] * skewed
        # Normalising to 1.0
        prob /= np.sum(prob)
        payout = np.random.choice(pers, 1, p = prob)
        world[self.player.name][self.resource] = world[self.player.name][self.resource] + payout.item(0)
    
    def toString(self):
        string = "(MINE " + self.player.name + " RESOURCE (" + self.resource + ") "
        string = string + "DIFFICULTY (" + str(self.difficulty) + "))"
        return string

    # __lt__
    # < operator for Mine instances
    # @other(obj): an object
    def __lt__(self, other):
        resources_df = pd.read_excel('/home/aaronwong/code/ai_project/resources.xlsx')

        if isinstance(other, Mine):
            if self.resource == other.resource:
                return self.difficulty < other.difficulty
            else:
                return resources_df[resources_df['Resources'] == self.resource]['Weight'].iloc[0] < resources_df[resources_df['Resources'] == other.resource]['Weight'].iloc[0]
        else:
            return False