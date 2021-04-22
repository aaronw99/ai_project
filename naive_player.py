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
    def __init__(self, name):
        Player.__init__(self, name)
        
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
        #below is the wrapper
        table = str.maketrans(dict.fromkeys("()"))
        bestAction = bestSchedule[0][0].translate(table)
        tokens = bestAction.split()
        actions = []
        if tokens[0] == "TRANSFER":
            fromName = tokens[2]
            ticker = tokens[5]
            quantity = int(tokens[6])
            if fromName == self.name:
                price = market.quotePrice(ticker)["sellingPrice"]
                #todo: generate a desired sell order
                if price == float("-inf"):
                    price = 30
                transaction = Transaction(self.name, "sell", {ticker: [{"quantity": quantity, "strike": price, "expiration": 2}]}, market)
                actions.append(transaction)
            else:
                price = market.quotePrice(ticker)["buyingPrice"]
                #todo: generate a desired buy order
                if price == float("inf"):
                    price = world[self.name]["cash"] / 2 / quantity
                else:
                    quantity = int(world[self.name]["cash"] / price)
                if quantity != 0:
                    transaction = Transaction(self.name, "buy", {ticker: [{"quantity": quantity, "strike": price, "expiration": 2}]}, market)
                    actions.append(transaction)
                else:
                    mine = Mine(self, ticker, 2)
                    actions.append(mine)
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
        