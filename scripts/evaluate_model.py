# scripts/evaluate_model.py

from utils.model_helper import load_data, load_model, preprocess_data, evaluate_model
from utils.logger import get_logger

logger = get_logger("ModelEvaluation")

def evaluate_trained_model(data_file, target_column, model_path):
    """
    Evaluates a trained model using test data and logs the results.

    Args:
        data_file (str): Path to the cleaned data file.
        target_column (str): The name of the target column in the dataset.
        model_path (str): Path to the saved trained model.
    """
    try:
        # Load and preprocess data
        df = load_data(data_file)
        X_train, X_test, y_train, y_test = preprocess_data(df, target_column)

        # Load the trained model
        model = load_model(model_path)
        if model is None:
            raise ValueError("Model loading failed.")

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    
    except Exception as e:
        logger.error(f"Failed to evaluate model: {e}")

if __name__ == "__main__":
    # Example usage
    evaluate_trained_model('data/processed/cleaned_data.csv', 'label', 'models/classification/gradient_boosting_model.pkl')
