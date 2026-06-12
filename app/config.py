# app/config.py
import os

# ==========================================
# ROOT DIRECTORY
# ==========================================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# ==========================================
# APP INFO
# ==========================================

APP_TITLE = "Customer Churn Prediction System"

APP_DESCRIPTION = """
Predict customer churn using Machine Learning,
XGBoost, and AI-powered business insights.
"""

# ==========================================
# PATHS
# ==========================================

MODEL_PATH = os.path.join(
    ROOT_DIR,
    "models",
    "churn_pipeline.pkl"
)

DATA_PATH = os.path.join(
    ROOT_DIR,
    "data",
    "churn.csv"
)

LOGO_PATH = os.path.join(
    ROOT_DIR,
    "app",
    "assets",
    "logo.png"
)

CSS_PATH = os.path.join(
    ROOT_DIR,
    "app",
    "assets",
    "styles.css"
)

# ==========================================
# MODEL SETTINGS
# ==========================================

THRESHOLD = 0.47

LOW_RISK = 0.30
MEDIUM_RISK = 0.60

LOW_RISK_LABEL = "Low Risk"
MEDIUM_RISK_LABEL = "Medium Risk"
HIGH_RISK_LABEL = "High Risk"