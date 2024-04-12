from openai import OpenAI
import json

#Free method to get historical information from Yahoo! Finance https://pypi.org/project/yfinance/
"""
Questions:
-We're using a single item market, so should we just pick a stock to train on?
-Will we need the market to have rounds? Stocks have open, high, low, and close
""" 

_GPT_MODEL = "gpt-3.5-turbo"
_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Processes the trader's buy or sell orders in the stock market",
            "parameters": {
                "type": "object",
                "properties": {
                    "quantity": {
                        "type": "integer",
                        "description": "Amount of shares the user wants to buy or sell. This is \
                        specified using a number, along with an optional unit (e.g., shares, stocks)." 
                    },
                    "price": {
                        "type": "integer",
                        "description": "The price the user is willing to buy or sell at. \
                        This can be specified using a number, along with an optional currency \
                        symbol (e.g., $, £, €). Common variations for dollars include 'dollars' \
                        and 'bucks'."
                    },
                    "direction":{
                        "type": "string",
                        "enum": ["B", "S"],
                        "description": "Determines if it is a bull or sell order. \
                                        B represents a buy order, S represents a \
                                        sell order"
                    }
                    
                },
                "required": ["quantity", "price", "direction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancels one the user's existing order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_token": {
                        "type": "integer",
                        "description": "The id representing the order id"
                    },
                    "quantity_remaining": {
                        "type": "integer",
                        "description" : "Amount of shares that are being removed"
                    },
                },
                "required": ["order_token", "quantity_remaining"]
            },
        },
    },

]

class GPTInterpreter:
    """
    An interpreter that generates executable code given market rules and conditions 
    and general guidelines from a user.
    """
    
    def __init__(self, market_rules = "none"):
        """Creates an Interpreter with basic rules of the market

        Args:
            market_rules: The general guidelines on how orders are made, traded, and canceled
        """
        self.interpretor = OpenAI()
    
    def perform_market_action(self, message, client):
        """
        Takes in a message from the user which is interpreted by the 
        LLM in order to call the correct function. 

        args:
            message: The message
            client: Client class
        """
        from cda_client import Client

        input = [{"role": "user", "content": message}]
        response = self.interpretor.chat.completions.create(
            model = _GPT_MODEL,
            messages = input,
            tools = _TOOLS,
        )

        response_message = response.choices[0].message
        # list of the funcitons called
        functions_called = response_message.tool_calls

        available_functions = {
            "place_order": client.place_order,
            "cancel_order": client.cancel_order,
        }
        # testing purposes
        function_list_result = []
        if functions_called:

            for _function in functions_called:
                
                function_name = _function.function.name
                function_list_result.append(function_name)
                function_to_call = available_functions[function_name]
                args = json.loads(_function.function.arguments)
                output = function_to_call(**args)
                #
                print(f"Function Name: {function_name}, Args: {args}")
                print(f"Output: {output}\n")
        #print(functions_called)
        # gprint(function_list_result, args)
        return function_list_result, args


        


