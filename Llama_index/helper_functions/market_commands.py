"""Helper functions that allow generated strategy to communicate with the Market"""
import time
import requests

def CDA_order(shares: int, price: int, direction: str):
    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": 10}
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)
    resp = requests.request("POST", "http://localhost:5001/place_order", json=data)
    # TODO: return the token of the placed order

def CDA_order_cancel(token: int):
    print("Cancelling order: ", token, time.time(), flush=True)
    resp = requests.request("POST", "http://localhost:5001/cancel/{token}", json=dict())

# TODO: this is currently just returning hard-coded values.
def best_offer():
    return {"best_buy":4, "best_sell":9}