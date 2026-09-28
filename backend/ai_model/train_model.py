"""
AI Model Training Script for Expense Prediction
Trained using Scikit-Learn Regression on Historical Financial Data
"""
import os
import sys
from pathlib import Path
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Ensure UTF-8 output encoding on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_SAVE_PATH = Path(__file__).resolve().parent / "model.joblib"

def generate_synthetic_historical_training_data(n_samples=500):
    """
    Generates realistic historical transactions for training:
    Features:
      0: Month index (0 - 36)
      1: Day of week (0 - 6)
      2: Category encoded index (0 - 9)
      3: Baseline category multiplier
    Target:
      Transaction Amount
    """
    np.random.seed(42)
    categories = [
        ('Food & Dining', 350.0, 150.0),
        ('Transportation', 200.0, 80.0),
        ('Housing & Rent', 12000.0, 500.0),
        ('Utilities', 1800.0, 300.0),
        ('Entertainment', 600.0, 250.0),
        ('Healthcare', 800.0, 400.0),
        ('Shopping', 1500.0, 600.0),
        ('Education', 2500.0, 800.0),
        ('Personal Care', 450.0, 150.0),
        ('Other', 500.0, 200.0)
    ]

    X = []
    y = []

    for _ in range(n_samples):
        cat_idx = np.random.randint(0, len(categories))
        cat_name, base_mean, base_std = categories[cat_idx]
        month_idx = np.random.randint(1, 36)
        day_of_week = np.random.randint(0, 7)

        # Spending slightly higher on weekends and gradual inflation trend
        weekend_boost = 1.25 if day_of_week in [5, 6] and cat_name in ['Food & Dining', 'Entertainment', 'Shopping'] else 1.0
        inflation_drift = 1.0 + (month_idx * 0.005)
        
        amount = max(20.0, np.random.normal(base_mean, base_std) * weekend_boost * inflation_drift)
        
        X.append([month_idx, day_of_week, cat_idx, base_mean])
        y.append(round(amount, 2))

    return np.array(X), np.array(y)

def train_and_evaluate():
    print("=" * 60)
    print(" [AI MODEL] TRAINING EXPENSE PREDICTION MODEL")
    print("=" * 60)
    
    print("\n[1/4] Preparing training feature matrix...")
    X, y = generate_synthetic_historical_training_data(1200)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f" -> Training samples: {len(X_train)}")
    print(f" -> Testing samples:  {len(X_test)}")

    print("\n[2/4] Fitting Random Forest Regressor Model...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    rf_model.fit(X_train, y_train)

    print("\n[3/4] Evaluating Model Performance...")
    y_pred = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f" -> Mean Absolute Error (MAE):     ${mae:.2f}")
    print(f" -> Root Mean Squared Error (RMSE): ${rmse:.2f}")
    print(f" -> R-Squared Score (Accuracy):    {r2:.4f} ({r2 * 100:.1f}%)")

    print("\n[4/4] Serializing model to disk...")
    os.makedirs(Path(__file__).resolve().parent, exist_ok=True)
    joblib.dump(rf_model, MODEL_SAVE_PATH)
    print(f" -> Saved trained model to: {MODEL_SAVE_PATH}")
    print("\n[SUCCESS] Training completed! The model is ready for inference.")
    print("=" * 60)

if __name__ == '__main__':
    train_and_evaluate()
