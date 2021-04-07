import sys
sys.path.append('../')

from player import Player
from mine import Mine
from manager import Manager

class MinePlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
    
    def generateActions(self, world, market):
        mine = Mine(self, "R1", 3)
        return [mine]


gm = Manager()
#the following is taken from initial state 1
playerA = MinePlayer("Atlantis")
playerAState = {"R1": 10}
gm.addPlayer(playerA, playerAState)
print("initial world state:", gm.world)
gm.playOneRound()
print("after 1 round:", gm.world)
gm.playOneRound()
print("after 2 rounds:", gm.world)
gm.playOneRound()
print("after 3 rounds:", gm.world)