from manager import Manager
from naive_player import NaivePlayer

gm = Manager()
#the following is taken from initial state 1
playerA = NaivePlayer("Atlantis")
playerAState = {
    "R1": 100, 
    "R2": 30, 
    "R3": 20, 
    "R4": 120, 
    "R5": 1000,
    "R6": 5000, 
    "R7": 6000, 
    "R8": 660, 
    "R9": 50, 
    "R18": 30,
    "R19": 8,
    "R20": 200, 
    "R21": 60, 
    "R22": 20, 
    "R1'": 0,
    "R5'": 0,
    "R6'": 0,
    "R18'": 0,
    "R19'": 0,
    "R20'": 0,
    "R21'": 0,
    "R22'": 0,
    "cash": 7000
}
playerB = NaivePlayer("Brobdingnag")
playerBState = {
    "R1": 100, 
    "R2": 10, 
    "R3": 15, 
    "R4": 100, 
    "R5": 300,
    "R6": 400, 
    "R7": 30, 
    "R8": 300, 
    "R9": 40, 
    "R18": 15,
    "R19": 4,
    "R20": 111, 
    "R21": 50, 
    "R22": 5, 
    "R1'": 0,
    "R5'": 0,
    "R6'": 0,
    "R18'": 0,
    "R19'": 0,
    "R20'": 0,
    "R21'": 0,
    "R22'": 0,
    "cash": 15000
}
playerC = NaivePlayer("Carpania")
playerCState = {
    "R1": 100, 
    "R2": 15, 
    "R3": 10, 
    "R4": 50, 
    "R5": 50,
    "R6": 200, 
    "R7": 20, 
    "R8": 200, 
    "R9": 20, 
    "R18": 25,
    "R19": 3,
    "R20": 123, 
    "R21": 20, 
    "R22": 10, 
    "R1'": 0,
    "R5'": 0,
    "R6'": 0,
    "R18'": 0,
    "R19'": 0,
    "R20'": 0,
    "R21'": 0,
    "R22'": 0,
    "cash": 20000
}

gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)
gm.addPlayer(playerC, playerCState)
print(gm.world)

gm.playOneRound()
print(gm.world)
print("------------Market------------")
gm.market.printOrderBook()
