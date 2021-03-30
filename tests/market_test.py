import sys
sys.path.append('../')

from market import Order, Market

#test toString()
order1 = Order(100, "C1", 120, 10)
print(order1.toString())
order2 = Order(100, "C1", float("inf"))
print(order2.toString())

#test < and <=
print(order1 < order2) #true
print(order1 <= order2) #true

market = Market({})
limitBuyOrder1 = {
    "R1": [{"quantity": 100, "strike": 100}, {"quantity": 130, "strike": 120}, {"quantity": 1300, "strike": 97}],
    "R2": [{"quantity": 560, "strike": 1250, "expiration": 10}, {"quantity": 300, "strike": 1000}]
}
market.submitLimitBuy(limitBuyOrder1, "C1")

limitSellOrder1 = {
    "R1": [{"quantity": 10, "strike": 150}, {"quantity": 100, "strike": 130}, {"quantity": 500, "strike": 165}],
    "R2": [{"quantity": 300, "strike": 1400}, {"quantity": 500, "strike": 1700}]
}
market.submitLimitSell(limitSellOrder1, "C2")

#market.printBuySide()
#market.printSellSide()

#start the simulation with more buyers than sellers
market.printOrderBook("R1")
quote = market.quotePrice("R1");
print("Buy at:", quote["buyPrice"], "Sell at:", quote["sellPrice"])

print()
marketBuyOrder1 = {"R1": {"quantity": 50}}
market.submitMarketBuy(marketBuyOrder1, "C3")
market.settle()
market.printOrderBook("R1")
quote = market.quotePrice("R1");
print("Buy at:", quote["buyPrice"], "Sell at:", quote["sellPrice"])


print()
marketBuyOrder2 = {"R1": {"quantity": 70}}
market.submitMarketBuy(marketBuyOrder2, "C3")
market.settle()
market.printOrderBook("R1")
quote = market.quotePrice("R1");
print("Buy at:", quote["buyPrice"], "Sell at:", quote["sellPrice"])

print()
marketBuyOrder3 = {"R1": {"quantity": 1000}}
market.submitMarketBuy(marketBuyOrder3, "C3")
market.settle()
market.printOrderBook("R1")
quote = market.quotePrice("R1");
print("Buy at:", quote["buyPrice"], "Sell at:", quote["sellPrice"])