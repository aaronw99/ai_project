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
            if command == "buy":
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
                        if len(tokens) < 3:
                            print("Missing parameters")
                        else:
                            tickers = tokens[2].split(",")
                            for i in range(0, len(tickers)):
                                ticker = tickers[i].upper()
                                print(ticker, market.quotePrice(ticker))
                    elif flag == "-tm":
                        print("housing:", housing)
                        print("alloys:", alloys)
                        print("electronics:", electronics)
                        print("farms:", farms)
                        print("factories:", factories)
                        print("metallic_elements:", metallic_elements)
                        print("timber:", timber)
                        print("plant:", plant)
                    else:
                        print("Illgeal flag")
                else:
                    print("My State:", world[self.name])
            elif command == "mine":
                if len(tokens) < 3:
                    print("missing parameters")
                else:
                    resource = tokens[1].upper()
                    difficulty = int(tokens[2])
                    mine = Mine(self, resource, difficulty)
                    print("Submitted: ", mine.toString())
                    actions.append(mine)
            #todo: implement this
            elif command == "transform":
                if len(tokens) < 3:
                    print("missing parameters")
                else:
                    t = tokens[1].lower()
                    multiplier = int(tokens[2])
                    template = ""
                    if t == "housing":
                        template = housing
                    if t == "alloys":
                        template = alloys
                    if t == "electronics":
                        template = electronics
                    if t == "farms":
                        template = farms
                    if t == "factories":
                        template = factories
                    if t == "metallic_elements":
                        template = metallic_elements
                    if t == "timber":
                        template = timber
                    if t == "plant":
                        template = plant
                    if template:
                        transformation = Transformation(self.name, template, multiplier)
                        print("Submitted: ", transformation.toString())
                        actions.append(transformation)
                    else:
                        print("Illegal template")
            #lol why not
            elif command == "greedisgood":
                money = 5000
                if len(tokens) >= 2:
                    money = float(tokens[1])
                world[self.name]["cash"] = world[self.name]["cash"] + money
                print("You gave yourself " + str(money) + " cash")
            elif command == "end":
                finish = True
            elif command == "help":
                print("Here's a list of the commands: ")
                print("1. show [-w] [-m] [-t (t1,t2,t3...)] [-tm]")
                print("2. buy (ticker) (strike1,quantity1,[expiration1]) (strike2,quantity2,[expiration2]) ...")
                print("3. sell (ticker) (strike1,quantity1,[expiration1]) (strike2,quantity2,[expiration2]) ...")
                print("4. mine (resource) (difficulty)")
                print("5. transform (template) (multiplier)")
                print("6. end")
            else:
                print("Illegal command")
            print()
        return actions

