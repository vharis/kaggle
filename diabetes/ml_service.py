"""
Diabetes Prediction ML Module
Provides a simple predict() function — no server required.
Auto-trains a 4-feature model on first import if model.pkl is missing.
Falls back to a rule-based classifier if training fails.
"""

import os
import joblib

FEATURES = ['Glucose', 'BMI', 'DiabetesPedigreeFunction', 'Age']
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler_api.pkl'


def train_and_save():
    """Train a RandomForest on 4 key features and save to disk."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv('diabetes.csv')
    for col in ['Glucose', 'BMI']:
        median = df.loc[df[col] != 0, col].median()
        df[col] = df[col].replace(0, median)

    X = df[FEATURES]
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    acc = model.score(X_test_scaled, y_test)
    print(f"  Accuracy on test set: {acc:.4f}")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"  Model saved → {MODEL_PATH}")


def _rule_based(glucose, bmi, dpf, age):
    score = 0
    if glucose > 140:   score += 2
    elif glucose > 100: score += 1
    if bmi > 30:        score += 2
    elif bmi > 25:      score += 1
    if age > 45:        score += 1
    if dpf > 0.5:       score += 1
    pred = 1 if score >= 3 else 0
    conf = min(0.50 + score * 0.07, 0.93)
    return pred, conf


# ── Bootstrap ─────────────────────────────────────────────────────────────────
_model = None
_scaler = None
_use_model = False

if not os.path.exists(MODEL_PATH):
    print("model.pkl not found — training now...")
    try:
        train_and_save()
    except Exception as e:
        print(f"  Training failed: {e}  →  rule-based fallback will be used")

try:
    _model = joblib.load(MODEL_PATH)
    _scaler = joblib.load(SCALER_PATH)
    _use_model = True
except Exception as e:
    print(f"Could not load model ({e}) — rule-based fallback active.")


# ── Public API ────────────────────────────────────────────────────────────────
def predict(age: float, bmi: float, glucose: float, diabetic_pedigree_function: float):
    """
    Returns (prediction: int, confidence: float, model_used: str).
    prediction  — 0 = low risk, 1 = high risk
    confidence  — probability for the predicted class (0–1)
    model_used  — 'ml_model' or 'rule_based'
    """
    if _use_model:
        import pandas as pd
        X = pd.DataFrame(
            [[glucose, bmi, diabetic_pedigree_function, age]],
            columns=FEATURES,
        )
        X_scaled = _scaler.transform(X)
        pred = int(_model.predict(X_scaled)[0])
        conf = float(_model.predict_proba(X_scaled)[0][pred])
        return pred, conf, "ml_model"
    else:
        pred, conf = _rule_based(glucose, bmi, diabetic_pedigree_function, age)
        return pred, conf, "rule_based"
