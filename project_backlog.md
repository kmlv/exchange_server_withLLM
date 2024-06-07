# Project Backlog (In no particular order)

## Multi-item Exchange
- Currently, the exchange separates orders by ID, not by stock.
- Likely need to refactor `OrderStore` class and `CDA_book.py`.

## Multiple Scripts Support
- Update logic in `Llama_rag.py` to handle multiple strategies running concurrently.
- Save the history of strategies and generated code.
- Retrieve any past strategies.

## Reducing Docker Containers
- Currently, each client gets their own React app and Flask app container. This adds unnecessary overhead for a single client.
- Adjust the Docker files to make a single container for each client rather than two. This would reduce the overhead required per client, allowing support for more clients.

## Using Databases to Log Data
- Creates a central point of data for all clients.
- Allows for client accounts that can persist even when the system is down.
- Can connect the database to `flask_client.py`.

## Connect Remotely Instead of on a Single Device
- `clients.py` must be given the address of the exchange server.
- Currently, on a local device:
  - `client_0`: http://localhost:5070
  - `client_1`: http://localhost:5071
- If the React apps are running on a different address, for example:
  - `client_1`: http://182.53.64.7
- Check the `react app.jsx` to ensure the apps fetch from the correct `flask_client.py` address.

# Known Bugs/Issues
- 
