from gpt_bot.gpt_interpreter import GPTInterpreter
from cda_client import Client
#from flask import Flask, jsonify
import logging


client = Client()
gpt = GPTInterpreter()


def test_gpt():
    msg1 = "I want to buy 10 shares of stock for 2 dollars."
    msg2 = "I want to sell 5 shares of my stock for 1 dollar"
    msg3 = "Buy 2 shares of stock for 6 bucks"
    msg4 = "buy 6 shares of stock for 3 dollars"
    msg5 = "put a sell order of 2 shares of stock for 1 dollar"
    msg6 = "Sell 5 shares for 4 dollars"
    msg7 = "I'm considering selling 50 shares at a price of $30 or higher."
    msg8 = "SELL 6 SHARES OF MY STOCK FOR three bucks"
    msg9 = "Sell 1 stock for $1 each that lasts for 60 seconds"
   
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

        function, resulting_params = gpt.perform_market_action(msg, client)
        if function == ["place_order"]:
            if resulting_params["quantity"] == correct_quantity and resulting_params["price"] == correct_price and resulting_params["direction"] == correct_direction:
                correct += 1
            else:
                incorrect += 1

    # set info logging level
    logging.basicConfig(level=logging.INFO)
    logging.info(f"   \033[92mCorrect: {correct}, \033[91mIncorrect: {incorrect}")
            
    # try:
    #         assert gpt.perform_market_action(msg2, client) == ["place_order"]
    #         results.append("Msg2 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg2 Fail")

    # try:
    #         assert gpt.perform_market_action(msg3, client) == ["place_order"]
    #         results.append(f"Msg3 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg3 Fail")
    # try:
    #         assert gpt.perform_market_action(msg4, client) == ["place_order"]
    #         results.append(f"Msg4 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg4 Fail")
    # try:
    #         assert gpt.perform_market_action(msg5, client) == ["place_order"]
    #         results.append(f"Msg4 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg4 Fail")
    # try:
    #         assert gpt.perform_market_action(msg6, client) == ["place_order"]
    #         results.append(f"Msg5 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg5 Fail")
    # try:
    #         assert gpt.perform_market_action(msg7, client) == ["place_order"]
    #         results.append(f"Msg6 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg6 Fail")
    # try:
    #         assert gpt.perform_market_action(msg8, client) == ["place_order"]
    #         results.append(f"Msg7 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg7 Fail")
    # try:
    #         assert gpt.perform_market_action(msg9, client) == ["place_order"]
    #         results.append(f"Msg8 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg8 Fail")
    # try:
    #         assert gpt.perform_market_action(msg1, client) == ["place_order"]
    #         results.append(f"Msg9 Pass")  # Store the result if assertion passes
    # except AssertionError:
    #         results.append("Msg9 Fail")
    


if __name__ == "__main__":
    test_gpt()