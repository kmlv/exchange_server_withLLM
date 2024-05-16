import logging as log
import json

PLACE_LIMIT_ORDER_ACTION = "place_limit_order"
CANCEL_LIMIT_ORDER_ACTION = "cancel_limit_order"

class BookLogger():
    def __init__(self, log_filepath, logger_name):

        book_log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"book\": %(message)s}')
        #create logger
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)
        # set formatter
        self.log_formatter = book_log_formatter
        # create console handler and set level to debug
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        # add formatter to fh
        self.logger_fh.setFormatter(self.log_formatter)
        # add ch to logger
        self.logger.addHandler(self.logger_fh)
    
    # The server + clients should call this whenever the order book gets updated
    def update_log(self, book, timestamp):
        self.logger.info(book.as_json(), extra={"timestamp" : timestamp})        


class TransactionLogger():
    def __init__(self, log_filepath, logger_name):
        #create logger
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)
        # create & set formatter (empty format)
        self.log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"transaction\": %(message)s}')
        # create console handler and set level to debug
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        # add formatter to fh
        self.logger_fh.setFormatter(self.log_formatter)
        # add ch to logger
        self.logger.addHandler(self.logger_fh)
    
    # The server + clients should call this whenever a transaction takes place in the market
    def update_log(self, transaction, timestamp):
        transaction_data = {}
        transaction_data["token"] = transaction['order_token'].decode()
        transaction_data["shares"] = transaction['executed_shares']
        transaction_data["price"] = transaction['execution_price']
        transaction_json = json.dumps({"transaction": transaction_data})
        self.logger.info(transaction_json, extra={"timestamp" : timestamp})


class ClientStateLogger():
    def __init__(self, log_filepath, logger_name):
        book_log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"state\": %(message)s}')
        #create logger
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)
        # set formatter
        self.log_formatter = book_log_formatter
        # create console handler and set level to debug
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        # add formatter to fh
        self.logger_fh.setFormatter(self.log_formatter)
        # add ch to logger
        self.logger.addHandler(self.logger_fh)
    
    # The clients should call this whenever their account/states gets updated
    def update_log(self, client_info, timestamp):
        client_info_json = json.dumps(client_info)
        self.logger.info(client_info_json, extra={"timestamp" : timestamp})

class ClientActionLogger():
    def __init__(self, log_filepath, logger_name):
        book_log_formatter = log.Formatter('{\"timestamp\": %(timestamp)s, \"action\": %(message)s}')
        #create logger
        self.logger = log.getLogger(logger_name)
        self.logger.setLevel(log.INFO)
        # set formatter
        self.log_formatter = book_log_formatter
        # create console handler and set level to debug
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        # add formatter to fh
        self.logger_fh.setFormatter(self.log_formatter)
        # add ch to logger
        self.logger.addHandler(self.logger_fh)
    
    # The server should call this whenever they receive a request from a client to do a market action (i.e, place_order, cancel_order)
    def update_log(self, action_type, client_action_msg, timestamp):
        action_data = {}
        
        if action_type == PLACE_LIMIT_ORDER_ACTION:
            token_id = client_action_msg['order_token'].decode("utf-8")
            direction = client_action_msg['buy_sell_indicator'].decode("utf-8")
            order_price = client_action_msg['price']
            order_shares = client_action_msg['shares']
            action_data = {"token" : token_id, "direction" : direction, "price" : order_price, "shares" : order_shares}
        elif action_type == CANCEL_LIMIT_ORDER_ACTION:
            print("CLIENT ACTION MSG: ", client_action_msg)
            token_id = client_action_msg['order_token'].decode("utf-8")
            canceled_shares = client_action_msg['shares']
            action_data = {"token" : token_id, "shares" : canceled_shares}
        
        action_json = json.dumps({"action_type" : action_type, "action_data" : action_data})
        self.logger.info(action_json, extra={"timestamp" : timestamp})