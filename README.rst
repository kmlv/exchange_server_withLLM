
Getting Started
=================
NOTE: Currently, the project supports python 3.10.9: https://www.python.org/downloads/release/python-3109/


Install dependencies
::

    pip install -r requirements.txt
    


Project Setup
=================

Run the CDA exchange

::

    python ./run_market_client.py


Run the CDA client

::

    python ./run_market_client.py


Run Llama_index(Interpretor)

::
    python ./Llama_index/llama_rag

Development information
=================
Folder: /Llama_index
Contains llama_rag.py which currently, asks for prompts and generates code based on them.
Contains /system_data which is where we store descriptions of functions
Contains /helper_functions which is where the executable helper functions are stored

Folder: /market_client
Contains client.py which is the client class used in flask_client.py
Contains flask_client.py that connects a client to the market and with generated strategies



Acknowledgements
=================
This project is based on the previous work from https://github.com/Leeps-Lab/exchange_server
