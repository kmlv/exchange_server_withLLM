"""
Helper functions that allow generated strategies to retrieve information
from a client. 
NOTE: if you add any additional functions here you must add a description
      in Llama_index\system_data\helper_function_descriptions to help ChatGPT understand
      what it does and how to use it.
"""
import requests
import json
_CLIENT_ADDR = "localhost"
_CLIENT_PORT = "5001"



def account_info():
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["account"]

def get_order_book():
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["book"]

def get_market_history():
    client_id = account_info()["id"]
    market_data = list()
    with open(f"market_client/market_logs/book_log_{client_id}.txt", mode="r") as f:
        for line in f:
            entry = json.loads(line)

            market_data.append(entry)
    market_data.reverse()
    return market_data

    
def get_order_history():
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["order_history"]

def get_market_history_logfiles():
    client_id = account_info()["id"]
    book_log_file = open(f"market_client/market_logs/book_log_{client_id.decode()}.txt", mode="r")
    transaction_log_file = open(f"market_client/market_logs/transaction_log_{client_id.decode()}.txt", mode="r")
    return book_log_file, transaction_log_file