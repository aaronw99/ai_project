import sys
sys.path.append('../')
from market import Market

#todo: sanity check => total amount of each resource or cash stays constant
#                      after market settles. I've verified by hand calculation.
#                      but going forward we need explicit unit tests for this.
C1 = {"R1": 1000, "R2": 1500, "R3": 400, "cash": 7000}
C2 = {"R1": 100, "R2": 5000, "R3": 450, "cash": 5000}
C3 = {"R1": 700, "R2": 500, "R3": 2000, "cash": 10000}
world = {"C1": C1, "C2": C2, "C3": C3}
market = Market()

limitBuyOrderC1 = {
    "R3": [{"quantity": 200, "strike": 10, "expiration": 3}, {"quantity": 300, "strike": 11}]
}
limitSellOrderC1 = {
    "R1": [{"quantity": 50, "strike": 30}, {"quantity": 130, "strike": 25}],
    "R2": [{"quantity": 100, "strike": 10}, {"quantity": 100, "strike": 13}, {"quantity": 200, "strike": 15}]
}
limitBuyOrderC2 = {
    "R1": [{"quantity": 200, "strike": 10, "expiration": 1}, {"quantity": 200, "strike": 5, "expiration": 3}, {"quantity": 100, "strike": 2}],
    "R3": [{"quantity": 100, "strike": 5}, {"quantity": 200, "strike": 2}]
}
limitSellOrderC2 = {
    "R2": [{"quantity": 1000, "strike": 8}, {"quantity": 1000, "strike": 10}, {"quantity": 500, "strike": 15}]
}
limitBuyOrderC3 = {
    "R1": [{"quantity": 50, "strike": 20, "expiration": 4}],
    "R2": [{"quantity": 500, "strike": 10, "expiration": 2}, {"quantity": 300, "strike": 12}]
}
limitSellOrderC3 = {
    "R3": [{"quantity": 1000, "strike": 4}, {"quantity": 500, "strike": 2}]
}
#round 1 actions
market.submitBuyOrders(limitBuyOrderC1, "C1", world)
market.submitSellOrders(limitSellOrderC1, "C1", world)
market.submitBuyOrders(limitBuyOrderC2, "C2", world)
market.submitSellOrders(limitSellOrderC2, "C2", world)
market.submitBuyOrders(limitBuyOrderC3, "C3", world)
market.submitSellOrders(limitSellOrderC3, "C3", world)

#before market settles
print("------------Market------------")
market.printOrderBook("R1")
print()
market.printOrderBook("R2")
print()
market.printOrderBook("R3")
print("------------------------------")
print()

print("World state:", world)
reservesC1 = market.getReserves("C1")
reservesC2 = market.getReserves("C2")
reservesC3 = market.getReserves("C3")
print("Reserves for C1:", reservesC1)
print("Reserves for C2:", reservesC2)
print("Reserves for C3:", reservesC3)
print("R1 Price:", market.quotePrice("R1"))
print("R2 Price:", market.quotePrice("R2"))
print("R3 Price:", market.quotePrice("R3"))
print()

#market settles
print("-----Settled Trades-----")
market.settle(world)
print("------------------------")
print()

#after market settles
print("------------Market------------")
market.printOrderBook("R1")
print()
market.printOrderBook("R2")
print()
market.printOrderBook("R3")
print("------------------------------")
print()

print("World state:", world)
reservesC1 = market.getReserves("C1")
reservesC2 = market.getReserves("C2")
reservesC3 = market.getReserves("C3")
print("Reserves for C1:", reservesC1)
print("Reserves for C2:", reservesC2)
print("Reserves for C3:", reservesC3)
print("R1 Price:", market.quotePrice("R1"))
print("R2 Price:", market.quotePrice("R2"))
print("R3 Price:", market.quotePrice("R3"))
print()

#round 2
limitBuyOrderC1 = {
    "R2": [{"quantity": 100, "strike": 6}, {"quantity": 100, "strike": 4}]
}
market.submitBuyOrders(limitBuyOrderC1, "C1", world)

marketBuyOrderC3 = {
    "R2": [{"quantity": 500, "strike": 8}]
}
market.submitBuyOrders(marketBuyOrderC3, "C3", world)

#before market settles
print("------------Market------------")
market.printOrderBook("R1")
print()
market.printOrderBook("R2")
print()
market.printOrderBook("R3")
print("------------------------------")
print()

print("World state:", world)
reservesC1 = market.getReserves("C1")
reservesC2 = market.getReserves("C2")
reservesC3 = market.getReserves("C3")
print("Reserves for C1:", reservesC1)
print("Reserves for C2:", reservesC2)
print("Reserves for C3:", reservesC3)
print("R1 Price:", market.quotePrice("R1"))
print("R2 Price:", market.quotePrice("R2"))
print("R3 Price:", market.quotePrice("R3"))
print()

#market settles
print("-----Settled Trades-----")
market.settle(world)
print("------------------------")
print()

#after market settles
print("------------Market------------")
market.printOrderBook("R1")
print()
market.printOrderBook("R2")
print()
market.printOrderBook("R3")
print("------------------------------")
print()

print("World state:", world)
reservesC1 = market.getReserves("C1")
reservesC2 = market.getReserves("C2")
reservesC3 = market.getReserves("C3")
print("Reserves for C1:", reservesC1)
print("Reserves for C2:", reservesC2)
print("Reserves for C3:", reservesC3)
print("R1 Price:", market.quotePrice("R1"))
print("R2 Price:", market.quotePrice("R2"))
print("R3 Price:", market.quotePrice("R3"))
print()

print("Price history for R1:", market.getHistory("R1"))
print("Price history for R2:", market.getHistory("R2"))
print("Price history for R3:", market.getHistory("R3"))
print("Buy side for R1", market.getBuyOrders("R1"))
print("Buy side for R2", market.getBuyOrders("R2"))
print("Buy side for R3", market.getBuyOrders("R3"))
