from openai import OpenAI

#Free method to get historical information from Yahoo! Finance https://pypi.org/project/yfinance/
"""
Questions:
-We're using a single item market, so should we just pick a stock to train on?
-Will we need the market to have rounds? Stocks have open, high, low, and close
""" 

_GPT_MODEL = "gpt-3.5-turbo"

class GPTInterpreter:
    """
    An interpreter that generates executable code given market rules and conditions 
    and general guidelines from a user.
    """
    def __init__(self, market_rules):
        """Creates an Interpreter with basic rules of the market

        Args:
            market_rules: The general guidelines on how orders are made, traded, and canceled
        """
        self.interpretor = OpenAI()

        completion = self.interpretor.chat.completions.create(
            model=_GPT_MODEL,
            message=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": market_rules}
            ]
        )

        print(completion)




