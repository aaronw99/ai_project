import copy
from random import uniform

# PopulationGrowth stimulates population growth in all countries of a state
class PopulationGrowth:

    def __init__(self, state, percent):
        self.state = copy.deepcopy(state)
        self.percent = percent
    
    def execute(self):
        for country in self.state:
            self.state[country]['R1'] *= uniform(self.percent * 0.9, self.percent * 1.1)
        return self.state