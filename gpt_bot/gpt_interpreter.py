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
                    },
                    "time_in_force": {
                        "type": "integer",
                        "description": "int that specifies duration(in seconds) that order should last"
                    },
                    
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
    {
        "type": "function",
        "function": {
            "name": "can_afford",
            "description": "determines true or false if the user can afford to make a buy order.\
                returns a boolean that specifies whether the client has the funds to make a buy num_shares at cost_per_share",
            "parameters": {
                "type": "object",
                "properties": {
                    "cost_per_share": {
                        "type": "integer",
                        "description": "an int representing the price per share" 
                    },
                    "num_shares": {
                        "type": "integer",
                        "description": "an int representing the quantity of shares to buy"
                    },
                    
                },
                "required": ["quantity", "price", "direction"]
            }
        }
    },

]

#######################################################################
# ISOLATING THE CONDITION TO BE EVALUTATED

def is_conditional(statement):
    # Construct the prompt
    prompt = f"Determine if the following statement is conditional:\n\n{statement}\n\nIs this statement conditional? (Yes/No)"
    
    # Call OpenAI's API
    client = OpenAI(api_key='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')

    messages = [
        {
            "role": "assistant",
            "content": prompt,
        }
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = messages,
        max_tokens=50,
        stop=["\n"]
    )
    # Parse the response
    if response.choices[0].message.content.strip().lower() == "yes":
        return True
    else:
        print("not conditional")
        return False
    
# ISOLATING THE CONDITION TO BE EVALUTATED
def isolate_condition(statement):
    # Regular expression pattern to match condition
    prompt = f"rewrite the following conditional statment,' \n\n{statement}\n\n ', into '(the condition itself), (and the rest of the statment)' separated by a comma"
    
    # Call OpenAI's API
    client = OpenAI(api_key='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')

    messages = [
        {
            "role": "assistant",
            "content": prompt,
        }
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = messages,
        max_tokens=50,
        stop=["\n"]
    )
    
    # If condition found, return it
    return response.choices[0].message.content

#######################################################################
    

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
        self.interpretor = OpenAI(api_key='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')
    



    def perform_market_action(self, message, client):
        """
        Takes in a message from the user which is interpreted by the 
        LLM in order to call the correct function. 

        args:
            message: The message
            client: Client class
        """
        from cda_client import Client

# TWEAKING CODE GENERATION BASED ON IS_CONDITIONAL
### 
        if is_conditional(message):
            if isolate_condition(message) != None:
                if isolate_condition(message):
                    
                    split_cond = isolate_condition(message).split(',')
                    print(split_cond)
                    messages = [
                        {
                            "role": "user",
                            "content": f"write me code that {split_cond[1]} if {split_cond[0]} returns 'True'"
                        }
                    ]
                    
                else: 
                    messages = [
                        {
                            "role": "user",
                            "content": message,
                        }
                    ]
###
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
            "can_afford": client._can_afford,
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


        


