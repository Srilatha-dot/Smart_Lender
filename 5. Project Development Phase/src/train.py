import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def run_training_pipeline():
    print("Step 1: Loading loan application dataset...")
    df = pd.read_csv('../data/loan_approval_dataset.csv')

    print("Step 2: Cleaning whitespace columns and values...")
    # Strip spaces from columns and text records
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()

    # Drop ID identifier and target
    X = df.drop(columns=['loan_id', 'loan_status'])
    y = df['loan_status']

    # Map target string to binary integer ('Approved' -> 0, 'Rejected' -> 1)
    y = y.map({'Approved': 0, 'Rejected': 1})

    print("Step 3: Categorical Label Encoding...")
    le = LabelEncoder()
    cat_cols = ['education', 'self_employed']
    for col in cat_cols:
        X[col] = le.fit_transform(X[col])

    # Stratified split to keep label proportions identical
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Step 4: Applying Standard Scaling to features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("\nStep 5: Training and comparing classification models...")
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    best_acc = 0.0
    best_model = None
    best_model_name = ""

    for name, clf in models.items():
        # Fit classifier
        clf.fit(X_train_scaled, y_train)
        y_pred = clf.predict(X_test_scaled)
        
        acc = accuracy_score(y_test, y_pred)
        print(f"-> {name} Test Accuracy: {acc * 100:.2f}%")
        
        if acc > best_acc:
            best_acc = acc
            best_model = clf
            best_model_name = name

    print(f"\nWinner Selected: {best_model_name} with {best_acc * 100:.2f}% accuracy.")
    
    # Print metrics report for the winner
    winner_preds = best_model.predict(X_test_scaled)
    print("\nWinner Performance Report:")
    print(classification_report(y_test, winner_preds))

    print("Step 6: Serializing and saving best model & scaler...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, 'models/loan_model.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    print("✓ Output model: models/loan_model.joblib")
    print("✓ Output scaler: models/scaler.joblib")

if __name__ == '__main__':
    run_training_pipeline()
