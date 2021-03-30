#work in progress
class Order:
    def __init__(self, quantity: int, name: str, strike = -1, expiration = -1):
        self.quantity = quantity
        self.name = name
        self.strike = strike
        self.expiration = expiration
    
    def __lt__(self, other):
        if isinstance(other, Order):
            return self.strike < other.strike
        else:
            return False
        
    def __le__(self, other):
        if isinstance(other, Order):
            return self.strike <= other.strike
        else:
            return False
    
    def setExpiration(self, expiration):
        self.expiration = expiration
    
    def setQuantity(self, quantity):
        self.quantity = quantity
        
    def getQuantity(self):
        return self.quantity
    
    def getStrike(self):
        return self.strike
    
    def getExpiration(self):
        return self.expiration
    
    def getName(self):
        return self.name
    
    def toString(self):
        output = "Strike: " + str(self.strike) + ". Quantity: " + str(self.quantity) + ". "
        if self.expiration != -1:
            output = output + "Expires in " + str(self.expiration) + ". "
        output = output + self.name
        return output

#work in progress
class Market:
    def __init__(self, world):
        self.bids = {}
        self.asks = {}
        self.buyers = {}
        self.sellers = {}
        self.reserves = {}
        
    def submitLimitBuy(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.bids.keys():
                self.bids[ticker] = []
            liquidity = self.bids[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = order["strike"]
                limitBuyOrder = Order(quantity, name, strike)
                if "expiration" in order.keys():
                    limitBuyOrder.setExpiration(order["expiration"])
                liquidity.append(limitBuyOrder)
                liquidity.sort(reverse = True)
                if name not in self.reserves:
                    self.reserves[name] = {}
                if "cash" not in self.reserves[name]:
                    self.reserves[name] = 0
                self.reserves[name]["cash"] = self.reserves[name]["cash"] + quantity * strike
                self.world[name]["cash"] = self.world[name]["cash"] - quantity * strike
    
    def submitLimitSell(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.asks.keys():
                self.asks[ticker] = []
            liquidity = self.asks[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = order["strike"]
                limitSellOrder = Order(quantity, name, strike)
                if "expiration" in order.keys():
                    limitSellOrder.setExpiration(order["expiration"])
                liquidity.append(limitSellOrder)
                liquidity.sort()
                if name not in self.reserves:
                    self.reserves[name] = {}
                if ticker not in self.reserves[name]:
                    self.reserves[name][ticker] = 0
                self.reserves[name][ticker] = self.reserves[name][ticker] + quantity
                self.world[name][ticker] = self.world[name][ticker] - quantity
    
    def submitMarketBuy(self, orders: dict, name: str):
        for ticker in orders.keys():
                quantity = orders[ticker]["quantity"]
                marketBuyOrder = Order(quantity, name)
                if "expiration" in orders[ticker].keys():
                    marketBuyOrder.setExpiration(orders[ticker]["expiration"])
                if ticker not in self.buyers:
                    self.buyers[ticker] = []
                self.buyers[ticker].append(marketBuyOrder)
                
    def submitMarketSell(self, orders: dict, name: str):
        for ticker in orders.keys():
                quantity = orders[ticker]["quantity"]
                marketSellOrder = Order(quantity, name)
                if "expiration" in orders[ticker].keys():
                    marketSellOrder.setExpiration(orders[ticker]["expiration"])
                if ticker not in self.sellers:
                    self.sellers[ticker] = []
                self.sellers[ticker].append(marketSellOrder)

    def executeMarketBuy(self):
        for ticker in self.buyers.keys():
            for order in self.buyers[ticker]:
                fillQuantity = order.getQuantity()
                liquidity = self.asks[ticker]
                lastPrice = self.quotePrice(ticker)["buyPrice"]
                while liquidity and fillQuantity > 0 and self.world[order.getName()]["cash"] >= lastPrice:
                    bestOffer = liquidity[0]
                    sellerName = bestOffer.getName()
                    sellingQuantity = bestOffer.getQuantity()
                    sellingPrice = bestOffer.getStrike()
                    maxFillingQuantity = min(sellingQuantity, int(self.world[order.getName()]["cash"] / sellingPrice))
                    #modify state
                    self.world[order.getName()][ticker] = self.world[order.getName()][ticker] + maxFillingQuantity 
                    self.world[order.getName()]["cash"] = self.world[order.getName()]["cash"] - maxFillingQuantity  * sellingPrice
                    self.world[sellerName]["cash"] = self.world[sellerName]["cash"] + maxFillingQuantity  * sellingPrice
                    self.reserves[sellerName][ticker] = self.reserves[sellerName][ticker] - maxFillingQuantity
                    fillQuantity = fillQuantity - maxFillingQuantity
                    liquidity.setQuantity(sellingQuantity - maxFillingQuantity)
                    lastPrice = sellingPrice
                    if not liquidity.getQuantity():
                        liquidity.pop(0)
                if fillQuantity != 0:
                    #note: for now, if a market buy order cannot be fully filled,
                    #      the rest will be converted to a limit buy order with
                    #      the last executed price being the strike
                    limitBuyOrder = Order(fillQuantity, order.getName(), lastPrice, order.getExpiration())
                    self.bids[ticker].append(limitBuyOrder)
                    self.bids[ticker].sort(reverse = True)
            
    def executeMarketSell(self):
        for ticker in self.sellers.keys():
            for order in self.sellers[ticker]:
                fillQuantity = order.getQuantity()
                liquidity = self.bids[ticker]
                lastPrice = self.quotePrice(ticker)["sellPrice"]
                while liquidity and fillQuantity > 0:
                    bestOffer = liquidity[0]
                    buyerName = bestOffer.getName()
                    buyingQuantity = bestOffer.getQuantity()
                    buyingPrice = bestOffer.getStrike()
                    maxFillingQuantity = min(buyingQuantity, fillQuantity)
                    #modify state
                    self.world[order.getName()][ticker] = self.world[order.getName()][ticker] - buyingQuantity
                    self.world[order.getName()]["cash"] = self.world[order.getName()]["cash"] + buyingQuantity * buyingPrice
                    self.world[buyerName][ticker] = self.world[buyerName][ticker] + maxFillingQuantity
                    self.reserves[buyerName]["cash"] = self.reserves[buyerName]["cash"] - maxFillingQuantity * buyingPrice
                    fillQuantity = fillQuantity - maxFillingQuantity
                    liquidity.setQuantity(buyingQuantity - maxFillingQuantity)
                    lastPrice = buyingPrice
                    if not liquidity.getQuantity():
                        liquidity.pop(0)
                if fillQuantity != 0:
                    #note: for now, if a market sell order cannot be fully filled,
                    #      the rest will be converted to a limit sell order with
                    #      the last executed price being the strike
                    limitSellOrder = Order(fillQuantity, order.getName(), lastPrice, order.getExpiration())
                    self.asks[ticker].append(limitSellOrder)
                    self.asks[ticker].sort()
                
    def settle(self):
        #todo: clear expired orders
        self.executeMarketBuy()
        self.executeMarketSell()
    
    def quotePrice(self, ticker):
        sellPrice = float("-inf")
        buyPrice = float("inf")
        if self.bids[ticker]:
            sellPrice = self.bids[ticker][0].getStrike()
        if self.asks[ticker]:
            buyPrice = self.asks[ticker][0].getStrike()
        return {"buyPrice": buyPrice, "sellPrice": sellPrice}
    
    def printBuySide(self):
        print("Buy side orders:")
        for ticker in self.bids.keys():
            print("For " + ticker)
            for order in self.bids[ticker]:
                print(order.toString())
    
    def printSellSide(self):
        print("Sell side orders:")
        for ticker in self.asks.keys():
            print("For " + ticker)
            for order in self.asks[ticker]:
                print(order.toString())
    
    def printOrderBook(self, ticker = "all"):
        if ticker != "all":
            for order in reversed(self.asks[ticker]):
                print(order.toString())
            print("--------------------------------")
            for order in self.bids[ticker]:
                print(order.toString())
            