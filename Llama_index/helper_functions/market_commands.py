"""
Helper functions that allow generated strategy to communicate with the Market
NOTE: if you add any additional functions here you must add a description
      in Llama_index\system_data\helper_function_descriptions.txt to help ChatGPT understand
      what it does and how to use it.
"""
import time
import requests
import json
import toml
import datetime
import pytz

DEFAULT_TIMEZONE = pytz.timezone('US/Pacific')

with open('./market_client/config.toml', 'r') as f:
        config = toml.load(f)
        _CLIENT_ADDR = config['client']['addr']
        _CLIENT_PORT = config['client']['flask_port']

def CDA_order(shares: int, price: int, direction: str, time_in_force: int):
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to place an order in the Exchange server market.
       To be used by active_strategy() in active_strategy.py whenever it should place an order.
        Args:
            shares: number of shares of the placed order
            price: price of the placed order
            direction: 'B' for buy order, 'S' for sell order
            time_in_force: max amount of time the placed order should remain in the market
        Returns:
            token: The token id of the placed order. Returns None if the order could not be placed.
    """

    data = {"quantity" : shares, "price" : price, "direction" : direction, "time": time_in_force}
    print("Placing order: ", direction, shares, "@", price, "lasting ", time_in_force, "s at ", time.time(), flush=True)

    try: 
        resp = requests.request("POST", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/place_order", json=data)
        placed_order_token = resp.json()['order_token']
        return placed_order_token
    except (json.decoder.JSONDecodeError, KeyError):
        return None


def CDA_order_cancel(token: int):
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to cancel an order placed by the Client in the Exchange server market.
       To be used by active_strategy() in active_strategy.py whenever it should cancel an order.
        Args:
            token: token id of the order to be cancelled.
    """
    print("Cancelling order: ", token, time.time(), flush=True)
    resp = requests.request("POST", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/cancel/{token}", json=dict())

def get_current_time(tz=DEFAULT_TIMEZONE):
    now = datetime.datetime.now(tz=tz)
    timestamp = 0  # since midnight
    timestamp += now.hour
    timestamp *= 60  # hours -> minutes
    timestamp += now.minute
    timestamp *= 60  # minutes -> seconds
    timestamp += now.second
    timestamp *= 10**6  # seconds -> microsecnds
    timestamp += now.microsecond
    timestamp *= 10**3  # microseconds -> nanoseconds
    return timestamp