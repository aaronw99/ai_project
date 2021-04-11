from player import Player
from transformation import Transformation
from transaction import Transaction
from mine import Mine
from world_wrapper import WorldWrapper
from scheduler import Scheduler
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import heapq

# The RandomPlayer class is a player that randomly buys/sells/transforms each turn
class RandomPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def generateActions(self, world, market):
        return []
        