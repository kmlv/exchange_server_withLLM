import time
from cda_client import Client

def CDA_order(shares: int, price: int, direction: str):
    print("SOS")
    client = Client()
    res = client.bingus(direction)
    print(res)
    print("HELP ME")

def active_strategy():
    while True:
        CDA_order(9, 2, 'S')
        time.sleep(5)
if __name__ == '__main__':
    active_strategy()