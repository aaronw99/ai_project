# The Transformation class represents the Transform action from p1 but it
# operates directly on the state of the world instead of a copy
class Transformation:
    # __init__
    # @name(str): the name of the country
    # @template(str): the name of the template
    # @multiplier(int): the multiplier associated with the template
    # this constructs the Transformation object
    def __init__(self, name, template, multiplier = 1):
        self.name = name
        self.template = template
        self.multiplier = multiplier
    
    # execute
    # @world(dict): the state of the world
    # this executes the transformation action and updates the state of the world
    def execute(self, world):
        inputs = self.template["in"]
        outputs = self.template["out"]
        for r_type in inputs:
            world[self.name][r_type] = world[self.name][r_type] - inputs[r_type] * self.multiplier
        for r_type in outputs:
            world[self.name][r_type] = world[self.name][r_type] + outputs[r_type] * self.multiplier
    
    # toString
    # this converts the transformation to a readable string
    def toString(self):
        string = "(TRANSFORMATION " + self.name + " INPUTS ("
        inputs = self.template["in"]
        outputs = self.template["out"]
        for r_type in inputs:
            string = string + "(" + r_type + " " + str(inputs[r_type] * self.multiplier) + ")"
        string = string + ") OUTPUTS("
        for r_type in outputs:
            string = string + "(" + r_type + " " + str(outputs[r_type] * self.multiplier)+ ")"
        string = string + "))"
        return string

