# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

def active_strategy():
    CDA_order(1, 1, 'S')
    print(get_account_history())
if __name__ == "__main__":
    active_strategy()
