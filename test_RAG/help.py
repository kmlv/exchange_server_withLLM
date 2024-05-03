import time
import requests
def CDA_order(shares: int, price: int, direction: str):
    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": 50}
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)
    resp = requests.request("POST", "http://localhost:5000/place_order", json=data)

def active_strategy():
def active_strategy():
    buy_stocks = 2
    cost_per_stock = 1
    total_cost = buy_stocks * cost_per_stock
    return total_cost

if __name__ == '__main__':
    active_strategy()