# scripts/evaluate_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from utils.model_helper import load_data, load_model, preprocess_data
from utils.logger import get_logger
import joblib  # Import joblib to load the vectorizer

logger = get_logger("ModelEvaluation")

def evaluate_trained_model(data_file, target_column, model_path, vectorizer_path):
    """
    Evaluates a trained model using test data and logs the results.

    Args:
        data_file (str): Path to the cleaned data file.
        target_column (str): The name of the target column in the dataset.
        model_path (str): Path to the saved trained model.
        vectorizer_path (str): Path to the saved fitted vectorizer.
    """
    try:
        # Load and preprocess data
        df = load_data(data_file)

        # Extract URLs and labels
        urls = df['url'].values
        labels = df[target_column].values

        # Load the fitted vectorizer
        vectorizer = joblib.load(vectorizer_path)
        logger.info(f"Vectorizer loaded from {vectorizer_path}.")

        # Transform URLs using the loaded vectorizer
        X = vectorizer.transform(urls)

        # Convert X to a DataFrame
        df_features = pd.DataFrame(X.toarray())
        df_features['label'] = labels

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = preprocess_data(df_features, 'label')

        # Load the trained model
        model = load_model(model_path)
        if model is None:
            raise ValueError("Model loading failed.")

        # Predict using the model
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, labels=['benign', 'malicious'], zero_division=0)
        matrix = confusion_matrix(y_test, y_pred, labels=['benign', 'malicious'])

        logger.info(f"Model Accuracy: {accuracy}")
        logger.info(f"Classification Report:\n{report}")
        logger.info(f"Confusion Matrix:\n{matrix}")
    
    except Exception as e:
        logger.error(f"Failed to evaluate model: {e}")

if __name__ == "__main__":
    # Example usage
    evaluate_trained_model('data/processed/cleaned_data.csv', 'label', 'models/classification/gradient_boosting_model.pkl', 'models/classification/tfidf_vectorizer.pkl')
