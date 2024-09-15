# scripts/data_preparation.py

import pandas as pd
from utils.data_cleaner import clean_urls, clean_dataframe
from utils.logger import get_logger

logger = get_logger("DataPreparation")

def prepare_data(input_file, output_file):
    """
    Prepares data for training by loading raw data, cleaning it, 
    and saving the processed data to a new file.

    Args:
        input_file (str): Path to the raw data file.
        output_file (str): Path to save the cleaned data.
    """
    try:
        # Load raw data
        df = pd.read_csv(input_file)
        logger.info(f"Raw data loaded from {input_file}.")
        
        # Clean the data
        df = clean_dataframe(df, columns=['url'])  # Assuming 'url' is a column in your dataset
        df['url'] = clean_urls(df['url'].tolist())  # Clean URLs

        # Save cleaned data
        df.to_csv(output_file, index=False)
        logger.info(f"Cleaned data saved to {output_file}.")
    
    except Exception as e:
        logger.error(f"Failed to prepare data: {e}")

if __name__ == "__main__":
    # Example usage
    prepare_data('data/raw/raw_data.csv', 'data/processed/cleaned_data.csv')
