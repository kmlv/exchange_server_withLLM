# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

#<s>
import random
import time

def active_strategy():
    orders_placed = 0
    while account_info()["balance"] >= 800 and orders_placed < 50:
        CDA_order(3, 3, 'B', 10)
        orders_placed += 1
        time.sleep(0.1)
    
    while account_info()["balance"] > 100:
        duration = random.randint(5, 10)
        token = CDA_order(3, 3, 'B', duration)
        time.sleep(duration)
        if duration > 8:
            CDA_order_cancel(token)
#</s>
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
