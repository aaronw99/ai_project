from transform import Transform
from transaction import Transaction

class Player:
    def __init__(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def generateActions(self, world, market):
        return []

