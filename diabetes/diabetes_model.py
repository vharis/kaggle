import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('diabetes.csv')

print("=" * 60)
print("DIABETES PREDICTION MODEL")
print("=" * 60)

# Data overview
print("\n1. DATA OVERVIEW")
print("-" * 60)
print(f"Dataset shape: {df.shape}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nBasic statistics:\n{df.describe()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nClass distribution:\n{df['Outcome'].value_counts()}")
print(f"Diabetes prevalence: {df['Outcome'].mean()*100:.2f}%")

# Data exploration
print("\n2. DATA ANALYSIS")
print("-" * 60)
print(f"\nZero values by column:")
print((df == 0).sum())

# Handle zero values as missing (excluding Pregnancies which can be 0)
columns_to_check = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in columns_to_check:
    zeros = (df[col] == 0).sum()
    print(f"  {col}: {zeros} zeros ({zeros/len(df)*100:.1f}%)")

# Replace zeros with median for these columns
for col in columns_to_check:
    if col in df.columns:
        median_val = df[df[col] != 0][col].median()
        df[col] = df[col].replace(0, median_val)

print(f"\nAfter handling missing values, zero counts:")
print((df == 0).sum())

# Prepare features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n3. FEATURE SCALING")
print("-" * 60)
print(f"Training set size: {X_train_scaled.shape}")
print(f"Test set size: {X_test_scaled.shape}")

# Train multiple models
print("\n4. MODEL TRAINING & EVALUATION")
print("-" * 60)

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = {}
best_model = None
best_score = 0

for name, model in models.items():
    # Train
    model.fit(X_train_scaled, y_train)

    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    # Evaluate
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)

    results[name] = {
        'model': model,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc
    }

    # Track best model
    if auc > best_score:
        best_score = auc
        best_model = name

    print(f"\n{name}:")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  ROC AUC:   {auc:.4f}")

    # Cross-validation score
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    print(f"  CV AUC:    {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

print("\n" + "=" * 60)
print(f"BEST MODEL: {best_model} (AUC: {best_score:.4f})")
print("=" * 60)

# Detailed report for best model
print(f"\n5. DETAILED ANALYSIS - {best_model}")
print("-" * 60)
best_results = results[best_model]
print(f"\nConfusion Matrix:")
cm = confusion_matrix(y_test, best_results['y_pred'])
print(cm)
print(f"\nClassification Report:")
print(classification_report(y_test, best_results['y_pred'], target_names=['No Diabetes', 'Diabetes']))

# Feature importance for tree-based models
if best_model != 'Logistic Regression':
    print(f"\nTop Features (by importance):")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_results['model'].feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))
else:
    # Coefficients for logistic regression
    print(f"\nFeature Coefficients:")
    coef_df = pd.DataFrame({
        'feature': X.columns,
        'coefficient': best_results['model'].coef_[0]
    }).sort_values('coefficient', ascending=False)
    print(coef_df.to_string(index=False))

# Save visualizations
print("\n6. GENERATING VISUALIZATIONS")
print("-" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Confusion Matrix
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
axes[0, 0].set_title(f'{best_model} - Confusion Matrix')
axes[0, 0].set_ylabel('True Label')
axes[0, 0].set_xlabel('Predicted Label')

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, best_results['y_pred_proba'])
axes[0, 1].plot(fpr, tpr, label=f'AUC = {best_score:.3f}')
axes[0, 1].plot([0, 1], [0, 1], 'k--', label='Random')
axes[0, 1].set_xlabel('False Positive Rate')
axes[0, 1].set_ylabel('True Positive Rate')
axes[0, 1].set_title('ROC Curve')
axes[0, 1].legend()

# Model comparison
model_names = list(results.keys())
model_scores = [results[m]['auc'] for m in model_names]
axes[1, 0].bar(model_names, model_scores, color=['green' if m == best_model else 'skyblue' for m in model_names])
axes[1, 0].set_ylabel('ROC AUC Score')
axes[1, 0].set_title('Model Comparison (AUC)')
axes[1, 0].set_ylim([0.7, 0.95])
for i, v in enumerate(model_scores):
    axes[1, 0].text(i, v + 0.01, f'{v:.3f}', ha='center')

# Outcome distribution
df_original = pd.read_csv('diabetes.csv')
outcome_counts = df_original['Outcome'].value_counts()
axes[1, 1].pie(outcome_counts, labels=['No Diabetes (0)', 'Diabetes (1)'],
               autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Outcome Distribution')

plt.tight_layout()
plt.savefig('diabetes_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: diabetes_analysis.png")

# Summary statistics
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✓ Analyzed {df.shape[0]} patient records")
print(f"✓ Trained 3 classification models")
print(f"✓ Best model: {best_model}")
print(f"✓ Test set AUC: {best_score:.4f}")
print(f"✓ Test set Accuracy: {best_results['accuracy']:.4f}")
print(f"✓ Visualization saved as 'diabetes_analysis.png'")
print("=" * 60)
