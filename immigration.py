import copy 

class Immigration:
    def __init__(self, state, country_from, cf_model, cycle, models, country_to="Atlantis"):
        self.state = copy.deepcopy(state)
        self.country_from = country_from
        self.cycle = cycle + 1979
        self.models = models
        self.country_to = country_to
        self.level = self.models[cf_model](self.cycle)
    
    def execute(self):
        cf_population = self.state[self.country_from]["R1"]
        ct_population = self.state[self.country_to]["R1"]
        
        if self.level > 0:
            self.state[self.country_to]["R1"] += self.level * cf_population
            self.state[self.country_from]["R1"] -= self.level * ct_population
        else:
            self.state[self.country_from]["R1"] += self.level * ct_population
            self.state[self.country_to]["R1"] -= self.level * cf_population

        return self.state

    def toString(self):
        string = f"(IMMIGRATION FROM {self.country_from} TO {self.country_to}: {self.level})"
        return string
