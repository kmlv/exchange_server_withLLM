"""
Helper functions that allow generated strategies to retrieve information
from a client. 
NOTE: if you add any additional functions here you must add a description
      in Llama_index\system_data\helper_function_descriptions to help ChatGPT understand
      what it does and how to use it.
"""
import requests
import re
_CLIENT_ADDR = "localhost"
_CLIENT_PORT = "5001"

timestamp_line_pattern = 'timestamp: \d+'

def account_info():
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["account"]

def get_order_book():
    # get latest entry in order book history log file
    book_history_logfile = get_book_history_logfile()
    # start at end of the file
    # search each line for "Book Log Entry"
    # then parse the lines starting below "Book Log Entry" until "End of Entry" is reached
    last_line = None
    last_entry_position = None
    book_timestamp = None
    print("READING LOG FILE FOR BOOK")
    for i, line in enumerate(book_history_logfile):
        print(f"line {i}: {line}")
        if "book log entry:" in line.lower():
            last_line = line
            last_entry_position = i
        elif "timestamp: " in line.lower():
            # https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python
            book_timestamp = int(re.search(timestamp_line_pattern, line).string)
        #last_book_min_bid = 0


    if last_line:
        print(f"last log entry at pos[{last_entry_position}]: {last_line}")
        return {"timestamp" : book_timestamp, "min_bid" : 0, "max_ask" : 0}

    return None

def get_order_history():
    response = requests.request("GET", f"http://{_CLIENT_ADDR}:{_CLIENT_PORT}/info", json=dict())
    return response.json()["order_history"]

def get_market_history_logfiles():
    client_id = account_info()["id"]
    book_log_file = open(f"market_client/market_logs/book_log_{client_id}.txt", mode="r")
    transaction_log_file = open(f"market_client/market_logs/transaction_log_{client_id}.txt", mode="r")
    return book_log_file, transaction_log_file

def get_book_history_logfile():
    client_id = account_info()["id"]
    return open(f"market_client/market_logs/book_log_{client_id}.txt", mode="r")

def get_transaction_history_logfile():
    client_id = account_info()["id"]
    return open(f"market_client/market_logs/transaction_log_{client_id}.txt", mode="r")

# TODO: this is currently just returning hard-coded values.
def best_offer():
    return {"best_buy":4, "best_sell":9}