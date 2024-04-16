import subprocess


results_of_test = open("test_RAG/test_result.txt", "w")

def run_test(prompt, testName):
    subprocess.run(["python", "test_RAG/custom_rag.py", prompt])
    
    write_results(prompt,testName)

def write_results(prompt,testName):
    with open("test_RAG/help.py", 'r+') as file1:
        # read all the times
        lines = file1.readlines()
        
        data_to_write = f"Test: {testName}\nPrompt:{prompt}\n"
        for lineNum, line in enumerate(lines):
            
            if lineNum > 7:
                data_to_write += line + "\n"
        results_of_test.write(data_to_write)

standard_buy_message = "Buy 5 shares at 3 dollars"
standard_sell_message = "Sell 10 shares at 2 dollars"
timed_buys = "Every 2 seconds buy 3 shares at 2 dollars until you reach 5 buy orders"
timed_sells = "Every 4 seconds put a sell order for 1 share until you react 3 sell orders"
random_buy = "Buy 5 random buys with the share count being from 1-10 and the price being from 2 dollars to 8 dollars"
random_sell = "Put 3 random sell orders from the share count ranging from 2-4 and price ranging from 1-5"
big_spender = "Buy until you have no more money"
big_seller = "place sell orders until you have more shares"
grammar_problem1 = "Buy 5 share at 2 dollar"
grammar_problem2 = "by 10 shares at two buks"
not_related = "Buy 10 bags of dog food from the pet store"

run_test(standard_buy_message, "standard_buy_message")
run_test(standard_sell_message, "standard_sell_message")
run_test(timed_buys, "timed_buys")
run_test(timed_sells, "timed_sells")
run_test(random_buy, "random_buy")
run_test(random_sell, "random_sell")
run_test(big_spender, "big_spender")
run_test(big_seller, "big_seller")
run_test(grammar_problem1, "grammar_problem1")
run_test(grammar_problem2, "grammar_problem2")
run_test(not_related, "not_related")






results_of_test.close()






