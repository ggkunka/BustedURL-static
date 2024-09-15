# scripts/train_model.py

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.model_helper import load_data, preprocess_data, save_model
from utils.logger import get_logger

logger = get_logger("ModelTraining")

def train_model(data_file, target_column, model_save_path):
    """
    Trains a machine learning model using the cleaned data and saves the model to disk.

    Args:
        data_file (str): Path to the cleaned data file.
        target_column (str): The name of the target column in the dataset.
        model_save_path (str): Path to save the trained model.
    """
    try:
        # Load and preprocess data
        df = load_data(data_file)

        # Ensure the correct column names are used
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in the dataset. Available columns: {df.columns}")

        # Extract URLs and labels
        urls = df['url'].values
        labels = df[target_column].values

        # Convert URLs to numeric features using TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(urls)

        # Split the data into training and testing sets
        df_features = pd.DataFrame(X.toarray())
        df_features['label'] = labels  # Correctly use 'label' column here

        # Split data
        X_train, X_test, y_train, y_test = preprocess_data(df_features, 'label')

        # Initialize and train the model
        model = GradientBoostingClassifier()
        model.fit(X_train, y_train)
        logger.info("Model training completed.")

        # Save the trained model
        save_model(model, model_save_path)
    
    except Exception as e:
        logger.error(f"Failed to train model: {e}")

if __name__ == "__main__":
    # Ensure 'label' matches the actual column name
    train_model('data/processed/cleaned_data.csv', 'label', 'models/classification/gradient_boosting_model.pkl')
