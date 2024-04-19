from gpt_bot.gpt_interpreter import GPTInterpreter
from cda_client import Client
from flask import Flask, request
import asyncio
import threading

app = Flask(__name__)
client = Client()
gpt = GPTInterpreter(client)

@app.route("/", methods=["POST"])
def handle_input():
    prompt = request.get_json().get('prompt')
    gpt.perform_market_action(prompt)

    print(client)
    
    return "ok\n"

async def main():
    thread = threading.Thread(target=app.run)
    thread.start() 
    await asyncio.gather(client.recver())  

if __name__ == "__main__":
    
    
    asyncio.run(main())
