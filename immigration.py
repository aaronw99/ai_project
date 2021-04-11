class Immigration:
    def __init__(self, country_from, cf_model, cycle, models, country_to="Atlantis"):
        self.country_from = country_from
        self.cycle = cycle + 1979
        self.models = models
        self.country_to = country_to
        self.level = self.models[cf_model][self.cycle]

    def toString(self):
        string = f"(IMMIGRATION FROM {self.country_from} TO {self.country_to}: {self.level})"
        return string
