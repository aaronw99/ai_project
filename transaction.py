class Transaction:
    def __init__(self, country, orderType, order, market):
        self.country = country
        self.orderType = orderType
        self.order = order
        self.market = market
    
    def execute(self):
        if self.orderType == "limit buy":
            self.market.submitLimitBuy(self.order, self.country)
        if self.orderType == "limit sell":
            self.market.submitLimitSell(self.order, self.country)
        if self.orderType == "market buy":
            self.market.submitMarketBuy(self.order, self.country)
        if self.orderType == "market sell":
            self.market.submitMarketSell(self.order, self.country)
