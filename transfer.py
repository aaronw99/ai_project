import copy

class Transfer:
    def __init__(self, state, country_1, country_2, trade):
  
        self.state = copy.deepcopy(state)
        self.country_1 = country_1
        self.country_2 = country_2
        self.trade = trade
    
    def execute(self):
        type = self.trade[0]
        quantity = self.trade[1]
        self.state[self.country_1][type] = self.state[self.country_1][type] - quantity 
        self.state[self.country_2][type] = self.state[self.country_2][type] + quantity
   
        return self.state
        
    def toString(self):
        type = self.trade[0]
        quantity = self.trade[1]
        string = "(TRANSFER " + self.country_1 + " " + self.country_2 + " (" + type + " " + str(quantity) + "))"
        return string
