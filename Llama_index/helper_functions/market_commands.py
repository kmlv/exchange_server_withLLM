"""
Helper functions that allow generated strategy to communicate with the Market
NOTE: if you add any additional functions here you must add a description
      in Llama_index\system_data\helper_function_descriptions.txt to help ChatGPT understand
      what it does and how to use it.
"""
import time
import requests
import json
_CLIENT_ADDR = "localhost"
_CLIENT_PORT = "5001"

def CDA_order(shares: int, price: int, direction: str):
    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": 100}
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)

    try: 
        resp = requests.request("POST", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/place_order", json=data)
        placed_order_token = resp.json()['order_token']
        return placed_order_token
    except (json.decoder.JSONDecodeError, KeyError):
        return None


def CDA_order_cancel(token: int):
    print("Cancelling order: ", token, time.time(), flush=True)
    resp = requests.request("POST", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/cancel/{token}", json=dict())

# TODO: this is currently just returning hard-coded values.
def best_offer():
    return {"best_buy":4, "best_sell":9}