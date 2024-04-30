from helper_functions.market_commands import *
from helper_functions.client_commands import *

def CDA_order(shares: int, price: int, direction: str):
    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": 50}
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)
    resp = requests.request("POST", "http://localhost:5000/place_order", json=data)

def active_strategy():
    CDA_order(2, 2, 'B')

if __name__ == '__main__':
    active_strategy()