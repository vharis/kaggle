# 🚀 Quick Start Guide - Diabetes Prediction App

## Setup Instructions (One-Time)

### Option A: Automated Setup (Recommended)

```bash
bash setup.sh
```

That's it! This single command will:
- ✓ Create a Python virtual environment
- ✓ Install all required packages
- ✓ Train and save the ML model
- ✓ Verify everything works

### Option B: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv diabetes_env

# 2. Activate it
source diabetes_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train model
python3 train_and_save_model.py

# 5. Verify setup
python3 test_setup.py
```

## Running the App

Every time you want to use the app:

```bash
# 1. Activate virtual environment
source diabetes_env/bin/activate

# 2. Start the app
streamlit run app.py
```

The app will automatically open at: **http://localhost:8501**

## 📱 Using the App

### Tab 1: Make Prediction
1. Enter **Age**, **Glucose level**, and **BMI**
2. (Optional) Click "Advanced Options" for more medical parameters
3. Click **"🔍 Predict"** button
4. Get instant diabetes risk assessment with confidence level

### Tab 2: Prediction History
- View all previous predictions
- See statistics (total, positive, negative cases)
- Analyze trends and patterns
- Export data if needed

## 🧪 Verify Setup Works

After setup, test everything:

```bash
source diabetes_env/bin/activate
python3 test_setup.py
```

Expected output:
```
✅ ALL CHECKS PASSED!
```

## 📊 App Features

| Feature | Description |
|---------|-------------|
| **Quick Prediction** | Input 3 main metrics for instant assessment |
| **Advanced Mode** | Input all 8 medical parameters for detailed analysis |
| **Real-time Results** | Immediate diabetes risk prediction with confidence |
| **Data Storage** | Automatic DuckDB storage of all predictions |
| **History Tracking** | View and analyze all previous predictions |
| **Model Insights** | See feature importance and model performance |
| **Medical Info** | Detailed disclaimers and health recommendations |

## 🔄 Workflow Example

```
1. Activate env:  source diabetes_env/bin/activate
2. Start app:     streamlit run app.py
3. Open browser:  http://localhost:8501
4. Make prediction:
   - Age: 45
   - Glucose: 130
   - BMI: 28
   - Click Predict
5. Review result and history
6. Close with Ctrl+C when done
```

## 📈 Prediction Output

For each prediction you get:
- **Risk Assessment**: Positive (High Risk) or Negative (No Risk)
- **Confidence**: Probability percentage (0-100%)
- **Recommendations**: What to do next
- **Auto-Stored**: Saved automatically in database

## 💾 Data Storage

All predictions are stored in `diabetes_predictions.duckdb`:
- Automatically created on first prediction
- Contains: Age, Glucose, BMI, other metrics, prediction, confidence, timestamp
- Accessible from the History tab

## ⚙️ System Requirements

- Python 3.7 or higher
- 50 MB disk space
- 200 MB RAM
- Modern web browser

## 🐛 Troubleshooting

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Need to reinstall?**
```bash
rm -rf diabetes_env
bash setup.sh
```

**Model won't train?**
```bash
python3 train_and_save_model.py
```

**Reset everything?**
```bash
rm -rf diabetes_env diabetes_predictions.duckdb .streamlit
bash setup.sh
```

## 🚢 Ready to Deploy?

See **README_APP.md** for:
- Streamlit Cloud deployment
- GitHub integration
- Production configuration
- Security considerations

## ✅ Checklist

- [ ] Run `bash setup.sh` (or manual setup)
- [ ] See "✅ ALL CHECKS PASSED!" from test_setup.py
- [ ] Run `streamlit run app.py`
- [ ] Make a test prediction
- [ ] See prediction in History tab
- [ ] Ready to use!

## 📚 More Information

- Model Details: See `diabetes_model.py`
- Full Documentation: See `README_APP.md`
- Configuration: `.streamlit/config.toml`

---

**Enjoy predicting diabetes risk!** 🏥
