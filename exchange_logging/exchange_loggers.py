import logging as log
import json

# Names for the ClientActionLogger's "action_type" parameter
PLACE_LIMIT_ORDER_ACTION = "place_limit_order"
CANCEL_LIMIT_ORDER_ACTION = "cancel_limit_order"

class BookLogger():
    """Object used by the Exchange and Client classes that log CDABook objects as JSON dictionaries to a specified logfile.
       Each log entry has a timestamp and a snapshot of the CDABook at that timestamp, and are added to the next new line in the logfile.
       Format of each log entry looks like this:
         {"timestamp" : timestamp, "book" : {"bids" : bids, "asks" : asks}}
    Attributes:
        logger: logger from logging
        log_formatter: log.Formatter object for self.logger
        logger_fh: log.FileHandler object for self.logger
    """

    def __init__(self, log_filepath, logger_name):
        """Initialize BookLogger
        Args:
            log_filepath: file path specifying the file for the BookLogger to write to
            logger_name: name of the logger
        """
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)
        
        self.log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"book\": %(message)s}')

        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        self.logger_fh.setFormatter(self.log_formatter)

        self.logger.addHandler(self.logger_fh)
        self.logger.propagate=False

    def update_log(self, book, timestamp):
        """Enters a new log entry.
           The Exchange server + Clients should call this on their BookLogger whenever the order book gets updated.
        Args:
            book: CDABook object specifying the current CDABook to log
            timestamp: int specifying the timestamp of the log entry
        """
        self.logger.info(book.as_json(), extra={"timestamp" : timestamp})        

class TransactionLogger():
    """Object used by the Exchange and Client classes that log transactions that occur in the exchange as JSON dictionaries to a specified logfile
       Each log entry has a timestamp and the transaction that occurred at that timestamp, and are added to the next new line in the logfile.
       NOTE: transactions will be logged twice - once for each order that is in the transaction.
       Format of each log entry looks like this:
         {"timestamp" : timestamp, "transaction" : {"token" : token, "price" : price, "shares" : shares}}
    Attributes:
        logger: logger from logging
        log_formatter: log.Formatter object for self.logger
        logger_fh: log.FileHandler object for self.logger
    """

    def __init__(self, log_filepath, logger_name):
        """Initialize TransactionLogger
        Args:
            log_filepath: file path specifying the file for the TransactionLogger to write to
            logger_name: name of the logger
        """
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)

        self.log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"transaction\": %(message)s}')

        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        self.logger_fh.setFormatter(self.log_formatter)

        self.logger.addHandler(self.logger_fh)
        self.logger.propagate=False
    
    def update_log(self, transaction, timestamp):
        """Enters a new log entry.
           The Exchange server + Clients should call this whenever a transaction takes place in the market.
        Args:
            transaction: JSON dictionary specifying the transaction to log
            timestamp: int specifying the timestamp of the log entry
        """
        transaction_data = {}
        transaction_data["token"] = transaction['order_token'].decode()
        transaction_data["shares"] = transaction['executed_shares']
        transaction_data["price"] = transaction['execution_price']
        transaction_json = json.dumps(transaction_data)
        self.logger.info(transaction_json, extra={"timestamp" : timestamp})

class ClientStateLogger():
    """Object used by the Client class that logs snapshots of the Client's account information as JSON dictionaries to a specified logfile.
       Each log entry has a timestamp and the snapshot of the Client's account info at that timestamp, and are added to the next new line in the logfile.
       NOTE: Only gets used by Clients, and not the Exchange server
       Format of each log entry looks like this:
         {"timestamp" : timestamp, "state" : {"id" : id, "balance" : balance, "orders" : orders, "owned_shares" : owned_shares}}
    Attributes:
        logger: logger from logging
        log_formatter: log.Formatter object for self.logger
        logger_fh: log.FileHandler object for self.logger
    """

    def __init__(self, log_filepath, logger_name):
        """Initialize ClientStateLogger
        Args:
            log_filepath: file path specifying the file for the ClientStateLogger to write to
            logger_name: name of the logger
        """
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)

        self.log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"state\": %(message)s}')

        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        self.logger_fh.setFormatter(self.log_formatter)

        self.logger.addHandler(self.logger_fh)
        self.logger.propagate=False

    def update_log(self, client_info, timestamp):
        """Enters a new log entry.
           The Clients should call this whenever their account/states gets updated
        Args:
            client_info: dictionary specifying the current client information to log
            timestamp: int specifying the timestamp of the log entry
        """
        client_info_json = json.dumps(client_info)
        self.logger.info(client_info_json, extra={"timestamp" : timestamp})

class ClientActionLogger():
    """Object used by the Exchange class that logs actions taken by Clients as JSON dictionaries to a specified logfile
       Each log entry has a timestamp and a JSON representation of the Client action at that timestamp, and are added to the next new line in the logfile.
       NOTE: Inside of "action", "action_type" should be accessed first in order to determine what action (i.e, place_order, cancel_order) the entry is. 
       "action_data" can then be accessed to retrieve specific data related to the action.
       Format of each log entry looks like this:
         {"timestamp" : timestamp, "action" : {"action_type" : action_type, "action_data" : action_data}}
    Attributes:
        logger: logger from logging
        log_formatter: log.Formatter object for self.logger
        logger_fh: log.FileHandler object for self.logger
    """

    def __init__(self, log_filepath, logger_name):
        """Initialize ClientActionLogger
        Args:
            log_filepath: file path specifying the file for the ClientActionLogger to write to
            logger_name: name of the logger
        """
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)

        self.log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"action\": %(message)s}')
        
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        self.logger_fh.setFormatter(self.log_formatter)

        self.logger.addHandler(self.logger_fh)
        self.logger.propagate=False
    
    def update_log(self, action_type, client_action_msg, timestamp):
        """Enters a new log entry.
           The Exchange server should call this whenever they receive a request from a client to do a market action (i.e, place_order, cancel_order)
        Args:
            action_type: string specifying the type of action that is being logged
            client_action_msg: dictionary specifying the data associated with the action being logged
            timestamp: int specifying the timestamp of the log entry
        """
        action_data = {}
        
        if action_type == PLACE_LIMIT_ORDER_ACTION:
            token_id = client_action_msg['order_token'].decode("utf-8")
            direction = client_action_msg['buy_sell_indicator'].decode("utf-8")
            order_price = client_action_msg['price']
            order_shares = client_action_msg['shares']
            action_data = {"token" : token_id, "direction" : direction, "price" : order_price, "shares" : order_shares}
        elif action_type == CANCEL_LIMIT_ORDER_ACTION:
            token_id = client_action_msg['order_token'].decode("utf-8")
            canceled_shares = client_action_msg['shares']
            action_data = {"token" : token_id, "shares" : canceled_shares}
        
        action_json = json.dumps({"action_type" : action_type, "action_data" : action_data})
        self.logger.info(action_json, extra={"timestamp" : timestamp})
