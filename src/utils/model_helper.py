# utils/model_helper.py

import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
from utils.logger import get_logger

logger = get_logger("ModelHelper")

def load_data(file_path):
    """
    Loads a dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}.")
        return df
    except Exception as e:
        logger.error(f"Failed to load data from {file_path}: {e}")
        return None

def preprocess_data(df, target_column):
    """
    Prepares data for training by splitting into features and labels,
    and performing a train-test split.

    Args:
        df (pd.DataFrame): DataFrame containing the dataset.
        target_column (str): Name of the target column.

    Returns:
        tuple: X_train, X_test, y_train, y_test datasets.
    """
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info("Data has been preprocessed and split into training and testing sets.")
    return X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluates a trained model on the test set and logs the results.

    Args:
        model (object): Trained machine learning model.
        X_test (pd.DataFrame): Test feature set.
        y_test (pd.Series): Test labels.

    Returns:
        None
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    logger.info(f"Model Accuracy: {accuracy}")
    logger.info(f"Classification Report:\n{report}")
    logger.info(f"Confusion Matrix:\n{matrix}")

def save_model(model, file_path):
    """
    Saves a trained model to a file using joblib.

    Args:
        model (object): Trained machine learning model.
        file_path (str): Path to save the model file.

    Returns:
        None
    """
    try:
        joblib.dump(model, file_path)
        logger.info(f"Model saved successfully at {file_path}.")
    except Exception as e:
        logger.error(f"Failed to save model at {file_path}: {e}")

def load_model(file_path):
    """
    Loads a trained model from a file using joblib.

    Args:
        file_path (str): Path to the model file.

    Returns:
        object: Loaded machine learning model.
    """
    try:
        model = joblib.load(file_path)
        logger.info(f"Model loaded successfully from {file_path}.")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from {file_path}: {e}")
        return None
