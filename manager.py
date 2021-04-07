from market import Market
from mine import Mine
import heapq

class Manager:
    def __init__(self):
        self.world = {}
        self.market = Market(self.world)
        self.players = []
        self.miningQueue = []
    
    def addPlayer(self, player, initialState):
        self.players.append(player)
        self.world[player.name] = initialState
    
    def playOneRound(self):
        for player in self.players:
            if player.free:
                actions = player.generateActions(self.world, self.market)
                for action in actions:
                    if isinstance(action, Mine):
                        player.free = False
                        heapq.heappush(self.miningQueue, [action.difficulty, action])
                    else:
                        action.execute(self.world)
        self.runMiningQueue()
        self.market.settle()
        
    def runMiningQueue(self):
        for pairs in self.miningQueue:
            pairs[0] = pairs[0] - 1
        while self.miningQueue and self.miningQueue[0][0] == 0:
            self.miningQueue[0][1].execute(self.world)
            heapq.heappop(self.miningQueue)
    
    