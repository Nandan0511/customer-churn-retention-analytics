# app/home.py

import streamlit as st
import os

from config import *
from utils import (
    load_css,
    premium_alert
    )

from auth import (
    login,
    check_auth,
    logout
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title=APP_TITLE,

    page_icon="📊",

    layout="wide"
)

load_css()
# ==========================================
# AUTHENTICATION
# ==========================================

if not check_auth():

    login()

    st.stop()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    f"""
    <div class="hero-container">
        <h1>🚀 {APP_TITLE}</h1>
        <p class="hero-text">
        Enterprise AI platform for predicting
        customer churn using Machine Learning,
        Explainable AI, and Business Intelligence.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# MAIN GRID
# ==========================================

col1, col2 = st.columns([1.7, 1])

# ==========================================
# LEFT SIDE
# ==========================================

with col1:

    st.markdown(
        """
        <div class="custom-card">

        <h2>🤖 AI-Powered Churn Intelligence</h2>

        <p>
        Advanced churn prediction platform built using:
        </p>

        <ul>
            <li>⚡ XGBoost Machine Learning</li>
            <li>🧠 SHAP Explainability</li>
            <li>📊 Executive AI Analytics</li>
            <li>💡 AI Retention Recommendations</li>
            <li>📈 Batch Customer Prediction</li>
            <li>🚀 Enterprise Dashboarding</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# RIGHT SIDE
# ==========================================

with col2:

    if os.path.exists(LOGO_PATH):

        st.image(
            LOGO_PATH,
            width=260
        )

    else:

        st.warning(
            "Logo file not found."
        )

# ==========================================
# FEATURES SECTION
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("✨ Platform Features")

f1, f2, f3 = st.columns(3)

# ==========================================
# FEATURE 1
# ==========================================

with f1:

    st.markdown(
        """
        <div class="feature-card">

        <h3>📈 Interactive Dashboard</h3>

        <p>
        Explore churn trends,
        customer analytics,
        and business KPIs.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# FEATURE 2
# ==========================================

with f2:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🤖 AI Prediction Engine</h3>

        <p>
        Predict customer churn
        probability in real-time
        using ML models.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# FEATURE 3
# ==========================================

with f3:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🧠 Explainable AI</h3>

        <p>
        Understand predictions
        using SHAP explainability
        and feature importance.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# SECOND ROW FEATURES
# ==========================================

f4, f5, f6 = st.columns(3)

with f4:

    st.markdown(
        """
        <div class="feature-card">

        <h3>📊 Batch Prediction</h3>

        <p>
        Upload customer datasets
        and generate predictions
        in bulk instantly.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with f5:

    st.markdown(
        """
        <div class="feature-card">

        <h3>💡 AI Recommendations</h3>

        <p>
        Generate retention
        strategies and business
        action plans automatically.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with f6:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🚀 Executive Reporting</h3>

        <p>
        AI-generated executive
        insights for strategic
        business decisions.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# PIPELINE SECTION
# ==========================================

st.markdown("---")

st.subheader("🧠 Machine Learning Pipeline")

st.code(
"""
Customer Dataset
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Preprocessing Pipeline
        ↓
XGBoost Model
        ↓
Threshold Optimization
        ↓
Churn Prediction
        ↓
SHAP Explainability
        ↓
AI Business Intelligence
        ↓
Executive Recommendations
"""
)

# ==========================================
# FINAL CTA
# ==========================================

premium_alert(
    "Enterprise AI churn analytics platform is ready for deployment.",
    "success"
)