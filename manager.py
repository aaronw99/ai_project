from market import Market

class Manager:
    def __init__(self):
        self.world = {}
        self.market = Market(self.world)
        self.players = []
    
    def addPlayer(self, player, initialState):
        self.players.append(player)
        self.world[player.getName()] = initialState
    
    def playOneRound(self):
        for player in self.players:
            actions = player.generateActions(self.world, self.market)
            for action in actions:
                action.execute()
        self.market.settle()
    
    def getWorldState(self):
        return self.world