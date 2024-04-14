from flask import Flask, request
from cda_client import Client
import threading
import asyncio
import time
app = Flask(__name__)

client = Client()


def sync_to_async(sync_fn):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(client.send(sync_fn))
    else:
        loop.run_until_complete(client.send(sync_fn))
    #time.sleep(1)

@app.route('/')
def home():
    return client.__str__()

@app.route('/place_order')
def hello():
   
    # Parse order info
    order_info = request.json
    order_quantity = int(order_info.get("quantity"))
    order_price = int(order_info.get("price"))
    order_direction = order_info.get("direction")
    order_time = int(order_info.get("time"))
    # send order based on request 
    # https://discuss.python.org/t/calling-coroutines-from-sync-code/23027 thanks Sebastian :)
    sync_to_async(client.place_order(order_quantity, order_price, order_direction, order_time))
    print(client)
    return 'ok'

@app.route('/cancel/<token>')
def cancel(token):
    cancel_info = request.json
    sync_to_async(client.cancel_order(token, cancel_info.get("quantity_remaining")))

@app.route('/info')
def info():
    return {"account" : client.account_info(), "book": client.account_info, "history" : client.account_info}


# Start client
async def main():
    t = threading.Thread(target=app.run)
    t.start()
    await asyncio.gather(client.sender(), client.recver())

if __name__ == '__main__':   
    asyncio.run(main())