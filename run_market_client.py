from market_client import flask_client
from market_client.client import Client
from dev.dev_run_client import *
import sys
import asyncio
import argparse

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', type=str, default='flask',choices=['dev'])
    args = parser.parse_args()
    # Use dev mode to run clients without using flask
    if args.mode == "dev":
        await run_dev_client()
    if args.mode == "flask":
        print("wow")
        # Create a client with specified parameters
        client = Client(balance=1000, starting_shares=100)
        await flask_client.start(input_client=client)
    

  

if __name__ == '__main__':  
    asyncio.run(main())
        