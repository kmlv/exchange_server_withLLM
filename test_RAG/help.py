import time
import requests

def CDA_order(shares: int, price: int, direction: str):
    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": 10}
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)
    resp = requests.request("GET", "http://localhost:5000/place_order", json=data)


def active_strategy():
    while True:
        CDA_order(1, 5, 'B')
        time.sleep(5)

if __name__ == '__main__':
    active_strategy()
import time

def active_strategy():
    while True:
        CDA_order(4, 5, 'B')
        time.sleep(10)


if __name__ == '__main__':
    active_strategy()