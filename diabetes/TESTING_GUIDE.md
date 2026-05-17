# 🧪 Local Testing Guide

## Pre-Test Verification

Before starting the app, verify everything is ready:

```bash
source diabetes_env/bin/activate
python3 test_setup.py
```

Expected output:
```
✅ ALL CHECKS PASSED!
```

---

## Step-by-Step Testing Guide

### Test 1: Start the App

```bash
source diabetes_env/bin/activate
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.xxx.xxx:8501
```

**Action**: Open browser to `http://localhost:8501`

---

### Test 2: UI Verification

When the app opens, verify you see:

**Tab 1: Make Prediction**
- [ ] Title: "🏥 Diabetes Prediction Tool"
- [ ] Three input fields: Age, Glucose, BMI
- [ ] Model Info panel on the right
- [ ] "Advanced Options" expander
- [ ] Blue "🔍 Predict" button

**Tab 2: Prediction History**
- [ ] Empty state: "No predictions yet"

---

### Test 3: Make First Prediction

**Scenario A: Healthy Profile**
1. Set Age: `35`
2. Set Glucose: `100`
3. Set BMI: `22`
4. Click "🔍 Predict"

**Expected Result:**
- Green box with "✅ NEGATIVE"
- Confidence: ~95%
- Health recommendations displayed

**Scenario B: At-Risk Profile**
1. Set Age: `55`
2. Set Glucose: `150`
3. Set BMI: `30`
4. Click "🔍 Predict"

**Expected Result:**
- Red box with "⚠️ POSITIVE"
- Confidence: ~70-80%
- Warning message with medical advice

---

### Test 4: Advanced Options

1. Click "Advanced Options" expander
2. Verify you can see fields for:
   - [ ] Pregnancies (0-20)
   - [ ] Blood Pressure (0-200)
   - [ ] Skin Thickness (0-100)
   - [ ] Insulin (0-900)
   - [ ] Diabetes Pedigree Function (0-3)

3. Try making a prediction with custom values
4. Verify prediction still works

---

### Test 5: Prediction History

After making at least 2 predictions:

1. Click "Prediction History" tab
2. Verify you see:
   - [ ] "Total Predictions: 2"
   - [ ] "Positive (Diabetes Risk): X"
   - [ ] "Negative (No Risk): X"
   - [ ] Percentage display
   - [ ] Table with predictions
   - [ ] Charts showing distribution

---

### Test 6: Data Persistence

1. Make another prediction
2. Close the browser tab
3. Stop the app (Ctrl+C)
4. Restart the app:
   ```bash
   streamlit run app.py
   ```
5. Go to History tab
6. Verify all previous predictions are still there

---

### Test 7: Database File Check

1. Stop the app (Ctrl+C)
2. Check if database was created:
   ```bash
   ls -lh diabetes_predictions.duckdb
   ```
3. Expected: File exists and is ~1-10 KB depending on predictions

---

### Test 8: Edge Cases

**Test Out-of-Range Values:**
- Age: Try 150 (should be limited to 120)
- Glucose: Try 350 (should be limited to 300)
- BMI: Try 70 (should be limited to 60)
- All should show validation feedback

**Test with Extreme Values:**
- Age: 18, Glucose: 50, BMI: 11
- Age: 120, Glucose: 300, BMI: 60
- All should still produce predictions

---

### Test 9: Mobile Responsiveness

Open the app on:
- [ ] Desktop browser (Full width)
- [ ] Tablet (Medium width)
- [ ] Mobile phone (Narrow width)

Verify:
- Layout adapts properly
- Buttons are clickable
- No text overflow
- Tables are readable

---

### Test 10: Performance

Make 10 quick predictions and verify:
- Each prediction takes <1 second
- No slowdown over time
- UI remains responsive
- Database handles multiple entries

---

## Test Data Sets

### Test Case 1: Definitely Negative
```
Age: 25
Glucose: 90
BMI: 20
Result: Should be 90%+ confidence negative
```

### Test Case 2: Definitely Positive
```
Age: 70
Glucose: 180
BMI: 35
Result: Should be 80%+ confidence positive
```

### Test Case 3: Borderline
```
Age: 45
Glucose: 120
BMI: 27
Result: Could go either way
```

### Test Case 4: Minimal Data
```
Age: 18
Glucose: 50
BMI: 11
Result: Must still produce a valid prediction
```

### Test Case 5: Maximum Data
```
Age: 120
Glucose: 300
BMI: 60
Result: Must still produce a valid prediction
```

---

## Common Test Workflows

### Quick Smoke Test (5 minutes)
```bash
1. source diabetes_env/bin/activate
2. streamlit run app.py
3. Make 1 prediction
4. Check History tab
5. Close app
```

### Full Regression Test (15 minutes)
```bash
1. Run test_setup.py
2. Start app
3. Test both scenarios (healthy + at-risk)
4. Use advanced options
5. Verify data persistence
6. Check database file
7. Close app
```

### Production Readiness Test (30 minutes)
```bash
1. Fresh environment: rm -rf diabetes_env
2. bash setup.sh
3. Full test suite from test_setup.py
4. Start app and test all features
5. Verify mobile responsiveness
6. Check performance with 20+ predictions
7. Verify database integrity
8. Verify documentation completeness
```

---

## Troubleshooting During Testing

### Issue: Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Issue: Model loading fails
```bash
python3 train_and_save_model.py
streamlit run app.py
```

### Issue: DuckDB locked
```bash
# Close all instances and restart
pkill -f streamlit
streamlit run app.py
```

### Issue: Database corrupted
```bash
rm diabetes_predictions.duckdb
streamlit run app.py
```

### Issue: Package import error
```bash
source diabetes_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Model files exist and load
- [ ] App starts without errors
- [ ] UI loads correctly
- [ ] Can make predictions
- [ ] Predictions produce results
- [ ] History tab shows data
- [ ] Database file created
- [ ] Data persists after restart
- [ ] Advanced options work
- [ ] Edge cases handled
- [ ] Performance acceptable
- [ ] Mobile responsive
- [ ] Documentation present

---

## Test Results Record

Date: _______________
Tester: _______________

### Overall Status
- [ ] All tests passed ✅
- [ ] Some issues found ⚠️
- [ ] Critical issues ❌

### Issues Found
```
1.
2.
3.
```

### Notes
```




```

### Recommendation
- [ ] Ready for deployment
- [ ] Need fixes before deployment
- [ ] Need significant rework

---

## When Testing is Complete

1. ✅ Verify all tests passed
2. ✅ Check no errors in console
3. ✅ Confirm database saved predictions
4. ✅ Document any issues
5. ✅ Fix issues if any
6. ✅ Re-test fixed issues

**Then you're ready to deploy! 🚀**
