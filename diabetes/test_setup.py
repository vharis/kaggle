#!/usr/bin/env python3
"""
Test script to verify Diabetes Prediction App setup
"""

import sys
import os

print("=" * 60)
print("DIABETES PREDICTION APP - SETUP VERIFICATION")
print("=" * 60)

# Test 1: Check required files
print("\n1. Checking required files...")
required_files = ['diabetes.csv', 'diabetes_model.pkl', 'scaler.pkl', 'feature_names.pkl', 'app.py']
all_files_exist = True

for file in required_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} (MISSING)")
        all_files_exist = False

if not all_files_exist:
    print("\n⚠️  Some files are missing. Run 'python3 train_and_save_model.py' to generate them.")
    sys.exit(1)

# Test 2: Check imports
print("\n2. Checking Python dependencies...")
dependencies = {
    'streamlit': 'Streamlit',
    'duckdb': 'DuckDB',
    'pandas': 'Pandas',
    'numpy': 'NumPy',
    'sklearn': 'Scikit-Learn',
    'joblib': 'Joblib'
}

all_imports_ok = True
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"   ✓ {name}")
    except ImportError:
        print(f"   ✗ {name} (NOT INSTALLED)")
        all_imports_ok = False

if not all_imports_ok:
    print("\n⚠️  Some packages are missing. Run 'pip install -r requirements.txt'")
    sys.exit(1)

# Test 3: Load and test model
print("\n3. Testing model...")
try:
    import joblib
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    model = joblib.load('diabetes_model.pkl')
    scaler = joblib.load('scaler.pkl')
    feature_names = joblib.load('feature_names.pkl')

    # Test prediction with sample data
    test_data = {
        'Pregnancies': 3.0,
        'Glucose': 120,
        'BloodPressure': 70,
        'SkinThickness': 23,
        'Insulin': 30.5,
        'BMI': 25.0,
        'DiabetesPedigreeFunction': 0.45,
        'Age': 50
    }

    X_test = pd.DataFrame([test_data])
    X_test = X_test[feature_names]
    X_scaled = scaler.transform(X_test)
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0]
    confidence = probability[prediction] * 100

    print(f"   ✓ Model loaded successfully")
    print(f"   ✓ Test prediction: {'Positive (Diabetes Risk)' if prediction == 1 else 'Negative (No Risk)'}")
    print(f"   ✓ Confidence: {confidence:.2f}%")

except Exception as e:
    print(f"   ✗ Error loading/testing model: {e}")
    sys.exit(1)

# Test 4: Test DuckDB
print("\n4. Testing DuckDB...")
try:
    import duckdb

    # Create test database
    con = duckdb.connect(':memory:')
    con.execute("""
        CREATE TABLE test (
            id INTEGER,
            value VARCHAR
        )
    """)
    con.execute("INSERT INTO test VALUES (1, 'test')")
    result = con.execute("SELECT * FROM test").df()

    print(f"   ✓ DuckDB working correctly")
    print(f"   ✓ Test table created and queried")

except Exception as e:
    print(f"   ✗ DuckDB error: {e}")
    sys.exit(1)

# Test 5: Check Streamlit
print("\n5. Checking Streamlit...")
try:
    import streamlit
    version = streamlit.__version__
    print(f"   ✓ Streamlit version: {version}")
except Exception as e:
    print(f"   ✗ Streamlit error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL CHECKS PASSED!")
print("=" * 60)
print("\nTo run the app:")
print("  streamlit run app.py")
print("\nThe app will be available at: http://localhost:8501")
print("=" * 60)
