import sys
sys.path.append('../')
from market import Market

C1 = {"R1": 1000, "R2": 1500, "R3": 400, "cash": 7000}
C2 = {"R1": 100, "R2": 5000, "R3": 450, "cash": 5000}
C3 = {"R1": 700, "R2": 500, "R3": 2000, "cash": 10000}
world = {"C1": C1, "C2": C2, "C3": C3}
market = Market(world)

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
market.submitBuyOrders(limitBuyOrderC1, "C1")
market.submitSellOrders(limitSellOrderC1, "C1")
market.submitBuyOrders(limitBuyOrderC2, "C2")
market.submitSellOrders(limitSellOrderC2, "C2")
market.submitBuyOrders(limitBuyOrderC3, "C3")
market.submitSellOrders(limitSellOrderC3, "C3")

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
print()

print("-----Settled Trades-----")
market.settle()
print("------------------------")
print()

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