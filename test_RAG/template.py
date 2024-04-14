start_template = ("import time\n\n"
                  "def CDA_order(shares: int, price: int, direction: str):\n"
                  "    print('Placing order: ', direction, shares, '@', price, time.time(), flush=True)\n")

# ---- START Appended code
generate_code = ("def active_strategy():\n"
                  "    while True:\n"
                  "      CDA_order(10, 19, 'B')\n"
                  "      time.sleep(1)\n")
# ---- END GENERATED CODE

excutor = ("if __name__ == '__main__':\n"
           "   active_strategy()")

a = f'{start_template}\n {generate_code}\n {excutor}'

print(a)