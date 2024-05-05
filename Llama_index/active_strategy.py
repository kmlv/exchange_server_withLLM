# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

#<s>
def active_strategy():
    market_history = get_market_history()
    if len(market_history) < 2:
        print("Sorry, I was not able to implement your strategy. please rephrase your prompt and try again.")
        return
    
    current_price = market_history[0]['book']['bids'][0]['price']
    previous_price = market_history[1]['book']['bids'][0]['price']
    
    if current_price > 1.3 * previous_price:
        CDA_order(1, 1, 'B')
#</s>
if __name__ == "__main__":
    active_strategy()
