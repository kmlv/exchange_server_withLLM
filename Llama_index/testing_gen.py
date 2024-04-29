_DIR = "./Llama_index/dummy_strat.py"
_START = "#<s>"
_STOP = "#</s>"
import_lines = """# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *
"""

execution_lines = """if __name__ == "__main__":
    active_strategy()
"""
import time
from time import perf_counter
import subprocess
import platform
code = """
```python
def active_strategy():
    x = 100
    while x > 0:
        balance = account_info()["balance"]

        #print("Hello world!")

        x -= 1
    print("Active Strategy is Done!")
```
"""

code_2 = """
```python
def active_strategy():
    y = 100
    x = 10000
    while y < x:
        balance = account_info()["balance"]

        #print("Hello world!")

        x -= 1

    
    print("Active Strategy 2 is Done!")
```
"""

strategies = list()

def write_script(code_str):
    with open(_DIR, 'r+') as file:
        # Clean file
        file.truncate()
        # Write necessary imports
        file.write(import_lines)
        # write generated code
        for line in code_str.split('\n'):
            # replace codeblock information with start and stop token
            if "```python" in line:
                line = line.replace(line,  _START)
            if "```" in line:
                line = line.replace(line, _STOP)
            file.write(line + '\n')
        # write code that will execute code
        file.write(execution_lines)


def run_script(code_str):
    # Write script to file
    write_script(code_str)

    # try to run the script that was written
    subprocess.run(['python' if (platform.system() == 'Windows') else 'python3', _DIR], text=True)
if __name__ == "__main__":
    t_start = perf_counter()
    run_script(code)
    run_script(code_2)
    t_stop = perf_counter()
    print(f"elapsed time: {t_stop - t_start}")