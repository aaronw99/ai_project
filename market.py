#work in progress
class Order:
    def __init__(self, name: str, quantity: int, strike: float, expiration = -1):
        self.name = name
        self.quantity = quantity
        self.strike = strike
        self.expiration = expiration
    
    def __lt__(self, other):
        if isinstance(other, Order):
            if self.strike == other.strike:
                return self.quantity < other.quantity
            return self.strike < other.strike
        else:
            return False
        
    def __le__(self, other):
        if isinstance(other, Order):
            return self.strike <= other.strike
        else:
            return False
    
    def setQuantity(self, quantity):
        self.quantity = quantity
        
    def setStrike(self, strike):
        self.strike = strike
    
    def setExpiration(self, expiration):
        self.expiration = expiration
        
    def getName(self):
        return self.name
        
    def getQuantity(self):
        return self.quantity
    
    def getStrike(self):
        return self.strike
    
    def getExpiration(self):
        return self.expiration
    
    def toString(self):
        output = "Strike: " + str(self.strike) + ". Quantity: " + str(self.quantity) + ". "
        if self.expiration != -1:
            output = output + "Expires in " + str(self.expiration) + ". "
        output = output + self.name
        return output

class Market:
    def __init__(self, world):
        self.world = world
        self.bids = {}
        self.asks = {}
        self.reserves = {}
        self.history = {}
        
    def submitBuyOrders(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.bids.keys():
                self.bids[ticker] = []
            #liquidity refers to the total amount of bids
            #if no one is buying, then the resource is not "liquid",
            #aka, cannot be cashe out
            liquidity = self.bids[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = self.quotePrice(ticker)["buyingPrice"]
                if "strike" in order.keys():
                    strike = order["strike"]
                limitBuyOrder = Order(name, quantity, strike)
                if "expiration" in order.keys():
                    limitBuyOrder.setExpiration(order["expiration"])
                liquidity.append(limitBuyOrder)
                #bid stack is sorted in descending order
                #because sellers want to sell high
                liquidity.sort(reverse = True)
                #reserve cash
                if name not in self.reserves:
                    self.reserves[name] = {}
                if "cash" not in self.reserves[name]:
                    self.reserves[name]["cash"] = 0
                self.reserves[name]["cash"] = self.reserves[name]["cash"] + quantity * strike
                self.world[name]["cash"] = self.world[name]["cash"] - quantity * strike
    
    def submitSellOrders(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.asks.keys():
                self.asks[ticker] = []
            #liquidity refers to the total amount of asks
            #if no one is selling, then the resource is not "liquid",
            #aka, no available "floating" resources for purchase
            liquidity = self.asks[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = self.quotePrice(ticker)["sellingPrice"]
                if "strike" in order.keys():
                    strike = order["strike"]
                limitSellOrder = Order(name, quantity, strike)
                if "expiration" in order.keys():
                    limitSellOrder.setExpiration(order["expiration"])
                liquidity.append(limitSellOrder)
                #ask stack is sorted in ascending order
                #because buyers want to buy low
                liquidity.sort()
                #reserve resources
                if name not in self.reserves:
                    self.reserves[name] = {}
                if ticker not in self.reserves[name]:
                    self.reserves[name][ticker] = 0
                self.reserves[name][ticker] = self.reserves[name][ticker] + quantity
                self.world[name][ticker] = self.world[name][ticker] - quantity
                
    def settle(self):
        #match buyers and sellers
        for ticker in self.asks.keys():
            if ticker in self.bids.keys():
                while self.asks[ticker] and self.bids[ticker] and self.asks[ticker][0] <= self.bids[ticker][0]:
                    asks = self.asks[ticker]
                    bids = self.bids[ticker]
                    sellerName = asks[0].getName()
                    sellingQuantity = asks[0].getQuantity()
                    sellingPrice = asks[0].getStrike()
                    buyerName = bids[0].getName()
                    buyingQuantity = bids[0].getQuantity()
                    buyingPrice = bids[0].getStrike()
                    fillQuantity = min(sellingQuantity, buyingQuantity)
                    settlePrice = (buyingPrice + sellingPrice) / 2
                    self.world[sellerName]["cash"] = self.world[sellerName]["cash"] + settlePrice * fillQuantity
                    self.reserves[sellerName][ticker] = self.reserves[sellerName][ticker] - fillQuantity
                    self.world[buyerName][ticker] = self.world[buyerName][ticker] + fillQuantity
                    self.reserves[buyerName]["cash"] = self.reserves[buyerName]["cash"] -  settlePrice * fillQuantity
                    #only reserves required amount of cash for the bidder
                    requiredReservedCash = buyingPrice * (buyingQuantity - fillQuantity)
                    #return the extra back to the bidder
                    self.world[buyerName]["cash"] = self.world[buyerName]["cash"] + (self.reserves[buyerName]["cash"] - requiredReservedCash)
                    deal = {"seller": sellerName, "buyer": buyerName, "price": settlePrice, "quantity": fillQuantity}
                    print(ticker, ":", deal)
                    if ticker not in self.history.keys():
                        self.history[ticker] = []
                    self.history[ticker].append(deal)
                    asks[0].setQuantity(sellingQuantity - fillQuantity)
                    bids[0].setQuantity(buyingQuantity - fillQuantity)
                    if not asks[0].getQuantity():
                        asks.pop(0)
                    if not bids[0].getQuantity():
                        bids.pop(0)
        #update the expirations for the orders
        for ticker in self.asks.keys():
            for order in self.asks[ticker]:
                if order.getExpiration() != -1:
                    order.setExpiration(order.getExpiration() - 1)
        for ticker in self.bids.keys():
            for order in self.bids[ticker]:
                if order.getExpiration() != -1:
                    order.setExpiration(order.getExpiration() - 1)
        #clear out expired orders
        for ticker in self.asks.keys():
            validAsks = []
            for order in self.asks[ticker]:
                if order.getExpiration() == 0:
                    self.world[order.getName()][ticker] = self.world[order.getName()][ticker] + order.getQuantity()
                    self.reserves[order.getName()][ticker] = self.reserves[order.getName()][ticker] - order.getQuantity()
                else:
                    validAsks.append(order)
            self.asks[ticker] = validAsks
        for ticker in self.bids.keys():
            validBids = []
            for order in self.bids[ticker]:
                if order.getExpiration() == 0:
                    self.world[order.getName()]["cash"] = self.world[order.getName()]["cash"] + order.getQuantity() * order.getStrike()
                    self.reserves[order.getName()]["cash"] = self.reserves[order.getName()]["cash"] - order.getQuantity() * order.getStrike()
                else:
                    validBids.append(order)
            self.bids[ticker] = validBids
    
    def quotePrice(self, ticker):
        sellPrice = float("-inf")
        buyPrice = float("inf")
        if ticker in self.bids.keys() and self.bids[ticker]:
            sellPrice = self.bids[ticker][0].getStrike()
        if ticker in self.asks.keys() and self.asks[ticker]:
            buyPrice = self.asks[ticker][0].getStrike()
        return {"buyingPrice": buyPrice, "sellingPrice": sellPrice}
    
    def getReserves(self, name):
        if name in self.reserves:
            return self.reserves[name]
    
    def printBuySide(self, ticker = "all"):
        print("Buy side orders for " + ticker)
        if ticker == "all":
            for ticker in self.bids.keys():
                print("For " + ticker)
                for order in self.bids[ticker]:
                    print(order.toString())
        else:
            if ticker in self.bids.keys():
                for order in self.bids[ticker]:
                    print(order.toString())
    
    def printSellSide(self, ticker = "all"):
        print("Sell side orders for " + ticker)
        if ticker == "all":
            for ticker in self.asks.keys():
                print("For " + ticker)
                for order in self.asks[ticker]:
                    print(order.toString())
        else:
            if ticker in self.asks.keys():
                for order in self.asks[ticker]:
                    print(order.toString())
    
    def printOrderBook(self, ticker = "all"):
        if ticker != "all":
            print("--------------" + ticker + "--------------")
            print("-------------Asks-------------")
            if ticker in self.asks.keys():
                for order in reversed(self.asks[ticker]):
                    print(order.toString())
            print("-------------Bids-------------")
            if ticker in self.bids.keys():    
                for order in self.bids[ticker]:
                    print(order.toString())
            