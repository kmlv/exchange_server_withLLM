from flask import Flask
from cda_client import Client
import threading
import asyncio

app = Flask(__name__)

client = Client()


def sync_to_async(sync_fn):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        print("oh NO!")
        asyncio.run(sync_fn)
    else:
        print("HELP ME!")
        loop.run_until_complete(sync_fn)

@app.route('/')
def home():
    return client.__str__()

@app.route('/buy')
def hello():
    # https://discuss.python.org/t/calling-coroutines-from-sync-code/23027 thanks Sebastian :)
    sync_to_async(client.send(client.place_order(4,5,'B',10)))
    print(client)
    return 'ok'




# Start client
async def main():
    t = threading.Thread(target=app.run)
    t.start()
    await asyncio.gather(client.sender(), client.recver())

if __name__ == '__main__':   
    asyncio.run(main())