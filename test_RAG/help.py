import time

def CDA_order(shares: int, price: int, direction: str):
    print("Placing order: ", direction, shares, "@", price, time.time(), flush=True)

# ---- START Appended code
def active_strategy():
    while True:
        CDA_order(10, 19, 'B')
        time.sleep(1)
# ---- END GENERATED CODE

if __name__ == '__main__':
    active_strategy()
