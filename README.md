# Getting Started

**NOTE:** Currently, the project supports Python 3.10.9: [Python 3.10.9 Release](https://www.python.org/downloads/release/python-3109/)

## Install Dependencies

```bash
pip install -r requirements.txt
```

# Run Method \# 1: Run with Docker
Running the system with docker-compose will create a couple of clients
and a Continuous Double Auction exchange.
## Install Docker Desktop
https://www.docker.com/get-started/
After installing Docker Dekstop, make sure it is running while performing any docker commands
## Running docker-compose
Make sure you're in the home directory where the docker-compose.yaml file is located.
To start the system enter:
```bash
docker-compose up
```
To stop the system enter:
```bash
docker-compose down
```
# Run Method \# 2: Run locally without Docker
To run the system without docker, you must manually start the Continuous Double Auction
and clients.

## Run the CDA Exchange
```bash
python ./run_market_server.py
```
## Run a CDA Client
Since the CDA Exchange is running locally on localhost:8090, you must specify that the host(CDA Exchange) is localhost
and change the port of the client to one other than 8090. An example would look like of correctly running a client
locally looks like:
```bash
python ./run_market_client.py --port 5001 --host localhost
```
If you want to run multiple CDA clients, run the same command in a different terminal and change the --local argument to a different unused port

# Run Method \# 3: Run locally in development mode
`run_market_client.py` has an argument '--mode' or '-m' that's used to specify the mode to run a client.
Using the term 'dev' will run a client in development mode.
## Run the CDA Exchange
```bash
python ./run_market_server.py
```
## Create a Client to Send Orders from the Terminal (Each Client Requires Own Terminal)
Creating a client this way will allow you to manually place orders **without ChatGPT and Flask**. As mentioned
earlier, the CDA Exchange is running locally on localhost:8090 so we must specify the --host as localhost
```bash
python ./run_market_client.py -m dev --host localhost
```


# Development Information

**Folder: /Llama_index**

- Contains `llama_rag.py` which currently asks for prompts and generates code based on them.
- Contains `/system_data` where we store descriptions of functions.
- Contains `/helper_functions` where the executable helper functions are stored.

**Folder: /market_client**

- Contains `client.py` which is the client class used in `flask_client.py`.
- Contains `flask_client.py` that connects a client to the market and with generated strategies.

# Acknowledgements

This project is based on the previous work from [Leeps-Lab/exchange_server](https://github.com/Leeps-Lab/exchange_server).