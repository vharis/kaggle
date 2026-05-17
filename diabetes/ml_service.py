"""
Diabetes Prediction ML Service
FastAPI backend exposing /predict endpoint.
Auto-trains a 4-feature model on startup if model.pkl is missing.
Falls back to a rule-based classifier if training fails.
"""

import os
import numpy as np
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

# ── Configuration ────────────────────────────────────────────────────────────
FEATURES = ['Glucose', 'BMI', 'DiabetesPedigreeFunction', 'Age']
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler_api.pkl'


# ── Training ─────────────────────────────────────────────────────────────────
def train_and_save():
    """Train a RandomForest on 4 key features and save to disk."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv('diabetes.csv')

    # Replace physiologically impossible zeros with column median
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
    print(f"  Scaler saved → {SCALER_PATH}")


# ── Rule-based fallback ───────────────────────────────────────────────────────
def rule_based_predict(glucose: float, bmi: float, dpf: float, age: float):
    """Simple heuristic used when model.pkl is unavailable."""
    score = 0
    if glucose > 140:
        score += 2
    elif glucose > 100:
        score += 1
    if bmi > 30:
        score += 2
    elif bmi > 25:
        score += 1
    if age > 45:
        score += 1
    if dpf > 0.5:
        score += 1

    prediction = 1 if score >= 3 else 0
    confidence = min(0.50 + score * 0.07, 0.93)
    return prediction, confidence


# ── Bootstrap: auto-train if needed ──────────────────────────────────────────
USE_MODEL = False
model = None
scaler = None

if not os.path.exists(MODEL_PATH):
    print("model.pkl not found — training now...")
    try:
        train_and_save()
    except Exception as e:
        print(f"  Training failed: {e}  →  will use rule-based fallback")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    USE_MODEL = True
    print("Model loaded successfully.")
except Exception as e:
    print(f"Could not load model ({e}) — rule-based fallback active.")


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Diabetes Prediction API",
    description="POST /predict with age, bmi, glucose, diabetic_pedigree_function",
    version="1.0.0",
)


class PredictRequest(BaseModel):
    age: float = Field(..., ge=1, le=120, description="Patient age in years")
    bmi: float = Field(..., ge=5.0, le=80.0, description="Body Mass Index")
    glucose: float = Field(..., ge=0, le=500, description="Plasma glucose (mg/dL)")
    diabetic_pedigree_function: float = Field(..., ge=0.0, le=5.0, description="DPF score")


class PredictResponse(BaseModel):
    prediction: int = Field(..., description="0 = no diabetes risk, 1 = diabetes risk")
    confidence: float = Field(..., description="Model probability for predicted class")
    model_used: str = Field(..., description="'ml_model' or 'rule_based'")


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "model_active": USE_MODEL}


@app.post("/predict", response_model=PredictResponse, tags=["prediction"])
def predict(data: PredictRequest):
    if USE_MODEL:
        import pandas as pd
        X = pd.DataFrame(
            [[data.glucose, data.bmi, data.diabetic_pedigree_function, data.age]],
            columns=FEATURES,
        )
        X_scaled = scaler.transform(X)
        pred = int(model.predict(X_scaled)[0])
        prob = float(model.predict_proba(X_scaled)[0][pred])
        source = "ml_model"
    else:
        pred, prob = rule_based_predict(
            data.glucose, data.bmi, data.diabetic_pedigree_function, data.age
        )
        source = "rule_based"

    return PredictResponse(prediction=pred, confidence=prob, model_used=source)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
