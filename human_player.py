from player import Player
from transformation import Transformation
from transaction import Transaction
from mine import Mine
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)        
    
    def generateActions(self, world, market):
        finish = False
        actions = []
        while not finish:
            print("Awaiting command: ")
            string = str(input())
            tokens = string.split()
            command = tokens[0].lower()
            if command == "bid":
                if len(tokens) < 3:
                    print("Missing parameters")
                else:
                    ticker = tokens[1].upper()
                    orders = []
                    for i in range(2, len(tokens)):
                        order = tokens[i].split(",")
                        content = {}
                        strike = float(order[0])
                        content["strike"] = strike
                        quantity = int(order[1])
                        content["quantity"] = quantity
                        if len(order) >= 3:
                            expiration = int(order[2])
                            content["expiration"] = expiration
                        orders.append(content)
                    transaction = Transaction(self.name, "buy", {ticker: orders}, market)
                    actions.append(transaction)
                    print("Submitted:")
                    print(transaction.toString())
            elif command == "sell":
                if len(tokens) < 3:
                    print("Missing parameters")
                else:
                    ticker = tokens[1].upper()
                    orders = []
                    for i in range(2, len(tokens)):
                        order = tokens[i].split(",")
                        content = {}
                        strike = float(order[0])
                        content["strike"] = strike
                        quantity = int(order[1])
                        content["quantity"] = quantity
                        if len(order) >= 3:
                            expiration = int(order[2])
                            content["expiration"] = expiration
                        orders.append(content)
                    transaction = Transaction(self.name, "sell", {ticker: orders}, market)
                    actions.append(transaction)
                    print("Submitted:")
                    print(transaction.toString())
            elif command == "show":
                if len(tokens) > 1:
                    flag = tokens[1].lower()
                    if flag == "-w":
                        print("World State:", world)
                    elif flag == "-m":
                        market.printOrderBook()
                    elif flag == "-t":
                        for i in range(2, len(tokens)):
                            ticker = tokens[i].upper()
                            print(ticker, market.quotePrice(ticker))
                else:
                    print("My State:", world[self.name])
            elif command == "mine":
                if len(tokens) <= 3:
                    print("missing parameters")
                else:
                    resource = tokens[1].upper()
                    difficulty = int(tokens[2])
                    mine = Mine(self, resource, difficulty)
                    print("Submitted: ", mine.toString())
                    actions.append(mine)
            #todo: implement this
            elif command == "transformation":
                print("Not implemented!")
            elif command == "end":
                finish = True
            else:
                print("Illegal command")
            print()
        return actions

