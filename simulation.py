from manager import Manager
from naive_player import NaivePlayer
import utils

#set up game manager
gm = Manager()
#the following is taken from test_initial_tests/initial_state_1.xlsx
initialStateNum = "1"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
#construct player agents
playerAName = "Atlantis"
playerA = NaivePlayer(playerAName)
playerAState = utils.getInitialState(initialStatePath, playerAName)
playerAState["cash"] = 7000

playerBName = "Brobdingnag"
playerB = NaivePlayer(playerBName)
playerBState = utils.getInitialState(initialStatePath, playerBName)
playerBState["cash"] = 15000

playerCName = "Carpania"
playerC = NaivePlayer(playerCName)
playerCState = utils.getInitialState(initialStatePath, playerCName)
playerCState["cash"] = 20000

#add players to the game manager
gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)
gm.addPlayer(playerC, playerCState)
print("Initial World State", gm.world)
print()

#start simulation
rounds = 2
for i in range(0, rounds):
    print("-----------Round " + str(i + 1) + "-----------")
    gm.playOneRound()
    print("World State:", gm.world)
    print("------------Market------------")
    gm.market.printOrderBook()
    print()
