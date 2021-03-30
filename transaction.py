class Transaction:
    def __init__(self, country, orderType, order, market):
        self.country = country
        self.orderType = orderType
        self.order = order
        self.market = market
    
    def execute(self):
        if self.orderType == "buy":
            self.market.submitBuyOrders(self.order, self.country)
        if self.orderType == "sell":
            self.market.submitSellOrders(self.order, self.country)
