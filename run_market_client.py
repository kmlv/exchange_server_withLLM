"""
Continuous Double Auction client that sends buy/sell or cancel orders
"""
from market_client import flask_client
from market_client.client import Client
from dev.dev_run_client import *
import asyncio
import argparse
import sys

async def main():
    # parser = argparse.ArgumentParser()
    # # Use dev mode to run clients without using flask
    # parser.add_argument('--mode', '-m', type=str, default='flask',choices=['dev', 'flask'])
    # args = parser.parse_args()
    if len(sys.argv) > 2:
        print(sys.argv[1], flush=True)
    # if args.mode == "dev":
    #     await run_dev_client()
    # if args.mode == "flask":
    # Create a client with specified parameters
    client = Client(balance=1000, starting_shares=100)
    await flask_client.start(input_client=client, openai_api_key=sys.argv[1])
    

  

if __name__ == '__main__':  
    asyncio.run(main())
        