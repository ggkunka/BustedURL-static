# utils/model_helper.py

import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
import pandas as pd
from transformers import Trainer, TrainingArguments
from transformers import RobertaForSequenceClassification, BertForSequenceClassification
import torch
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

def evaluate_model(model, X_test, y_test, model_type="sklearn"):
    """
    Evaluates a trained model on the test set and logs the results. Supports sklearn and Hugging Face transformer models.

    Args:
        model (object): Trained machine learning model or Hugging Face transformer.
        X_test (pd.DataFrame): Test feature set.
        y_test (pd.Series): Test labels.
        model_type (str): Type of the model - 'sklearn' for traditional ML models or 'transformer' for Hugging Face models.

    Returns:
        None
    """
    if model_type == "sklearn":
        predictions = model.predict(X_test)
    elif model_type == "transformer":
        inputs = X_test['url'].tolist()
        predictions = model.predict(inputs).logits.argmax(axis=-1)
        predictions = torch.tensor(predictions)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted')
    recall = recall_score(y_test, predictions, average='weighted')
    f1 = f1_score(y_test, predictions, average='weighted')
    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    logger.info(f"Model Accuracy: {accuracy}")
    logger.info(f"Precision: {precision}")
    logger.info(f"Recall: {recall}")
    logger.info(f"F1-score: {f1}")
    logger.info(f"Classification Report:\n{report}")
    logger.info(f"Confusion Matrix:\n{matrix}")

def fine_tune_transformer(model_name, train_dataset, val_dataset):
    """
    Fine-tunes a transformer model using the provided dataset.

    Args:
        model_name (str): Name of the transformer model to fine-tune (e.g., 'roberta-base', 'bert-base-uncased').
        train_dataset (Dataset): Training dataset.
        val_dataset (Dataset): Validation dataset.

    Returns:
        object: Fine-tuned transformer model.
    """
    logger.info(f"Starting fine-tuning for {model_name}...")
    
    if 'bert' in model_name:
        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    else:
        model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=2)

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=50,
        save_steps=100,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()
    logger.info("Fine-tuning complete.")
    
    return model

def save_model(model, file_path, model_type="sklearn"):
    """
    Saves a trained model to a file using joblib or transformers.

    Args:
        model (object): Trained machine learning model or transformer model.
        file_path (str): Path to save the model file.
        model_type (str): Type of the model - 'sklearn' for traditional ML models or 'transformer' for Hugging Face models.

    Returns:
        None
    """
    try:
        if model_type == "sklearn":
            joblib.dump(model, file_path)
        elif model_type == "transformer":
            model.save_pretrained(file_path)

        logger.info(f"Model saved successfully at {file_path}.")
    except Exception as e:
        logger.error(f"Failed to save model at {file_path}: {e}")

def load_model(file_path, model_type="sklearn"):
    """
    Loads a trained model from a file using joblib or transformers.

    Args:
        file_path (str): Path to the model file.
        model_type (str): Type of the model - 'sklearn' for traditional ML models or 'transformer' for Hugging Face models.

    Returns:
        object: Loaded machine learning model or transformer model.
    """
    try:
        if model_type == "sklearn":
            model = joblib.load(file_path)
        elif model_type == "transformer":
            model = RobertaForSequenceClassification.from_pretrained(file_path)  # or BertForSequenceClassification

        logger.info(f"Model loaded successfully from {file_path}.")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from {file_path}: {e}")
        return None
