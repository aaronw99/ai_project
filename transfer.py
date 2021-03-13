import copy

# The Transfer class represents the singleton transfer operation
class Transfer:
    def __init__(self, state, country_from, country_to, trade):
        self.state = copy.deepcopy(state)
        self.country_from = country_from
        self.country_to = country_to
        self.trade = trade

    def execute(self):
        resource = self.trade[0]
        quantity = self.trade[1]
        self.state[self.country_from][resource] = self.state[self.country_from][resource] - quantity
        self.state[self.country_to][resource] = self.state[self.country_to][resource] + quantity
        return self.state

    def toString(self):
        resource = self.trade[0]
        quantity = self.trade[1]
        string = "(TRANSFER FROM " + self.country_from + " TO " + \
            self.country_to + " (" + resource + " " + str(quantity) + "))"
        return string

    def isFrom(self):
        return self.country_from

    def isTo(self):
        return self.country_to
