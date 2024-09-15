# utils/logger.py

import logging

def setup_logging():
    """
    Sets up logging configuration.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

def get_logger(name):
    """
    Returns a logger instance.
    """
    return logging.getLogger(name)
