# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

#<s>
def active_strategy():
    token = CDA_order(9, 50, 'S', 10)
    return token
#</s>
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
