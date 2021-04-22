class Transformation:
    def __init__(self, name, template, multiplier = 1):
        self.name = name
        self.template = template
        self.multiplier = multiplier
    
    def execute(self, world):
        inputs = self.template["in"]
        outputs = self.template["out"]
        for r_type in inputs:
            world[self.name][r_type] = world[self.name][r_type] - inputs[r_type] * self.multiplier
        for r_type in outputs:
            world[self.name][r_type] = world[self.name][r_type] + outputs[r_type] * self.multiplier
<<<<<<< HEAD
=======
        return world
>>>>>>> 6202892547aa510f64c45949192dcdeadca73b21
        
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

