import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

def setup_logger(name, log_file, level=logging.INFO, formatter=None):
    """Function to setup as many loggers as you want"""
    if formatter is None:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # This is to ensure the logger doesn't propagate to any potential root logger
    logger.propagate = False

    return logger

# Setup specific loggers
ssh_logger = setup_logger('ssh_honeypot', 'ssh_honeypot.log')
http_logger = setup_logger('http_honeypot', 'http_honeypot.log', formatter=JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Disable the root logger to prevent any unexpected logging
logging.getLogger().handlers = []
