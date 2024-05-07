# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

#<s>
import time

def active_strategy():
    while account_info()["balance"] > 950:
        CDA_order(3, 3, 'B')
        time.sleep(0.25)
    else:
        print("Sorry, I was not able to implement your strategy. Please rephrase your prompt and try again.")
#</s>
if __name__ == "__main__":
    active_strategy()
