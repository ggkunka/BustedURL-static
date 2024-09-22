# utils/__init__.py

"""
Utility package for BustedURL project.
Includes functions for data cleaning, model handling, and logging.
"""

# Import essential utilities to make them easily accessible when importing the package
from .data_cleaner import clean_urls, validate_url, clean_dataframe
from .model_helper import load_data, preprocess_data, evaluate_model, save_model, load_model
from .logger import setup_logging, get_logger
