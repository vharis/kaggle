# Diabetes Prediction Web App

A machine learning-powered web application for predicting diabetes risk using Streamlit and DuckDB.

## 📋 Features

- **Quick Prediction**: Enter Age, Glucose, and BMI to get instant diabetes risk prediction
- **Advanced Options**: Input additional medical metrics for more detailed analysis
- **Model Explainability**: Shows prediction confidence and model information
- **Data Storage**: All predictions automatically stored in DuckDB
- **Prediction History**: View and analyze all previous predictions
- **Medical Disclaimer**: Clear warnings about AI limitations and recommendations to consult healthcare professionals

## 🏗️ Architecture

- **ML Model**: Gradient Boosting Classifier (75.97% accuracy, AUC: 0.8304)
- **Database**: DuckDB for lightweight, serverless data storage
- **Frontend**: Streamlit web framework
- **Data Features**: 8 medical parameters (Age, Glucose, BMI, Pregnancies, Blood Pressure, Skin Thickness, Insulin, Diabetes Pedigree Function)

## 📦 Prerequisites

- Python 3.7+
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. One-Command Setup

```bash
bash setup.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Train and save the ML model
- Verify the setup

### 2. Manual Setup

```bash
# Create virtual environment
python3 -m venv diabetes_env

# Activate virtual environment
source diabetes_env/bin/activate  # On Windows: diabetes_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model
python3 train_and_save_model.py

# Verify setup
python3 test_setup.py
```

### 3. Run the App

```bash
source diabetes_env/bin/activate
streamlit run app.py
```

The app will open at: **http://localhost:8501**

## 📊 Making a Prediction

### Required Fields
- **Age**: Patient's age (18-120 years)
- **Glucose**: Blood glucose level (0-300 mg/dL)
- **BMI**: Body Mass Index (10-60 kg/m²)

### Optional Advanced Fields
- **Pregnancies**: Number of pregnancies (0-20)
- **Blood Pressure**: Systolic BP in mmHg (0-200)
- **Skin Thickness**: Triceps skin fold in mm (0-100)
- **Insulin**: 2-hour serum insulin in mu U/ml (0-900)
- **Diabetes Pedigree Function**: Family history indicator (0-3.0)

## 📈 Prediction History

The app automatically stores all predictions in `diabetes_predictions.duckdb`. The History tab shows:
- Total predictions made
- Positive/Negative risk distribution
- Detailed prediction table with timestamps
- Analytics charts

## 🧪 Testing the Setup

Run the verification script anytime to ensure everything is working:

```bash
source diabetes_env/bin/activate
python3 test_setup.py
```

This checks:
- ✓ All required files exist
- ✓ All dependencies installed
- ✓ Model loads and makes predictions
- ✓ DuckDB works correctly
- ✓ Streamlit is available

## 🌐 Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Add diabetes prediction app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "Deploy an app"
3. Paste your GitHub repo URL
4. Select `app.py` as the entry point
5. Click "Deploy"

### Step 3: Configuration

Create `.streamlit/config.toml` in your repo:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

## 📁 Project Structure

```
diabetes/
├── app.py                        # Main Streamlit app
├── diabetes_model.py             # Model training & evaluation
├── train_and_save_model.py       # Save trained model
├── test_setup.py                 # Verification script
├── setup.sh                      # Automated setup script
├── diabetes.csv                  # Training dataset (768 records)
├── diabetes_model.pkl            # Trained model
├── scaler.pkl                    # Feature scaler
├── feature_names.pkl             # Feature names list
├── diabetes_predictions.duckdb   # Prediction history (auto-created)
├── requirements.txt              # Python dependencies
└── README_APP.md                 # This file
```

## 📊 Model Information

**Dataset**: Pima Indians Diabetes Database
- 768 patient records
- 34.9% diabetes prevalence

**Model Performance**:
- Accuracy: 75.97%
- Precision: 68.89%
- Recall: 57.41%
- F1 Score: 0.6263
- ROC AUC: 0.8304

**Top Predictive Features**:
1. Glucose (41.4% importance)
2. BMI (19.4%)
3. Age (11.7%)
4. Diabetes Pedigree Function (10.8%)

## ⚠️ Important Medical Disclaimer

**This application is for educational and informational purposes only.** The predictions made by this AI model:

- Are NOT a medical diagnosis
- Should NOT replace professional medical advice
- Require confirmation from healthcare professionals
- Should be used in conjunction with clinical judgment

**If positive diabetes risk is predicted, please:**
1. Consult a qualified healthcare provider
2. Get appropriate laboratory tests
3. Discuss lifestyle modifications
4. Monitor health regularly

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
source diabetes_env/bin/activate
pip install -r requirements.txt
```

### Issue: "Model file not found"
```bash
python3 train_and_save_model.py
```

### Issue: DuckDB database locked
- Close the app and restart: `streamlit run app.py`

### Issue: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

## 📝 Files Generated at Runtime

- `diabetes_predictions.duckdb` - SQLite database with prediction history
- `.streamlit/` - Streamlit configuration (auto-created)

## 🔐 Privacy & Security

- All data is stored locally in DuckDB
- No data is sent to external servers
- Predictions are processed client-side
- For production deployment, implement proper authentication

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web framework |
| duckdb | 0.9.2 | Lightweight database |
| scikit-learn | 1.3.2 | ML model |
| pandas | 2.1.3 | Data processing |
| numpy | 1.26.2 | Numerical computing |
| joblib | 1.3.2 | Model serialization |

## 🤝 Contributing

To improve the model:
1. Update `diabetes.csv` with new data
2. Retrain: `python3 train_and_save_model.py`
3. Test: `python3 test_setup.py`
4. Deploy

## 📜 License

Educational use only

## 📞 Support

For issues or questions, refer to:
- [Streamlit Docs](https://docs.streamlit.io/)
- [DuckDB Docs](https://duckdb.org/docs/)
- [Scikit-Learn Docs](https://scikit-learn.org/)
