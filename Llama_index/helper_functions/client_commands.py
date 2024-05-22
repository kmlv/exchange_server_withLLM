"""
Helper functions that allow generated strategies to retrieve information
from a client. 
NOTE: if you add any additional functions here you must add a description
      in Llama_index\system_data\helper_function_descriptions to help ChatGPT understand
      what it does and how to use it.
"""
import requests
import json
import toml
with open('./market_client/config.toml', 'r') as f:
        config = toml.load(f)
        _CLIENT_ADDR = config['client']['addr']
        _CLIENT_PORT = config['client']['flask_port']

def account_info():
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to retrieve the account information of the Client.
       To be used by active_strategy() in active_strategy.py whenever it should access the Client's account information.
        Returns:
            dictionary containing the keys ["id", "balance", "active_orders", "owned_shares"]
    """
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["account"]

def get_client_order_history():
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to retrieve the order history of the Client.
       To be used by active_strategy() in active_strategy.py whenever it should access the Client's order history.
        Returns:
            dictionary containing the keys ["price", "quantity", "direction", "timestamp"]
    """
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["order_history"]

def get_book_history():
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to retrieve the Exchange's Order Book History stored in the Client's local log file.
       To be used by active_strategy() in active_strategy.py whenever it should access the Exchange's Order Book History.
        Returns:
            market_data, which is a list of JSON-formatted CDABook entries found in the book log file.
    """
    market_data = list()
    with open(f"market_client/market_logs/book_log.txt", mode="r") as f:
        for line in f:
            entry = json.loads(line)

            market_data.append(entry)
    market_data.reverse()
    return market_data

def get_transaction_history():
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to retrieve the Exchange's Transaction History stored in the Client's local log file.
       To be used by active_strategy() in active_strategy.py whenever it should access the Exchange's Transaction History.
        Returns:
            market_data, which is a list of JSON-formatted order transaction entries found in the transaction log file.
    """
    market_data = list()
    with open(f"market_client/market_logs/transaction_log.txt", mode="r") as f:
        for line in f:
            entry = json.loads(line)
            market_data.append(entry)
    market_data.reverse()
    return market_data

def get_account_history():
    """Sends an HTTP request to the Client object with address _CLIENT_ADDR and port _CLIENT_PORT, to retrieve the Client's account info history stored in the Client's local log file.
       To be used by active_strategy() in active_strategy.py whenever it should access the Client's account info history.
        Returns:
            client_data, which is a list of JSON-formatted account_info() entries found in the client's state log file.
    """
    client_data = list()
    with open(f"market_client/market_logs/state_log.txt", mode="r") as f:
        for line in f:
            entry = json.loads(line)
            client_data.append(entry)
    client_data.reverse()
    return client_data
