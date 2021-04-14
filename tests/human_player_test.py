import sys
sys.path.append('../')

from manager import Manager
from human_player import HumanPlayer
import utils

#set up game manager
gm = Manager()
#the following is taken from test_initial_tests/initial_state_1.xlsx
initialStateNum = "1"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
#construct player agents
playerAName = "Atlantis"
playerA = HumanPlayer(playerAName)
playerAState = utils.getInitialState(initialStatePath, playerAName)
playerAState["cash"] = 7000

playerBName = "Brobdingnag"
playerB = HumanPlayer(playerBName)
playerBState = utils.getInitialState(initialStatePath, playerBName)
playerBState["cash"] = 15000

gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)

rounds = 2
gm.run(rounds)