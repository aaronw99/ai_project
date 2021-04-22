# This Player class is the interface that the game manager expects
# To create a new type of player, inherit from this class and overwrite
# the "generateActions" method
class Player:
    # __init___
    # @name(str): the name of the player
    # this constructs the Player object
    def __init__(self, name):
        self.name = name
        self.free = True    
    
    # generateActions
    # this generates the actions that a(n) player/agent will take at each turn;
    # game manager will invoke this method each round for each player and pass
    # in the world state and the market state
    # @world(dict): the state of the world
    # @market(object): the market object
    def generateActions(self, world: dict, market):
        return []
