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
    while account_info()["balance"] > 100:
        token = CDA_order(3, 3, 'B', random.randint(5, 10))
        time.sleep(2.5)
        if account_info()["orders"][token]["time_in_force"] > 8:
            CDA_order_cancel(token)
        if get_transaction_history()[0]["price"] > get_transaction_history()[1]["price"] * 1.23:
            CDA_order(8, 10, 'S', 15)
# End of Generated Code
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
