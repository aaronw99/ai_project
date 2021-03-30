from manager import Manager
from player import Player

gm = Manager()
playerA = Player("Atlantis")
playerAState = {"R1": 1000, "R2": 1500, "R3": 400, "cash": 7000}
playerB = Player("Brobdingnag")
playerBState = {"R1": 100, "R2": 5000, "R3": 450, "cash": 5000}
playerC = Player("Brobdingnag")
playerCState = {"R1": 700, "R2": 500, "R3": 2000, "cash": 10000}

gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)
gm.addPlayer(playerC, playerCState)
print(gm.getWorldState())

gm.playOneRound()
print(gm.getWorldState())