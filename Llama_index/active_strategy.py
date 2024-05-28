# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

# Start of Generated Code
import time
import random

def active_strategy():
    while True:
        try:
            current_balance = account_info()["balance"]
            if current_balance > 100:
                order_token = CDA_order(3, 3, 'B', random.randint(5, 10))
                time.sleep(2.5)
                current_time = get_current_time()
                for token, order_info in account_info()["orders"].items():
                    if current_time - order_info["timestamp"] > 8:
                        CDA_order_cancel(token)
                
                current_stock_price = get_transaction_history()[0]["price"]
                previous_stock_price = get_transaction_history()[1]["price"]
                if current_stock_price > 1.23 * previous_stock_price:
                    CDA_order(8, 10, 'S', 15)
        except IndexError:
            pass
# End of Generated Code
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)

import time
import random

def active_strategy():
    while True:
        try:
            current_balance = account_info()["balance"]
            if current_balance > 100:
                order_token = CDA_order(3, 3, 'B', random.randint(5, 10))
                time.sleep(2.5)
                current_time = get_current_time()
                for token, order_info in account_info()["orders"].items():
                    order_timestamp = order_info["timestamp"]
                    if current_time - order_timestamp > 8:
                        CDA_order_cancel(token)

                current_stock_price = get_transaction_history()[0]["price"]
                past_stock_price = get_transaction_history()[1]["price"]
                if current_stock_price > 1.23 * past_stock_price:
                    CDA_order(8, 10, 'S', 15)
        except IndexError:
            pass