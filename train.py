import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier


# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("data/churn.csv")

print("Dataset Loaded Successfully!")


# ============================================
# DATA CLEANING
# ============================================

# Remove customerID
df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove missing values
df.dropna(inplace=True)

# Convert target variable
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ============================================
# FEATURE ENGINEERING
# ============================================

# Average charge per month
df["AvgChargesPerMonth"] = (
    df["TotalCharges"] / (df["tenure"] + 1)
)

# Long-term customer flag
df["IsLongTerm"] = (
    df["tenure"] > 24
).astype(int)


# ============================================
# FEATURES & TARGET
# ============================================

X = df.drop("Churn", axis=1)
y = df["Churn"]


# ============================================
# HANDLE CLASS IMBALANCE
# ============================================

negative = y.value_counts()[0]
positive = y.value_counts()[1]

scale_pos_weight = negative / positive

print(f"\nScale Pos Weight: {scale_pos_weight:.2f}")


# ============================================
# COLUMN TYPES
# ============================================

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

print("\nCategorical Features:")
print(categorical_features)

print("\nNumerical Features:")
print(numerical_features)


# ============================================
# NUMERICAL PIPELINE
# ============================================

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# ============================================
# CATEGORICAL PIPELINE
# ============================================

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])


# ============================================
# COLUMN TRANSFORMER
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)


# ============================================
# XGBOOST MODEL
# ============================================

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.03,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric="logloss"
)


# ============================================
# FULL PIPELINE
# ============================================

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", model)
])


# ============================================
# TRAIN TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================================
# TRAIN MODEL
# ============================================

print("\nTraining Model...")

pipeline.fit(X_train, y_train)

print("Training Completed!")


# ============================================
# PREDICTION PROBABILITIES
# ============================================

y_prob = pipeline.predict_proba(X_test)[:, 1]


# ============================================
# THRESHOLD TUNING
# ============================================

threshold = 0.47

y_pred = (y_prob >= threshold).astype(int)

print(f"\nUsing Threshold: {threshold}")


# ============================================
# EVALUATION
# ============================================

accuracy = accuracy_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

roc_auc = roc_auc_score(y_test, y_prob)

print(f"\nAccuracy: {accuracy:.4f}")

print(f"F1 Score: {f1:.4f}")

print(f"ROC-AUC Score: {roc_auc:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================
# CROSS VALIDATION
# ============================================

cv_scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=5,
    scoring="f1"
)

print("\nCross Validation F1 Scores:")
print(cv_scores)

print(f"\nMean CV F1 Score: {cv_scores.mean():.4f}")


# ============================================
# SAVE PIPELINE
# ============================================

joblib.dump(
    pipeline,
    "models/churn_pipeline.pkl"
)

print("\nPipeline Saved Successfully!")