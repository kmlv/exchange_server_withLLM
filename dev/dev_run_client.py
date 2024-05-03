"""Create client to test with the market without sending prompts"""
from market_client.client import Client

async def run_dev_client():
    client = Client()
    await client.runner()

