from market import Market
from mine import Mine
import heapq

# The Manager class represents the game manager, which is in charge of
# running the event loop of the game (playOneRound)
class Manager:
    # __init___
    # this constructs the Manager object
    def __init__(self):
        self.world = {}
        self.market = Market()
        self.players = []
        self.miningQueue = []
    
    # addPlayer
    # @player(object): a player object. See player.py for details
    # @initialState(dict): the initial state of the given player
    def addPlayer(self, player, initialState: dict):
        self.players.append(player)
        self.world[player.name] = initialState
    
    # playOneRound
    # run one round of the game and apply the actions proposed by each player
    # this is the "event loop" of the game
    def playOneRound(self):
        for player in self.players:
            if player.free:
                print("-------" + player.name + "'s turn-------")
                actions = player.generateActions(self.world, self.market)
                print(player.name, "proposed:")
                for action in actions:
                    print(action.toString())
                    if isinstance(action, Mine):
                        player.free = False
                        heapq.heappush(self.miningQueue, [action.difficulty, action])
                    else:
                        action.execute(self.world)
                print("-" * (len(player.name) + 21))
                print()
        self.runMiningQueue()
        self.market.settle(self.world)
    
    # runMiningQueue
    # update the mining queue
    def runMiningQueue(self):
        for pairs in self.miningQueue:
            pairs[0] = pairs[0] - 1
        while self.miningQueue and self.miningQueue[0][0] == 0:
            self.miningQueue[0][1].execute(self.world)
            heapq.heappop(self.miningQueue)
    
    # run
    # run the game with the given round limit
    # @rounds: the round limit
    def run(self, rounds: int):
        for i in range(0, rounds):
            self.playOneRound()