# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

# Start of Generated Code
import time

def active_strategy():
    while account_info()["balance"] >= 100:
        CDA_order(1, get_transaction_history()[0]["price"], 'B', 94)
        time.sleep(1)
# End of Generated Code
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
