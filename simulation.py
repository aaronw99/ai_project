from manager import Manager
from player import Player
from transform import Transform
from transaction import Transaction

gm = Manager()
playerA = Player("Atlantis")
playerAState = {}
playerB = Player("Something")
playerBState = {}

gm.addPlayer(playerA, playerAState)
gm.addPlayer(playerB, playerBState)

gm.playOneRound()
