# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

def active_strategy():
    initial_balance = account_info()["balance"]
    while account_info()["balance"] >= initial_balance / 2:
        CDA_order(5, 5, 'B')
if __name__ == "__main__":
    active_strategy()
