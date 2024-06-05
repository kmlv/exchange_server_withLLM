# /LlamaIndex

- `llama_rag.py` currently asks for prompts and generates code based on them.
- `/system_data` stores descriptions of functions.
- `/helper_functions` stores executable helper functions.
- `active_strategy.py` location where the **generated strategy** is written and executed.


## Adding functionality
To improve ChatGPT's ability to understand context or increase the generated strategy's capabilities
you must make adjustments to a couple of files.

### Adding Helper Functions
Update or add any functions in `/helper_functions` to allow the generated strategy to use them without getting
compilation errors since the files within this folder are imported to `active_strategy.py` by default.

### Adding Context
There a couple of reasons for adding context:
- You need to describe how a Helper function works and is used
- You need to describe certain rules that must be followed
Adding context is done within `/system_data` where you write descriptions for the aformentioned aspects.

## Example: adding a function
To allow the generated strategy use a function **add(a,b)** that returns the sum of two numbers
- write the code in `/helper_functions`
```python
def add(a,b):
    return a + b
```
- add a description in `/system_data`
```
The python function add takes two integers and returns the sum
```
It is recommended to experiment with the description to achieve the desired use of **add(a,b)**.



## Testing LlamaIndex and ChatGPT in an isolated environment
Running the module located at `Llama_index\llama_rag.py` will allow you to experiment directly with the code-generation implementation.  
Addtionally within `llama_rag.py` you can change the GPT-model to your liking. 
After moving into the `Llama_index` directory you can run:
```bash
python llama_rag.py
```
You will be prompted to enter a prompt and then observe the generated code at:
`Llama_index\active_strategy.py`