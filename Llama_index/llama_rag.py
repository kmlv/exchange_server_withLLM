"""Simple use of Llama-index that builds a query_engine from cda_rules.txt

Ex: 
Query: "sell 183 shares at 3"
Response: "To sell 193 shares at $2, you would use the provided Python function `CDA_order` 
           with the parameters as follows: shares = 193, price = 2, and direction = 'Sell'."
NOTE: Currently, if the prompt does not contain 'shares', then we may get an Empty Response
Ex2: 
Query: buy 132 at 3
Query: Empty Response
"""
from llama_index.llms.openai import OpenAI
from llama_index.core import (Settings, VectorStoreIndex,
                              SimpleDirectoryReader, PromptTemplate,
                              get_response_synthesizer, query_engine)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
import subprocess

import sys

import platform
# Step 1: Defining settings

_GPT_MODEL = "gpt-3.5-turbo"
_DATA_FOLDER = "./Llama_index/system_data"


# Define settings of LLM
Settings.llm = OpenAI(model=_GPT_MODEL)


# Step 2: load data
"""Reader/loader that locates and loads data from supported file types
There are other loaders such as Discord, Notion, Spotify, etc. that must be downloaded to be used
"""
documents = SimpleDirectoryReader(_DATA_FOLDER).load_data()

# Step 3: build index
"""Two basic index types
VectorStoreIndex:
    splits documents into Nodes, then creates vector embeddings of the text of every node that can be queried by an LLM
    Vector Embedding: numerical representation of the semantics/meaning of text
    Many types of embeddings:
        Defualt is text-embedding-ada-002 used by OpenAI
        Different LLMs may require different embeddings
    Searching embeddings(top-k semantic retrieval):
        query is turned into vector embending and is mathematically compared to all embeddings in VectorStoreIndex based on sementic similarity
        VectorStoreIndex returns the most-similar embeddings, the number of emebddings is called 'k'

SummaryIndex(super duper simple):
    stores all of the documents and returns all of them to query engine
"""
index = VectorStoreIndex.from_documents(documents)

# Step 4: store index(currently skipped)

# Step 5: Query
"""Querying
Retrieval: find and return most relevant documents for query from index using a retrieval strategy
Response synthesis: initial query, most-relevant data, and prompt are combined and sent to LLM and returned as a response
Postprocessing: Filter, transform, rerank, retrieved nodes by requireing that they have specific metadata such as keywords attached
"""
# Retriever configuration: https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/
retriever = VectorIndexRetriever(
    index = index,
    similarity_top_k=5
)

# Response synthesizer
response_synthesizer = get_response_synthesizer()

# build query engine
query_engine = query_engine.RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    # Using SimilarityPostprocessor there are other processors that can be used: https://docs.llamaindex.ai/en/stable/understanding/querying/querying/
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],

    
)



def script_runner(code_str):
    print("Running Script..", code_str)
    code_str = code_str.split('\n')
    if 'python' in code_str[0]:
        code_str[0] = ''
        code_str[-1] = ''
    
    
    # read
    with open("./Llama_index/active_strategy.py", 'r+') as file:
        lines = file.readlines()
        # move file pointer to the beginning of a file
        file.seek(0)
        # truncate the file
        file.truncate()

        # start writing lines
        # iterate line and line number
        for number, line in enumerate(lines):
            
            if number <= 7:
                file.write(line)
            else:
                break

    
    with open("./Llama_index/active_strategy.py", "a") as file:

        for line in code_str:
            file.write(line + '\n')
        # Add execution code
        idk = ["\nif __name__ == '__main__':\n",
               "    active_strategy()"
               ]
        file.writelines(idk)
        
    


prompt = ""


# if(len(sys.argv) > 1):
#     # ran the test script
#     prompt = sys.argv[1]
# else:
#     # normal input
#     prompt = input("Enter prompt: ")

def gen_script(prompt):
    # Ask ChatGPT to generate Code
    # Llama-index promptTemplates 
    response = query_engine.query("Write a Python function called active_strategy() that will code the following: " + prompt + ". DO NOT INCLUDE A DESCRIPTION OF THE CODE OR ANYTHING THAT IS NOT THE CODE ITSELF!")
    script_runner(str(response))

    a = subprocess.run(['python' if (platform.system() == 'Windows') else 'python3', './Llama_index/active_strategy.py'], text=True)