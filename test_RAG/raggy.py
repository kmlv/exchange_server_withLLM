# Testing out llama-index Retrieval Augmented Generation (RAG) capabilities
# for a simple game of Rock-Paper-Scissors given various prompts

import os.path
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

prompts = [
"If I were playing against you in a game of Rock Paper Scissors, and it looks like I am going to choose Rock, what option should you choose to win?", 
"I am playing a game of Rock Paper Scissors with you. I chose Paper last round. What do you think I will choose this round?",
"I am playing many games of Rock Paper Scissors with you. We have played 10 games together so far, and in all 10 of them I chose Rock. What option should you choose to be fairly confident of winning this next game?",
"I am playing a game of Rock Paper Scissors with you. I choose Squirtle. Is this a valid game? If it is a valid game, what option do you choose to win?",
"What is the weather in Singapore right now?",
"In Python, write code that runs a game of Rock Paper Scissors",
"In Python, write code that runs multiple games of Rock Paper Scissors between two players using the command line to prompt their choices",
"How do I reliably win at Rock Paper Scissors?",
"Describe to me a specific strategy that a person could use to win reliably at Rock Paper Scissors against an opponent who likes to copy their opponent's previous choice half of the time?"]


# Check if storage already exists
PERSIST_DIR = "test_RAG/storage"
if not os.path.exists(PERSIST_DIR):
    # Load the documents and create the index
    documents = SimpleDirectoryReader("test_RAG/data2").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Query the index
query_engine = index.as_query_engine()

for prompt in prompts:
    response = query_engine.query(prompt)
    print("PROMPT: ", prompt)
    print("RESPONSE: ", response)
