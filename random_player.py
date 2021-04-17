from player import Player
from transformation import Transformation
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import utils
import random
from transformation import Transformation
from transaction import Transaction
from mine import Mine
from world_wrapper import WorldWrapper
from scheduler import Scheduler
import heapq

# The RandomPlayer class is a player that randomly buys/sells/transforms each turn
class RandomPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def generateActions(self, world, market):
        # a list of the possible randoma ctions
        actions = []

        # generate possible transforms
        transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
        myResources = world[self.name]
        for template in transform_templates:
            max_multiplier = utils.calculate_transform_max_multiplier(
                myResources, template)
            if max_multiplier:
                transform = Transformation(self.name, template, max_multiplier)
                actions.append(transform)

        # generate possible buys from the market
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
                        transaction = Transaction(self.name, "buy", {resource: [{"quantity": quantity_to_buy, "strike": price}]}, market)
                        actions.append(transaction)

        # generate possible sells for the market
        for resource in resources:
            if resource not in untradeable_resources:
                quantity = myResources[resource]
                price = market.quotePrice(resource)["sellingPrice"]
                if price == float("-inf"):
                    price = 30
                # create a sell order for a random amount of the resource that the country has at the market's price for it
                quantity = random.randint(1, quantity)
                transaction = Transaction(self.name, "sell", {resource: [{"quantity": quantity, "strike": price}]}, market)
                actions.append(transaction)

        # generate possible random mine actions
        mineable_resources = ["R2", "R3", "R6"]
        for resource in mineable_resources:
            for difficulty in [1,2,3]:
                mine = Mine(self, resource, difficulty)
                actions.append(mine)
        
        # return one random action of all the possible actions
        action = [random.choice(actions)]
        print(self.name + ": " + action[0].toString())
        return action