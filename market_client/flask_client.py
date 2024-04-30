from flask import Flask, request, make_response, jsonify
from market_client.client import Client
import threading
import asyncio
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

client = None


async def start(input_client: Client):
    global client
    if not input_client or not isinstance(input_client, Client):
        raise Exception(f"Cannot Start Non-Client object {input_client}")
    client = input_client
    print(client)
    t = threading.Thread(target=app.run)
    t.start()
    await asyncio.gather(client.recver())
    
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
    return {"account" : client.account_info(), "book": client.account_info, "history" : client.account_info}

@app.route('/client_orders', methods=["GET"])
def get_client_orders():
    # return {"balance" : self.balance,"orders" : self.orders, "owned_shares" : self.owned_shares}
    account_data = client.account_info()
    # balance = account_data.get("balance")
    # shares = account_data.get("owned_shares")
    orders = account_data.get("orders")
    
    orders_list = []
    for order_num, order_data in orders.items():
        orders_list.append({"order_num": order_num, "price": order_data[0], "quantity": order_data[1], "direction": order_data[2]})

    return jsonify({"orders": orders_list})

if __name__ == '__main__':
    app.run()
