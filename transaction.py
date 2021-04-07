class Transaction:
    #expects order format:
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
            self.market.submitBuyOrders(self.order, self.name)
        if self.orderType == "sell":
            self.market.submitSellOrders(self.order, self.name)
