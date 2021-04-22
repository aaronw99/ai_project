# The Order class represents a bid or an ask for a given resource
class Order:
    # __init___
    # this constructs the Order object with the given parameters
    # @name(str): the name of issuer
    # @quantity(int): quantity
    # @strike(float): the strike price
    # @expiration(int): the time period during which the order is valid
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
    
    def toDict(self):
        d = {}
        d["strike"] = self.strike
        d["quantity"] = self.quantity
        d["name"] = self.name
        if self.expiration != -1:
            d["expiration"] = self.expiration
        return d

# The Market class represents an exchange center that matches buyers and sellers
# See tests/market_test.py for a demo
class Market:
    # __init___
    # this constructs the Market object  
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.reserves = {}
        self.history = {}
    
    # submitBuyOrders
    # this adds the given orders to the bid heap
    # @orders(dict): the orders. See transaction.py for the expected format
    # @name(str): name of the issuer
    # @world(dict): the state of the world
    def submitBuyOrders(self, orders: dict, name: str, world: dict):
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
                world[name]["cash"] = world[name]["cash"] - quantity * strike
    
    # submitSellOrders
    # this adds the given orders to the ask heap
    # @orders(dict): the orders. See transaction.py for the expected format
    # @name(str): name of the issuer
    # @world(dict): the state of the world
    def submitSellOrders(self, orders: dict, name: str, world: dict):
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
                world[name][ticker] = world[name][ticker] - quantity
    
    # settle
    # this settles the market by matching available buy and sell orders,
    # updating the validity of the orders, removing the expired orders,
    # and returning extra reserves to their owners
    # @world(dict): the state of the world
    def settle(self, world: dict):
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
                    world[sellerName]["cash"] = world[sellerName]["cash"] + settlePrice * fillQuantity
                    self.reserves[sellerName][ticker] = self.reserves[sellerName][ticker] - fillQuantity
                    world[buyerName][ticker] = world[buyerName][ticker] + fillQuantity
                    self.reserves[buyerName]["cash"] = self.reserves[buyerName]["cash"] -  settlePrice * fillQuantity
                    #only reserves required amount of cash for the bidder
                    self.reserves[buyerName]["cash"] = self.reserves[buyerName]["cash"] - (buyingPrice - settlePrice) * fillQuantity
                    world[buyerName]["cash"] = world[buyerName]["cash"] + (buyingPrice - settlePrice) * fillQuantity
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
                #return reserves from expired orders
                if order.getExpiration() == 0:
                    world[order.getName()][ticker] = world[order.getName()][ticker] + order.getQuantity()
                    self.reserves[order.getName()][ticker] = self.reserves[order.getName()][ticker] - order.getQuantity()
                else:
                    validAsks.append(order)
            self.asks[ticker] = validAsks
        for ticker in self.bids.keys():
            validBids = []
            for order in self.bids[ticker]:
                #return reserves from expired orders
                if order.getExpiration() == 0:
                    world[order.getName()]["cash"] = world[order.getName()]["cash"] + order.getQuantity() * order.getStrike()
                    self.reserves[order.getName()]["cash"] = self.reserves[order.getName()]["cash"] - order.getQuantity() * order.getStrike()
                else:
                    validBids.append(order)
            self.bids[ticker] = validBids
    
    # quotePrice
    # this returns the best bid and ask prices for a given resource
    # @ticker(str): the name of the resource
    # return: best bidding and asking prices with the following format:
    #         {"buyingPrice": p1, "sellingPrice": p2}
    # note: if no bidding price is available, buyingPrice will be -inf
    #       if no asking price is available, sellingPrice will be inf
    def quotePrice(self, ticker):
        sellPrice = float("-inf")
        buyPrice = float("inf")
        if ticker in self.bids.keys() and self.bids[ticker]:
            sellPrice = self.bids[ticker][0].getStrike()
        if ticker in self.asks.keys() and self.asks[ticker]:
            buyPrice = self.asks[ticker][0].getStrike()
        return {"buyingPrice": buyPrice, "sellingPrice": sellPrice}
    
    # getReserves
    # this returns the reserves of a country in the market
    # @name(str): the name of the country
    # return: the reserves that a country has in the market with the following format:
    #         {"cash": q1, "tickerName1": q2, "tickerName2": q3, ...}
    def getReserves(self, name):
        if name in self.reserves:
            return self.reserves[name]
        else:
            return {}
    
    # getReserves
    # this returns the chronological transaction history for a given resource
    # @ticker(str): the name of the resource
    # return: the chronological transaction history of a given resource 
    #         with the following format
    #         [
    #           {"buyer": b1, "seller": s1, "price": p1, "quantity": q1},
    #           {"buyer": b2, "seller": s2, "price": p2, "quantity": q2},
    #           ...
    #         ]
    def getHistory(self, ticker):
        if ticker in self.history.keys():
            return self.history[ticker]
        else:
            return []
    
    # getBuyOrders
    # this returns all the buy orders for a given resource, organized
    # from best to worst
    # @ticker(str): the name of the resource
    # return: the buy orders for a given resource, organized
    #         from best to worst, with the following format:
    #         [
    #           {"strike": s1, "quantity": q1, "name": n1, "expiration": e1 [optional]},
    #           {"strike": s2, "quantity": q2, "name": n2, "expiration": e2 [optional]},
    #           ...
    #         ]
    def getBuyOrders(self, ticker):
        orders = []
        if ticker in self.bids.keys():
            for order in self.bids[ticker]:
                orders.append(order.toDict())
        return orders
    
    # getSellOrders
    # this returns all the sell orders for a given resource, organized
    # from best to worst
    # @ticker(str): the name of the resource
    # return: the buy orders for a given resource, organized
    #         from best to worst, with the following format:
    #         [
    #           {"strike": s1, "quantity": q1, "name": n1, "expiration": e1 [optional]},
    #           {"strike": s2, "quantity": q2, "name": n2, "expiration": e2 [optional]},
    #           ...
    #         ]
    def getSellOrders(self, ticker):
        orders = []
        if ticker in self.asks.keys():
            for order in self.asks[ticker]:
                orders.append(order.toDict())
        return orders
    
    # getOrders
    # this returns all the orders for a given resource, organized
    # from best to worst respectively
    # @ticker(str): the name of the resource
    # return: all bids and asks of a given resource, organized
    #         from best to worst respectively, with the following format:
    #        {
    #           "bids": [
    #                       {"strike": s1, "quantity": q1, "name": n1, "expiration": e1 [optional]},
    #                       {"strike": s2, "quantity": q2, "name": n2, "expiration": e2 [optional]},
    #                       ...
    #                   ],
    #           "asks": [
    #                       {"strike": s1, "quantity": q1, "name": n1, "expiration": e1 [optional]},
    #                       {"strike": s2, "quantity": q2, "name": n2, "expiration": e2 [optional]},
    #                       ...
    #                   ]
    #        }
    def getOrders(self, ticker):
        book = {}
        book["bids"] = self.getBuyOrders(ticker)
        book["asks"] = self.getSellOrders(ticker)
        return book
    
    # these are util functions for testing and visualization purposes
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
            print("------------------------------")
            print()
        
        else:
            tickers = set()
            for ticker in self.asks.keys():
                tickers.add(ticker)
            for ticker in self.bids.keys():
                tickers.add(ticker)
            for ticker in tickers:
                print("--------------" + ticker + "--------------")
                print("-------------Asks-------------")
                if ticker in self.asks.keys():
                    for order in reversed(self.asks[ticker]):
                        print(order.toString())
                print("-------------Bids-------------")
                if ticker in self.bids.keys():    
                    for order in self.bids[ticker]:
                        print(order.toString())
                print("------------------------------")
                print()