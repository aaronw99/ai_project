# The Transaction class represents an order to be submitted to the market
class Transaction:
    #__init__
    # @name(str): the name of the issuer
    # @orderType(str): either "buy" or "sell"
    # @order(dict): the content of the order
    # @market(obj): the market
    # note: @order expects the following format:
    # { 
    #    ticker1: [
    #                {
    #                    "quantity": [required], 
    #                    "strike": [required],
    #                    "expiration": [optional]
    #                },
    #                {
    #                    "quantity": [required].
    #                    "strike": [required],
    #                    "expiration": [optional]
    #                },
    #                ...
    #              ],
    #    ticker2: [
    #                {same as above},
    #                ...
    #             ]
    # }
    # this constructs the Transaction object
    def __init__(self, name, orderType, order, market):
        self.name = name
        self.orderType = orderType
        self.order = order
        self.market = market
    
    # execute
    # @world(dict): the state of the world
    # this submits the order to the market
    def execute(self, world):
        if self.orderType == "buy":
            self.market.submitBuyOrders(self.order, self.name, world)
        if self.orderType == "sell":
            self.market.submitSellOrders(self.order, self.name, world)
    
    # toString
    # this converts the order to a readable string
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
