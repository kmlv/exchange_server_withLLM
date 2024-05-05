import logging as log

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
        self.log_formatter = log.Formatter('')
        # create console handler and set level to debug
        self.logger_fh = log.FileHandler(filename=log_filepath, mode='w')
        self.logger_fh.setLevel(log.INFO)
        # add formatter to fh
        self.logger_fh.setFormatter(self.log_formatter)
        # add ch to logger
        self.logger.addHandler(self.logger_fh)
    
    # The server + clients should call this whenever a transaction takes place in the market
    def update_log(self, transaction):
        self.logger.info(transaction)
