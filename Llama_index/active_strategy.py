# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

# Start of Generated Code
import time

def active_strategy():
    while True:
        try:
            CDA_order(3, 5, 'B', 30)
            time.sleep(2.5)
        except IndexError:
            break
# End of Generated Code
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
