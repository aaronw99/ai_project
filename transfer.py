import copy

class Transfer:
    def __init__(self, state_1, state_2, country_1, country_2, template, multiplier = 1):
        #country1 would be the main actor of trade here, so "in" and "out" corresponds 
        #to the resource of country1 and will be the contrary for country 2
        self.state_1 = copy.deepcopy(state_1)
        self.state_2 = copy.deepcopy(state_2)
        self.country_1 = country_1
        self.country_2 = country_2
        self.template = template
        self.multiplier = multiplier
    
    def execute(self):
        inputs = self.template["in"]
        outputs = self.template["out"]
        for r_type in inputs:
            self.state_1[self.country_1][r_type] = self.state_1[self.country_1][r_type] + outputs[r_type] * self.multiplier
            self.state_2[self.country_2][r_type] = self.state_2[self.country_2][r_type] - inputs[r_type] * self.multiplier
        for r_type in outputs:
            self.state_1[self.country_1][r_type] = self.state_1[self.country_1][r_type] - outputs[r_type] * self.multiplier
            self.state_2[self.country_2][r_type] = self.state_2[self.country_2][r_type] + inputs[r_type] * self.multiplier
        return self.state_1, self.state_2
        
    def toString(self):
        string = "(TRANSFER " + self.country1 
        inputs = self.template["in"]
        outputs = self.template["out"]
        for r_type in inputs:
            string = string + "(" + r_type + " " + str(inputs[r_type] * self.multiplier) + ")"
        string = string + " TRANSFER " + self.country2 
        for r_type in outputs:
            string = string + "(" + r_type + " " + str(outputs[r_type] * self.multiplier)+ ")"
        string = string + "))"
        return string
