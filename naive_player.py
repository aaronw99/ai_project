from player import Player
from transformation import Transformation
from transaction import Transaction
from mine import Mine
from world_wrapper import WorldWrapper
from scheduler import Scheduler
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import heapq

# The NaivePlayer class is a wrapper for our p1 code to utilize the
# market system
class NaivePlayer(Player):
    # __init___
    # @name(str): the name of the player
    # this constructs the NaivePlayer object
    def __init__(self, name):
        Player.__init__(self, name)
    
    # generateActions
    # this generates the actions that a(n) player/agent will take at each turn;
    # game manager will invoke this method each round for each player and pass
    # in the world state and the market state
    # @world(dict): the state of the world
    # @market(object): the market object
    def generateActions(self, world, market):
        resources_filename = "resources.xlsx"
        depth_bound = 5
        frontier_max_size = 5
        multiplier = 0.3
        transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
        worldWrapper = WorldWrapper(world, self.name, transform_templates, resources_filename)
        scheduler = Scheduler(worldWrapper)
        res = scheduler.search(depth_bound, frontier_max_size, multiplier)
        bestSchedule = heapq.heappop(res).getSchedule()
        # below is the wrapper
        table = str.maketrans(dict.fromkeys("()"))
        bestAction = bestSchedule[0][0].translate(table)
        tokens = bestAction.split()
        actions = []
        if tokens[0] == "TRANSFER":
            fromName = tokens[2]
            ticker = tokens[5]
            quantity = int(tokens[6])
            # convert a transfer that brings resource out to a market sell order
            if fromName == self.name:
                price = market.quotePrice(ticker)["sellingPrice"]
                # arbitrarily set the price so that we gain 25% of what we have in cash right now
                if price == float("-inf"):
                    price = world[self.name]["cash"] / 4 / quantity
                transaction = Transaction(self.name, "sell", {ticker: [{"quantity": quantity, "strike": price, "expiration": 2}]}, market)
                actions.append(transaction)
            # convert a transfer that brings resource in to a market buy order
            else:
                price = market.quotePrice(ticker)["buyingPrice"]
                # arbitrarily use 25% of the money to bid for it
                if price == float("inf"):
                    price = world[self.name]["cash"] / 4 / quantity
                # buy as much as possible
                else:
                    quantity = int(world[self.name]["cash"] / price)
                if quantity != 0:
                    transaction = Transaction(self.name, "buy", {ticker: [{"quantity": quantity, "strike": price, "expiration": 2}]}, market)
                    actions.append(transaction)
                # if the country cannot afford to buy it, convert it to a mine action
                else:
                    mine = Mine(self, ticker, 2)
                    actions.append(mine)
        # convert a transform to a transformation
        if tokens[0] == "TRANSFORM":
            tokens = bestAction.split("||")
            inputs = tokens[1].split()
            outputs = tokens[2].split()
            multiplier = int(tokens[3].split())
            template = {}
            template["in"] = {}
            template["out"] = {}
            for i in range(0, len(inputs) / 2):
                template["in"][inputs[i]] = int(inputs[i + 1])
            for i in range(0, len(outputs) / 2):
                template["out"][outputs[i]] = int(outputs[i + 1])
            transformation = Transformation(self.name, template, multiplier)
            actions.append(transformation)
        return actions
        