from gpt_bot.gpt_interpreter import GPTInterpreter
from market_client.client import Client
#from flask import Flask, jsonify
import logging
import time


client = Client()
gpt = GPTInterpreter(client,test = True)


def test_gpt():
    msg1 = "I want to buy 10 shares of stock for 2 dollars."
    msg2 = "I want to sell 5 shares of my stock for 1 dollar"
    msg3 = "Buy 2 shares of stock for 6 bucks"
    msg4 = "buy 6 shares of stock for 3 dollars"
    msg5 = "put a sell order of 2 shares of stock for 1 dollar"
    msg6 = "Sell 5 shares for 4 dollars"
    msg7 = "SELL 50 shares for 30 dollars or higer"
    msg8 = "SELL 6 SHARES OF MY STOCK FOR three bucks"
    msg9 = "Sell 1 stock for $1 each that lasts for 60 seconds"

    condition_msg1 = "Buy 5 shares if I have more than 6 dollars"
    condition_msg2 = "buy 2 shares if I have more than 2 shares"
    
    c_msgs =[condition_msg1, condition_msg2]
   
    msgs = [msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9]
    correct_params = [{"quantity": 10, "price": 2, "direction": "B"},
                        {"quantity": 5, "price": 1, "direction": "S"},
                        {"quantity": 2, "price": 6, "direction": "B"},
                        {"quantity": 6, "price": 3, "direction": "B"},
                        {"quantity": 2, "price": 1, "direction": "S"},
                        {"quantity": 5, "price": 4, "direction": "S"},
                        {"quantity": 50, "price": 30, "direction": "S"},
                        {"quantity": 6, "price": 3, "direction": "S"},
                        {"quantity": 1, "price": 1, "direction": "S", 'time_in_force': 60}]

    # msg1 = "I want to buy 10 shares of stock for 2 dollars if I can afford it."
    # # msg2 = "I want to sell 5 shares of my stock for 1 dollar"
   
    # msgs = [msg1]
    # correct_params = [{"quantity": 10, "price": 2, "direction": "B"},
    # ]
                      
    correct = 0
    incorrect = 0
    for msg, param in zip(msgs, correct_params):
        correct_quantity = param["quantity"]
        correct_price = param["price"]
        correct_direction = param["direction"]

        function, resulting_params = gpt.perform_market_action(msg)
        if function == ["place_order"]:
            if resulting_params["quantity"] == correct_quantity and resulting_params["price"] == correct_price and resulting_params["direction"] == correct_direction:
                correct += 1
            else:
                incorrect += 1
        else:
            incorrect += 1
        print(f"function called: {function} with parameters {resulting_params}")

    
    # set info logging level
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"   \033[92mCorrect: {correct}, \033[91mIncorrect: {incorrect}")
    print(f"   \033[92mCorrect: {correct}, \033[91mIncorrect: {incorrect}")
    for msg in c_msgs:
        function, resulting_params = gpt.perform_market_action(msg)
        
        print(f"\033[97m function called: {function} with parameters {resulting_params}")
    
if __name__ == "__main__":
    start_time = time.time()
    test_gpt()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print("\033[95m Elapsed time:", elapsed_time, "seconds")
