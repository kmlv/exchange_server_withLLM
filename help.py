import time
from cda_client import Client

def CDA_order(shares: int, price: int, direction: str):
    print("Placing order: ", direction, shares, "@", price, flush=True)
    client = Client()
    res = client.bingus(direction)
    print(res, flush=True)

import time

def active_strategy():
    while True:
        CDA_order(10, 4, 'B')
        time.sleep(3)


if __name__ == '__main__':
    active_strategy()