"""
Continuous Double Auction client that sends buy/sell or cancel orders
"""
from market_client.user_interface import flask_client
from market_client.client import Client
from dev.dev_run_client import *
import asyncio
import configargparse
import os
import toml

"""Client commandline arguments
addr: The port of this client
local: The address of this client
port: The port of the CDA exchange
host: The address of the CDA exchange
mode: specify mode to run the system
   flask: Run the client with the flask endpoint
   dev: Run a client in the terminal where you manually send orders(no flask or ChatGPT)
key: ChatGPT API key
"""
p = configargparse.ArgParser()
p.add('--addr', default='localhost', help="Address of client's flask endpoint")
p.add('--local', default=8090, help="Port of client's flask endpoint")
p.add('--port', default=8090, type=int)
p.add('--host', default='10.10.0.2', help="Address of server")
p.add('--mode', '-m', type=str, default='flask',choices=['dev', 'flask'], help="Specify mode to run system")
p.add('--key', type=str, default=os.getenv("OPENAI_API_KEY"), help="OPEN_API_KEY(required to use interpreter)")
options, args = p.parse_known_args()


def define_configs():
    """Define the address and port for the client's flask endpoint.
    This information is needed for the generated script to work
    """
    with open('./market_client/config.toml', 'r') as f:
        config = toml.load(f)
    with open('./market_client/config.toml', 'w') as f:
        config['client']['addr'] = options.addr
        config['client']['flask_port'] = options.local
        toml.dump(config, f)

async def main():
    define_configs()

    if options.mode == "dev":
        await run_dev_client(options.host, options.port)
    if options.mode == "flask":
        client = Client(balance=1000, starting_shares=100, host=options.host, port=options.port)
        await flask_client.start(input_client=client, openai_api_key=options.key)
    

  

if __name__ == '__main__':  
    asyncio.run(main())
        