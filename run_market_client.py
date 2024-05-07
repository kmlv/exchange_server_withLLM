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
p = configargparse.ArgParser()
p.add('--port', default=8090)
p.add('--host', default='10.10.0.2', help="Address of server")
p.add('--mode', '-m', type=str, default='flask',choices=['dev', 'flask'])
p.add('--key', type=str, default=os.getenv("OPENAI_API_KEY"), help="OPEN_API_KEY")
options, args = p.parse_known_args()
async def main():
    if options.mode == "dev":
        await run_dev_client(options.host, options.port)
    if options.mode == "flask":
        #Create a client with specified parameters
        client = Client(balance=1000, starting_shares=100, host=options.host, port=options.port)
        await flask_client.start(input_client=client, openai_api_key=options.key)
    

  

if __name__ == '__main__':  
    asyncio.run(main())
        