from player import Player
from transaction import Transaction
from mine import Mine

# The PricePlayer class is an agent that uses supply and demand to predict the
# price movement and act accordingly
class PricePlayer(Player):
    # __init___
    # @name(str): the name of the player
    # this constructs the HumanPlayer object
    def __init__(self, name):
        Player.__init__(self, name)
    
    # generateActions
    # this generates the actions that a(n) player/agent will take at each turn;
    # game manager will invoke this method each round for each player and pass
    # in the world state and the market state
    # @world(dict): the state of the world
    # @market(object): the market object
    def generateActions(self, world, market):
        actions = []
        untradeable_resources = ['R1', 'R4', 'R7', 'R19', 'R21', 'R22',
                             "R1'", "R5'", "R6'", "R18'", "R19'", "R20'", "R21'", "R22'", "cash"]
        myResources = world[self.name]
        lowOnCash = myResources["cash"] <= 2000
        # if the agent is low on cash, try to sell a type of resource for
        # cash gain and at the same time mine for the loss
        if lowOnCash:
            bestResourceToMine = ""
            bestPrice = float("-inf")
            # find the resource with the highest selling price
            for ticker in myResources.keys():
                if ticker not in untradeable_resources:
                    sellPrice = market.quotePrice(ticker)["sellingPrice"]
                    if sellPrice > bestPrice:
                        bestResourceToMine = ticker
                        bestPrice = sellPrice
            # if it exists, sell and mine
            if bestResourceToMine:
                quantity = market.getBuyOrders(bestResourceToMine)[0]["quantity"]
                if myResources[bestResourceToMine] < quantity:
                    quantity = myResources[bestResourceToMine] / 2
                transaction = Transaction(self.name, "sell", {bestResourceToMine: [{"quantity": quantity, "strike": bestPrice, "expiration": 2}]}, market)
                actions.append(transaction)
                mine = Mine(self, bestResourceToMine, 2)
                actions.append(mine)
        # generate actions according to the supply and demand
        else:
            cashAmount = myResources["cash"]
            for ticker in myResources.keys():
                if ticker not in untradeable_resources:
                    book = market.getOrders(ticker)
                    buyAmount = 0
                    sellAmount = 0
                    for order in book["bids"]:
                        buyAmount = buyAmount + order["quantity"]
                    for order in book["asks"]:
                        sellAmount = sellAmount + order["quantity"]
                    # if buyers are more than sellers, try to outbid the buyers 
                    # in anticipation for the price to go up
                    if buyAmount > sellAmount:
                        bestBid = book["bids"][0]
                        bidPrice = bestBid["strike"]
                        askPrice = float("inf")
                        askQuantity = float("inf")
                        if sellAmount != 0:
                            bestAsk = book["asks"][0]
                            askPrice = bestAsk["strike"]
                            askQuantity = bestAsk["quantity"]
                        myBidPrice = bidPrice + 5
                        if myBidPrice > askPrice:
                            myBidPrice = askPrice
                            
                        quantity = askQuantity
                        if myBidPrice * quantity > cashAmount:
                            quantity = int(cashAmount / 4 / myBidPrice)
                            
                        if quantity != 0:
                            transaction = Transaction(self.name, "buy", {ticker: [{"quantity": quantity, "strike": myBidPrice, "expiration": 2}]}, market)
                            cashAmount = cashAmount - myBidPrice * quantity
                            actions.append(transaction)
                    # if buyers are less than sellers, try to undercut the sellers
                    # in anticipation for the price to go down
                    if buyAmount < sellAmount:
                        bestAsk = book["asks"][0]
                        askPrice = bestAsk["strike"]
                        bidPrice = float("-inf")
                        bidQuantity = 0
                        if buyAmount != 0:
                            bestBid = book["bids"][0]
                            bidPrice = bestBid["strike"]
                            bidQuantity = bestBid["quantity"]
                        myAskPrice = askPrice - 5
                        if myAskPrice < bidPrice:
                            myAskPrice = bidPrice
                        if bidQuantity == 0:
                            quantity = int(myResources[ticker] / 20)
                            if quantity != 0:
                                transaction = Transaction(self.name, "sell", {ticker: [{"quantity": quantity, "strike": myAskPrice, "expiration": 2}]}, market)
                                actions.append(transaction)
                        else:
                            quantity = bidQuantity
                            if myResources[ticker] < quantity:
                                quantity = int(myResources[ticker] / 2)
                            if quantity != 0:
                                transaction = Transaction(self.name, "sell", {ticker: [{"quantity": quantity, "strike": myAskPrice, "expiration": 2}]}, market)
                                actions.append(transaction)
        return actions