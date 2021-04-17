import sys
sys.path.append('../')
from manager import Manager
from random_player import RandomPlayer

C1 = {"R1": 1000, "R2": 1500, "R3": 400, "R4": 250, "R5": 300, "R6": 400, "R7": 200, "R8": 50, "R9": 20, "R18": 40, "R19": 10,
"R20": 150, "R21": 50, "R1'": 0, "R5'": 0, "R6'": 0, "R18'": 0, "R19'": 0, "R20'": 0, "R21'": 0, "R22'": 0,  "cash": 7000}

C2 = {"R1": 100, "R2": 5000, "R3": 450, "R4": 200, "R5": 350, "R6": 300, "R7": 200, "R8": 50, "R9": 20, "R18": 40, "R19": 10,
"R20": 150, "R21": 50, "R1'": 0, "R5'": 0, "R6'": 0, "R18'": 0, "R19'": 0, "R20'": 0, "R21'": 0, "R22'": 0,  "cash": 5000}

C3 = {"R1": 700, "R2": 500, "R3": 2000, "R4": 300, "R5": 250, "R6": 350, "R7": 200, "R8": 50, "R9": 20, "R18": 40, "R19": 10,
"R20": 150, "R21": 50, "R1'": 0, "R5'": 0, "R6'": 0, "R18'": 0, "R19'": 0, "R20'": 0, "R21'": 0, "R22'": 0,  "cash": 10000}

gm = Manager()
player1 = RandomPlayer("C1")
player1_state = C1
player2 = RandomPlayer("C2")
player2_state = C2
player3 = RandomPlayer("C3")
player3_state = C3

gm.addPlayer(player1, player1_state)
gm.addPlayer(player2, player2_state)
gm.addPlayer(player3, player3_state)

print("initial world state:", gm.world)
gm.playOneRound()
print("after 1 round:", gm.world)
gm.playOneRound()
print("after 2 rounds:", gm.world)
gm.playOneRound()
print("after 3 rounds:", gm.world)