"""Helper functions that allow generated strategies to retrieve information
from a client"""
import requests

def account_info():
    return {"balance" : 100, "orders" : None, "owned_shares" : 13, "order_history": None, "market_history": None}