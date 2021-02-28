import copy

class Transfer:
    def __init__(self, state, country_1, country_2, trade):
        #country1 would be the main actor of trade here, so "in" and "out" corresponds 
        #to the resource of country1 and will be the contrary for country 2
        self.state = copy.deepcopy(state)
        self.country_1 = country_1
        self.country_2 = country_2
        self.trade = trade
    
    def execute(self):
        inputs = self.trade["in"]
        outputs = self.trade["out"]
        for r_type in inputs:
            self.state[self.country_1][r_type] = self.state[self.country_1][r_type] + inputs[r_type] 
            self.state[self.country_2][r_type] = self.state[self.country_2][r_type] - inputs[r_type] 
        for r_type in outputs:
            self.state[self.country_1][r_type] = self.state[self.country_1][r_type] - outputs[r_type]
            self.state[self.country_2][r_type] = self.state[self.country_2][r_type] + outputs[r_type] 
        return self.state
        
    def toString(self):
        string = "(TRANSFER " + self.country_1 
        inputs = self.trade["in"]
        outputs = self.trade["out"]
        for r_type in inputs:
            string = string + "(" + r_type + " " + str(inputs[r_type]) + ")"
        string = string + " TRANSFER " + self.country_2 
        for r_type in outputs:
            string = string + "(" + r_type + " " + str(outputs[r_type])+ ")"
        string = string + "))"
        return string
