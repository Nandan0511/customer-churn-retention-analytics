# app/pages/3_Model_Insights.py
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

APP_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.append(APP_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_css,
    premium_alert)

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(

    page_title="Model Insights",

    page_icon="📊",

    layout="wide"
)

load_css()

# ==========================================
# TITLE
# ==========================================

st.title("📊 Model Insights")

st.caption(
    "Performance analysis and business interpretation of the churn prediction model."
)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""

<div class="custom-card">

<h2>🧠 AI Model Performance Analytics</h2>

<p>
Analyze model accuracy, feature importance,
business impact, and predictive performance
using enterprise AI analytics.
</p>

</div>

""", unsafe_allow_html=True)

# ==========================================
# METRICS
# ==========================================

# ==========================================
# METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        """
        <div class="metric-card">
            <h3>🎯 Accuracy</h3>
            <h1>72.5%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="metric-card">
            <h3>📈 Recall</h3>
            <h1>80%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="metric-card">
            <h3>⚡ F1 Score</h3>
            <h1>60.7%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        """
        <div class="metric-card">
            <h3>🧠 ROC-AUC</h3>
            <h1>0.836</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================
# FEATURE IMPORTANCE
# ==========================================

st.subheader("🚀 Feature Importance")

importance_df = pd.DataFrame({

    "Feature": [

        "Contract",

        "Tenure",

        "MonthlyCharges",

        "OnlineSecurity",

        "TechSupport"
    ],

    "Importance": [

        0.21,

        0.18,

        0.15,

        0.11,

        0.10
    ]
})

fig = px.bar(

    importance_df,

    x="Importance",

    y="Feature",

    orientation="h",

    title="Top Features Driving Churn",

    color="Importance",

    color_continuous_scale="Blues"
)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="white"
    ),

    title_font_size=24,

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# MODEL INTERPRETATION
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

with col1:

    st.markdown("""

    <div class="custom-card">

    <h3>📊 Business Interpretation</h3>

    <p>

    The model is optimized for high recall,
    helping identify churn-prone customers
    before they leave the business.

    </p>

    <ul>

    <li>Detects high-risk customers early</li>

    <li>Improves retention strategy effectiveness</li>

    <li>Supports proactive customer engagement</li>

    <li>Reduces revenue loss</li>

    </ul>

    </div>

    """, unsafe_allow_html=True)

# ==========================================
# MODEL STRENGTHS
# ==========================================

with col2:

    st.markdown("""

    <div class="custom-card">

    <h3>🤖 Model Strengths</h3>

    <ul>

    <li>XGBoost ensemble learning</li>

    <li>Threshold optimization</li>

    <li>Feature engineering pipeline</li>

    <li>SHAP explainability support</li>

    <li>AI-powered business recommendations</li>

    </ul>

    </div>

    """, unsafe_allow_html=True)

# ==========================================
# MODEL PIPELINE
# ==========================================

st.markdown("---")

# ==========================================
# FINAL NOTE
# ==========================================

premium_alert(
    "Model successfully optimized for enterprise churn analytics and AI-powered retention strategy.",
    "success"
)