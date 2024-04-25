from helper_functions.market_commands import *
from helper_functions.client_commands import *






def active_strategy():
    if today == "Thursday":
        CDA_order(1000, 1, 'B')

if __name__ == '__main__':
    active_strategy()