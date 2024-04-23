from market_client import flask_client
from market_client.client import Client
import asyncio

async def main():
    # Create a client with specified parameters
    client = Client(balance=1000, starting_shares=100)
    await flask_client.start(input_client=client)

  

if __name__ == '__main__':  
    asyncio.run(main())
        