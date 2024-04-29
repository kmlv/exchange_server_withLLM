from helper_functions.market_commands import *
from helper_functions.client_commands import *






def active_strategy():
    while account_info()["balance"] >= 950:
        CDA_order(1, 5, 'B')
    print(account_info()["id"])

if __name__ == '__main__':
    active_strategy()