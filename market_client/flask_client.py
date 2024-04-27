from flask import Flask, request, make_response, jsonify
from market_client.client import Client
import threading
import asyncio
app = Flask(__name__)

client = None

def run_flask():
    app.run(host="0.0.0.0", port=5001)

async def start(input_client: Client):
    global client
    if not input_client or not isinstance(input_client, Client):
        raise Exception(f"Cannot Start Non-Client object {input_client}")
    client = input_client
    print(client)
    t = threading.Thread(target=run_flask)
    t.start()
   # await asyncio.gather(client.recver())
    
def sync_to_async(sync_fn):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(client.send(sync_fn))
    else:
        loop.run_until_complete(client.send(sync_fn))

@app.route('/')
def home():
    return client.__str__()

@app.route('/place_order', methods=["POST"])
def place_order():
   
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
    return "Not Implemented"