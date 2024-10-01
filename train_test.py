from utils.model_helper import load_data, preprocess_data, evaluate_model, save_model
from sklearn.ensemble import GradientBoostingClassifier

# Load and preprocess data
df = load_data('data/processed/cleaned_urls.csv')
X_train, X_test, y_train, y_test = preprocess_data(df, 'target_column')

# Initialize model
model = GradientBoostingClassifier()

# Train model
print("Training the model...")
model.fit(X_train, y_train)

# Evaluate the model
evaluate_model(model, X_test, y_test)

# Save the model
save_model(model, 'models/classification/trained_model.joblib')
