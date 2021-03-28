import copy

class Order:
    def __init__(self, quantity: int, strike: float, name: str, expiration = -1):
        self.quantity = quantity
        self.strike = strike
        self.name = name
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
    
    def toString(self):
        output = "Strike: " + str(self.strike) + ". Quantity: " + str(self.quantity) + ". "
        if self.expiration != -1:
            output = output + "Expires in " + str(self.expiration) + ". "
        output = output + self.name
        return output

#work in progress
class Market:
    def __init__(self):
        self.inventory = {}
        self.bids = {}
        self.asks = {}
        
    def submitLimitBuy(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.bids.keys():
                self.bids[ticker] = []
            liquidity = self.bids[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = order["strike"]
                limitBuyOrder = Order(quantity, strike, name)
                if "expiration" in order.keys():
                    limitBuyOrder.setExpiration(order["expiration"])
                liquidity.append(limitBuyOrder)
                liquidity.sort(reverse = True)
    
    def submitLimitSell(self, orders: dict, name: str):
        for ticker in orders.keys():
            if ticker not in self.asks.keys():
                self.asks[ticker] = []
            liquidity = self.asks[ticker]
            for order in orders[ticker]:
                quantity = order["quantity"]
                strike = order["strike"]
                limitSellOrder = Order(quantity, strike, name)
                if "expiration" in order.keys():
                    limitSellOrder.setExpiration(order["expiration"])
                liquidity.append(limitSellOrder)
                liquidity.sort()

    def submitMarketBuy(self, orders: dict, name: str):
        for ticker in orders.keys():
            fillQuantity = orders[ticker]
            liquidity = self.asks[ticker]
            lastPrice = -1
            while liquidity and fillQuantity > 0:
                quantity = liquidity[0].getQuantity()
                lastPrice = liquidity[0].getStrike()
                if fillQuantity > quantity:
                    #todo: modify state
                    fillQuantity = fillQuantity - quantity
                    liquidity.pop(0)
                else:
                    liquidity[0].setQuantity(quantity - fillQuantity)
                    fillQuantity = 0
            if fillQuantity != 0:
                #note: for now, if a market buy order cannot be fully filled,
                #      the rest will be converted to a limit buy order with
                #      the last executed price being the strike
                limitBuyOrder = Order(fillQuantity, lastPrice, name)
                if "expiration" in orders.keys():
                    limitBuyOrder.setExpiration(orders["expiration"])
                self.bids[ticker].append(limitBuyOrder)
                self.bids[ticker].sort(reverse = True)
                
            
    def submitMarketSell(self, orders: dict, name: str):
        for ticker in orders.keys():
            fillQuantity = orders[ticker]
            liquidity = self.bids[ticker]
            lastPrice = -1
            while liquidity and fillQuantity > 0:
                quantity = liquidity[0].getQuantity()
                lastPrice = liquidity[0].getStrike()
                if fillQuantity > quantity:
                    #todo: modify state
                    fillQuantity = fillQuantity - quantity
                    liquidity.pop(0)
                else:
                    liquidity[0].setQuantity(quantity - fillQuantity)
                    fillQuantity = 0
            if fillQuantity != 0:
                #note: for now, if a market sell order cannot be fully filled,
                #      the rest will be converted to a limit sell order with
                #      the last executed price being the strike
                limitSellOrder = Order(fillQuantity, lastPrice, name)
                if "expiration" in orders.keys():
                    limitSellOrder.setExpiration(orders["expiration"])
                self.asks[ticker].append(limitSellOrder)
                self.asks[ticker].sort()
    
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
            