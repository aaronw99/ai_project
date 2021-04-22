from player import Player
from transformation import Transformation
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import utils
import random
from transaction import Transaction
from mine import Mine

# The RandomPlayer class is a type of Player that randomly buys/sells/transforms each turn

class RandomPlayer(Player):
    # __init___
    # @name(str): the name of the player
    # this constructs the RandomPlayer object
    def __init__(self, name):
        Player.__init__(self, name)
    
    # generateActions
    # this generates the actions that a(n) player/agent will take at each turn;
    # game manager will invoke this method each round for each player and pass
    # in the world state and the market state
    # @world(dict): the state of the world
    # @market(object): the market object
    def generateActions(self, world, market):
        # a list of the possible random actions
        actions = []

        # Generate possible transforms
        transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
        myResources = world[self.name]
        for template in transform_templates:
            max_multiplier = utils.calculate_transform_max_multiplier(
                myResources, template)
            if max_multiplier:
                transform = Transformation(self.name, template, max_multiplier)
                actions.append(transform)

        # Generate possible buys from the market
        untradeable_resources = ['R1', 'R4', 'R7', 'R19', 'R21', 'R22',
                             "R1'", "R5'", "R6'", "R18'", "R19'", "R20'", "R21'", "R22'", "cash"]
        resources = myResources.keys()
        for resource in resources:
            if resource not in untradeable_resources:
                sell_orders = market.getSellOrders(resource)
                for order in sell_orders:
                    quantity = order["quantity"]
                    price = order["strike"]
                    seller = order["name"]
                    quantity_to_buy = world[self.name]["cash"] // price

                    # create a buy order of a random quantity of the resource up to the limit
                    quantity_to_buy = random.randint(1, quantity_to_buy)
                    if seller != self.name:
                        transaction = Transaction(self.name, "buy", {resource: [{"quantity": quantity_to_buy, "strike": price, "expiration": 3}]}, market)
                        actions.append(transaction)

        # Generate possible sells for the market
        for resource in resources:
            if resource not in untradeable_resources:
                quantity = myResources[resource]
                if quantity != 0:
                    price = market.quotePrice(resource)["sellingPrice"]
                    if price == float("-inf"):
                        price = 30
                    # Create a sell order for a random amount of the resource that the country has at the market's price for it
                    quantity = random.randint(1, quantity)
                    transaction = Transaction(self.name, "sell", {resource: [{"quantity": quantity, "strike": price, "expiration": 3}]}, market)
                    actions.append(transaction)

        # Generate possible random mine actions
        mineable_resources = ["R2", "R3", "R6"]
        for resource in mineable_resources:
            for difficulty in [1,2,3]:
                mine = Mine(self, resource, difficulty)
                actions.append(mine)
        
        # Return one random action of all the possible actions
        action = [random.choice(actions)]
        #print(self.name + ": " + action[0].toString())
        return action