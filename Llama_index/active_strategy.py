# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

# Imports
from sys import exit

# Start of Generated Code
def active_strategy():
    try:
        current_stock_price = get_transaction_history()[0]["price"]
        past_stock_price = get_transaction_history()[1]["price"]
        oldest_stock_price = get_transaction_history()[-1]["price"]
        
        if current_stock_price > 1.05 * past_stock_price:
            account = account_info()
            balance = account["balance"]
            shares_to_buy = balance // current_stock_price
            if shares_to_buy > 0:
                CDA_order(shares_to_buy, current_stock_price, 'B', 3600)
        
        if current_stock_price < 0.95 * past_stock_price:
            account = account_info()
            owned_shares = account["owned_shares"]
            if owned_shares > 0:
                CDA_order(owned_shares, current_stock_price, 'S', 3600)
    except IndexError:
        pass
# End of Generated Code
if __name__ == "__main__":
    active_strategy()
    print("EXIT active_strategy()")
    exit(0)
