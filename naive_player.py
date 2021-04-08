from player import Player
from transformation import Transformation
from transaction import Transaction
from mine import Mine
from world_wrapper import WorldWrapper
from scheduler import Scheduler
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import heapq

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
        #below is the core of the wrapper
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
                transaction = Transaction(self.name, "sell", {ticker: [{"quantity": quantity, "strike": price}]}, market)
                actions.append(transaction)
            else:
                price = market.quotePrice(ticker)["buyingPrice"]
                #todo: generate a desired buy order
                if price == float("inf"):
                    price = world[self.name]["cash"] / 2 / quantity
                else:
                    quantity = int(world[self.name]["cash"] / price)
                if quantity != 0:
                    transaction = Transaction(self.name, "buy", {ticker: [{"quantity": quantity, "strike": price}]}, market)
                    actions.append(transaction)
                else:
                    mine = Mine(self, ticker, 2)
                    actions.append(mine)
        if tokens[0] == "TRANSFORM":
            print("TRANSFORM is yet to be implemented")
        return actions
        