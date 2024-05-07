"""Create client to test with the market without sending prompts"""
from market_client.client import Client

async def run_dev_client(host, port):
    client = Client(host=host, port=port)
    await client.runner()

