"""
Continuous Double Auction client that sends buy/sell or cancel orders
"""
from market_client import flask_client
from market_client.client import Client
from dev.dev_run_client import *
import asyncio
import configargparse
import sys
import os
import toml
p = configargparse.ArgParser()
p.add('--addr', default='localhost')
p.add('--local', default=8090)
p.add('--port', default=8090, type=int)
p.add('--host', default='10.10.0.2', help="Address of server")
p.add('--mode', '-m', type=str, default='flask',choices=['dev', 'flask', 'container'])
p.add('--key', type=str, default=os.getenv("OPENAI_API_KEY"), help="OPEN_API_KEY")
options, args = p.parse_known_args()

async def main():
    with open('./market_client/config.toml', 'r') as f:
        config = toml.load(f)
    with open('./market_client/config.toml', 'w') as f:
        config['client']['addr'] = options.addr
        config['client']['local_port'] = options.local
        toml.dump(config, f)

    print("RUNNING CLIENT", options, flush=True)
    if options.mode == "dev":
        await run_dev_client(options.host, options.port)
        return
    if options.mode == "flask":
        #Create a client with specified parameters
        client = Client(balance=1000, starting_shares=100, host=options.host, port=options.port)
        await flask_client.start(input_client=client, openai_api_key=options.key)
    

  

if __name__ == '__main__':  
    asyncio.run(main())
        