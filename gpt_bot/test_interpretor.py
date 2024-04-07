from gpt_interpreter import GPTInterpreter
from cda_client import Client
def main():
    client = Client()
    interpretor = GPTInterpreter()
    interpretor.perform_market_action(input("Enter a command: "), client)

if __name__ == "__main__":
    main()