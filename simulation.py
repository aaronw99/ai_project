from manager import Manager
from naive_player import NaivePlayer
from human_player import HumanPlayer
from random_player import RandomPlayer
from price_player import PricePlayer
import utils

# set up game manager
gm = Manager()
# the following is taken from test_initial_tests/initial_state_1.xlsx
initialStateNum = "1"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
# construct player agents
playerAName = "Atlantis"
playerA = NaivePlayer(playerAName)
playerAState = utils.getInitialState(initialStatePath, playerAName)
playerAState["cash"] = 7000

playerBName = "Brobdingnag"
playerB = RandomPlayer(playerBName)
playerBState = utils.getInitialState(initialStatePath, playerBName)
playerBState["cash"] = 15000

playerCName = "Carpania"
playerC = HumanPlayer(playerCName)
playerCState = utils.getInitialState(initialStatePath, playerCName)
playerCState["cash"] = 20000

playerDName = "Dinotopia"
playerD = PricePlayer(playerDName)
playerDState = utils.getInitialState(initialStatePath, playerDName)
playerDState["cash"] = 10000

# add players to the game manager
gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)
gm.addPlayer(playerC, playerCState)
gm.addPlayer(playerD, playerDState)
print("Initial World State", gm.world)
print()

# start simulation
rounds = 5
gm.run(rounds)
