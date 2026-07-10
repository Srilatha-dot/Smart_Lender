from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the saved model and scaler
MODEL_PATH = 'models/loan_model.joblib'
SCALER_PATH = 'models/scaler.joblib'

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    print("ERROR: Model or Scaler not found! Please run train.py first.")
    exit(1)

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Build features list in the exact order the model expects:
        # no_of_dependents, education, self_employed, income_annum, loan_amount,
        # loan_term, cibil_score, residential_assets_value, commercial_assets_value,
        # luxury_assets_value, bank_asset_value
        features_raw = np.array([[
            int(data['dependents']),
            int(data['education']),
            int(data['self_employed']),
            float(data['income']),
            float(data['loan_amount']),
            int(data['loan_term']),
            int(data['cibil_score']),
            float(data['residential_assets']),
            float(data['commercial_assets']),
            float(data['luxury_assets']),
            float(data['bank_assets'])
        ]])
        
        # Scale the features using the saved StandardScaler
        features_scaled = scaler.transform(features_raw)
        
        # Predict target (0 = Approved, 1 = Rejected)
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Invert label mapping to return approved state
        approved = int(prediction) == 0
        
        return jsonify({
            'approved': approved,
            'approval_probability': float(prediction_proba[0]) * 100,
            'rejection_probability': float(prediction_proba[1]) * 100
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
