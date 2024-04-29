# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

#<s>
def active_strategy():
    y = 100
    x = 10000
    while y < x:
        balance = account_info()["balance"]

        #print("Hello world!")

        x -= 1

    
    print("Active Strategy 2 is Done!")
#</s>

if __name__ == "__main__":
    active_strategy()
