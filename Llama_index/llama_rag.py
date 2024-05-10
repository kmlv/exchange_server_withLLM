"""Simple use of Llama-index class that builds a query_engine from
a directory of documents describing how our Continuous Double Auction
implementation works in addition to available functions that can be used.

"""
from llama_index.llms.openai import OpenAI
from llama_index.core import (Settings, VectorStoreIndex,
                              SimpleDirectoryReader, PromptTemplate,
                              get_response_synthesizer, query_engine)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
import subprocess
import os
import sys
# from prompt_eng import get_confirmation

import platform

_START = "#<s>"
_STOP = "#</s>"

import_lines = """# Generated code
# Helper functions
from helper_functions.market_commands import *
from helper_functions.client_commands import *

"""

execution_lines = """if __name__ == "__main__":
    active_strategy()
"""

class LlamaRag:
    def __init__(self):
        self._GPT_MODEL = "gpt-3.5-turbo"
        self._dir = "./Llama_index/"
        self._DATA_FOLDER = f"{self._dir}system_data"
        self._API_KEY = os.getenv("OPENAI_API_KEY")
        self._script_path = f"{self._dir}active_strategy.py"
        self.running_script = None

        if not self._API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        OpenAI.api_key = self._API_KEY

        Settings.llm = OpenAI(model=self._GPT_MODEL, api_key=self._API_KEY)
        self.documents = None
        self.index = None
        self.retriever = None
        self.query_engine = None

    def _load_data(self):
        """
        Reader/loader that locates and loads data from supported file types
        There are other loaders such as Discord, Notion, Spotify, etc. that must be downloaded to be used
        """
        self.documents = SimpleDirectoryReader(self._DATA_FOLDER).load_data()

    def _build_index(self):
        """Initialize index"""
        self.index = VectorStoreIndex.from_documents(self.documents)

    def _configure_retriever(self):
        """Initialize retriever"""
        self.retriever = VectorIndexRetriever(index=self.index, similarity_top_k=5)

    def configure_query_engine(self):
        """Compile information using LlamaIndex"""
        self._load_data()
        self._build_index()
        self._configure_retriever()

        response_synthesizer = get_response_synthesizer()
        self.query_engine = query_engine.RetrieverQueryEngine(
            retriever=self.retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]
        )

    def _write_script(self, code_str):
        """Write a code string to the class file descriped by self._script"""
        with open(self._script_path, 'r+') as file:
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

    def _run_script(self, code_str):
        """Run a code string as a subprocess"""

        # Write to a file
        self._write_script(code_str)

        # try to run the script that was written
        self.running_script = subprocess.Popen(['python' if (platform.system() == 'Windows') else 'python3', self._script_path], text=True)

    def get_confirmation(self, code_chunk):
        """User confirmation 
        Addressing: Before active_strategy() calls CDA_client functions to make market orders, 
        it must confirm with the user that it is making the right function call
        """
        if "stop" in code_chunk.lower(): # adjust error handling here for relevancy
            self.stop_script()
            return
        
        response = self.query_engine.query("Please isolate the token's shares and prices in the following code, " +
                                           "Summarize what it does in the market class" + 
                                           "be sure to include any details like time delay:\n\n " 
                                           + code_chunk + 
                                           "\n\n DONT MENTION TOKENS, and be EXTREMELY concise. Summary:")

        user_response = input("Is this what you would like to deploy? (yes/no): \n\n" + '\033[1m' + str(response) + "\033[0m\n\n").lower().strip()

        # Check user response
        if user_response == 'yes':
            print("Ok, Deploying now...")
            return True
        else:
            print("Aborting active strategy deployment.")
            return False
        
    def execute_query(self, prompt):
        """Generate and execute from a prompt\n
        Basic prompt overview
        Handles:
        - function description active_strategy()
        - code stripping 
        - conditional statement handling
        - user account/market inquiries 
        - irrelevant input handling

        """
        if "stop" in prompt.lower():
            self.stop_script()
            return
        response = self.query_engine.query("Write a Python function named active_strategy() that implements the following: \n" + prompt + 
                                " \n\n DO NOT INCLUDE A DESCRIPTION OF THE CODE OR ANYTHING THAT IS NOT THE CODE ITSELF! \n" +
                                " Include any necessary conditional statements ('if', 'elif', 'else') or calculations needed to accomplish the task or answer the question. \n")

        if self.get_confirmation(str(response)):
            self._run_script(str(response))

    def stop_script(self):
        if self.running_script:
            self.running_script.terminate()
            self.running_script.wait()
   
if __name__ == "__main__":
    # Create LlamaRag() instance
    llama_rag = LlamaRag()
    # Configure it(i.e. retrieve data)
    llama_rag.configure_query_engine()
    # Send prompt
    prompt = input("Enter prompt: ")
    llama_rag.execute_query(prompt)