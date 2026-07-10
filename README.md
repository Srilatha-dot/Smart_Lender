# 💰 Smart Lender - AI Powered Loan Approval Prediction

Smart Lender is a machine learning powered web application that analyzes an applicant's financial and personal details (CIBIL Score, Income, Assets, etc.) to predict whether their loan will be **Approved** or **Rejected**, along with the approval probability.

---

## 🚀 Features

- **Interactive UI** — Clean, modern, responsive FinTech-style interface built with HTML, CSS and JavaScript.
- **ML Model Comparison** — Trains and compares Logistic Regression, Random Forest, and XGBoost, then automatically selects the best-performing model based on test accuracy.
- **Real-time Prediction** — Flask backend returns instant loan status and approval probability using AJAX (Fetch API), with no page reload.
- **Robust Data Pipeline** — Handles data cleaning, categorical label encoding, and standard feature scaling before training.
- **Loading & Result Animations** — Loading spinner while predicting, animated success/rejection result screens with probability bar.

---

## 🛠️ Tech Stack

**Backend:** Python, Flask
**Machine Learning:** Scikit-Learn, XGBoost, Pandas, NumPy, Joblib
**Frontend:** HTML5, CSS3, JavaScript (Vanilla)

---

## 📂 Project Structure

```
Smart_Lender/
│
├── data/
│   └── loan_approval_dataset.csv   # Training dataset
│
├── src/
│   ├── app.py                      # Flask backend & /predict API
│   ├── train.py                    # Model training pipeline (compares 3 models)
│   ├── models/
│   │   ├── loan_model.joblib        # Saved best-performing ML model
│   │   └── scaler.joblib            # Saved StandardScaler used for preprocessing
│   ├── templates/
│   │   └── index.html               # Frontend UI
│   └── static/
│       ├── style.css
│       └── script.js
│
├── requirements.txt                # Python libraries required for this project
├── .gitignore                      # Files/folders excluded from GitHub
├── notebook.ipynb                  # Data analysis & exploration notebook
└── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Srilatha-dot/Smart_Lender.git
   cd Smart_Lender
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Move into the `src` folder** (both `train.py` and `app.py` must be run from here)
   ```bash
   cd src
   ```

5. **Train the model** (generates `models/loan_model.joblib` and `models/scaler.joblib`)
   ```bash
   python train.py
   ```

6. **Run the Flask app**
   ```bash
   python app.py
   ```

7. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🔮 How Prediction Works

The user fills the loan application form → JavaScript sends a JSON payload to the `/predict` API → Flask scales the input using the saved `scaler.joblib` → the trained model predicts approval → the result (with probability %) is sent back and displayed instantly, without reloading the page.

### Input Fields (JSON keys sent to `/predict`)

| Field                | Description                                  |
|-----------------------|-----------------------------------------------|
| `dependents`          | Number of dependents                         |
| `education`           | 0 = Graduate, 1 = Not Graduate               |
| `self_employed`       | 0 = No, 1 = Yes                              |
| `income`               | Annual income                                |
| `loan_amount`          | Requested loan amount                        |
| `loan_term`            | Loan term in months                          |
| `cibil_score`          | CIBIL credit score (300–900)                 |
| `residential_assets`   | Residential asset value                      |
| `commercial_assets`    | Commercial asset value                       |
| `luxury_assets`        | Luxury asset value                           |
| `bank_assets`          | Liquid bank asset value                      |

### Sample API Response

```json
{
  "approved": true,
  "approval_probability": 87.42,
  "rejection_probability": 12.58
}
```

---

## 📊 Model Performance

`train.py` trains three classifiers on the loan approval dataset and automatically picks the one with the highest test accuracy:

| Model                | Role                         |
|-----------------------|-------------------------------|
| Logistic Regression   | Baseline linear model         |
| Random Forest          | Ensemble tree-based model     |
| XGBoost                 | Gradient boosted model        |

> Run `python train.py` (from inside `src/`) to see the printed accuracy of each model and the winning model that gets saved as `models/loan_model.joblib`.

---

## 📌 Notes

- The model is trained on the `loan_approval_dataset.csv` file inside `data/` (one level above `src/`).
- If you retrain the model with new/extra features, remember to update both `train.py` (feature order) and `app.py` (JSON key parsing) so they stay in sync with the frontend form.

---

## 👤 Developer

**Name:** [Ch.Srilatha]
**GitHub:** [@Srilatha-dot](https://github.com/Srilatha-dot)

---

## 📄 License

This project is open-source and free to use for learning purposes.