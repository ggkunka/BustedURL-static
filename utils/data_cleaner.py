# utils/data_cleaner.py

import pandas as pd
import re
from utils.logger import get_logger

logger = get_logger("DataCleaner")

def clean_urls(urls):
    """
    Cleans a list of URLs by removing unwanted characters, normalizing formats, 
    and ensuring they are well-formed.

    Args:
        urls (list of str): List of URLs to clean.

    Returns:
        list of str: Cleaned URLs.
    """
    cleaned_urls = []
    for url in urls:
        # Remove leading/trailing whitespace
        url = url.strip()
        
        # Normalize by removing unwanted characters
        url = re.sub(r"[^\w\s:/.-]", "", url)
        
        # Convert to lowercase
        url = url.lower()
        
        if validate_url(url):
            cleaned_urls.append(url)
        else:
            logger.warning(f"Invalid URL removed: {url}")

    logger.info(f"Cleaned {len(cleaned_urls)} URLs from {len(urls)} original URLs.")
    return cleaned_urls

def validate_url(url):
    """
    Validates a URL to ensure it is well-formed.

    Args:
        url (str): URL to validate.

    Returns:
        bool: True if URL is valid, False otherwise.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def clean_dataframe(df, columns):
    """
    Cleans specific columns in a DataFrame by removing duplicates, handling missing values,
    and normalizing data.

    Args:
        df (pd.DataFrame): DataFrame to clean.
        columns (list of str): List of column names to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    original_size = len(df)
    df.drop_duplicates(inplace=True)
    df.dropna(subset=columns, inplace=True)
    
    for column in columns:
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip().str.lower()

    cleaned_size = len(df)
    logger.info(f"Cleaned DataFrame from {original_size} rows to {cleaned_size} rows.")
    return df
