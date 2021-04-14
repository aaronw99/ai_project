class Transaction:
    #expects the following order format:
    #{
    #   ticker1: [
    #               {
    #                   "quantity": [required], 
    #                   "strike": [required],
    #                   "expiration": [optional]
    #               },
    #               {
    #                   "quantity": [required].
    #                   "strike": [required],
    #                   "expiration": [optional]
    #               },
    #               ...
    #             ],
    #   ticker2: [
    #               {same as above},
    #               ...
    #            ]
    #}
    def __init__(self, name, orderType, order, market):
        self.name = name
        self.orderType = orderType
        self.order = order
        self.market = market
    
    def execute(self, world):
        if self.orderType == "buy":
            self.market.submitBuyOrders(self.order, self.name, world)
        if self.orderType == "sell":
            self.market.submitSellOrders(self.order, self.name, world)
    
    def toString(self):
        string = ""
        for ticker in self.order.keys():
            for order in self.order[ticker]:
                if self.orderType == "buy":
                    string = string + "BIDS"
                if self.orderType == "sell":
                    string = string + "ASKS"
                string = string + " FOR " + ticker
                string = string + " STRIKE: " + str(order["strike"])
                string = string + ", QUANTITY: " + str(order["quantity"])
                if "expiration" in order.keys():
                    string = string + ", EXPIRATION: " + str(order["expiration"])
                string = string + "\n"
        return string
        