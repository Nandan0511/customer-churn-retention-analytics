# app/pages/4_Batch_Prediction.py
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

APP_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.append(APP_DIR)

import streamlit as st
import pandas as pd

from utils import (
    load_css,
    load_pipeline,
    get_risk_level,
    generate_batch_ai_insights,
    generate_pdf_report,
    premium_alert
)

from config import THRESHOLD

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="Batch Prediction",

    page_icon="📂",

    layout="wide"
)

load_css()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    """
    <div class="hero-container">
        <h1>
        📂 Batch Churn Prediction
        </h1>
        <p class="hero-text">
        Upload customer datasets and generate
        AI-powered churn predictions,
        risk analysis, and executive insights.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# LOAD MODEL
# ==========================================

pipeline = load_pipeline()

# ==========================================
# FILE UPLOADER
# ==========================================

st.markdown(
    """
    <div class="custom-card">

    <h3>📤 Upload Customer Dataset</h3>

    <p>
    Upload a CSV file containing telecom
    customer information for bulk churn prediction.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(

    "Upload CSV File",

    type=["csv"]
)

# ==========================================
# PROCESS FILE
# ==========================================

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        # ==========================================
        # DATA PREVIEW
        # ==========================================

        st.markdown("---")

        st.subheader("📄 Uploaded Dataset")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        # ==========================================
        # FEATURE ENGINEERING
        # ==========================================

        df["TotalCharges"] = pd.to_numeric(

            df["TotalCharges"],

            errors="coerce"
        )

        df["TotalCharges"] = (
            df["TotalCharges"]
            .fillna(0)
        )

        # ==========================================
        # ENGINEERED FEATURES
        # ==========================================

        df["AvgChargesPerMonth"] = (

            df["TotalCharges"]

            /

            (df["tenure"] + 1)
        )

        df["IsLongTerm"] = (

            df["Contract"]

            != "Month-to-month"

        ).astype(int)

        # ==========================================
        # PREDICTION
        # ==========================================

        probabilities = (

            pipeline
            .predict_proba(df)[:, 1]
        )

        predictions = (

            probabilities >= THRESHOLD

        ).astype(int)

        # ==========================================
        # RESULTS
        # ==========================================

        results_df = df.copy()

        results_df["Churn Probability"] = (
            probabilities * 100
        ).round(2)

        results_df["Prediction"] = predictions

        results_df["Risk Level"] = [

            get_risk_level(prob)

            for prob in probabilities
        ]

        results_df["Prediction"] = (

            results_df["Prediction"]

            .map({

                0: "Stay",

                1: "Churn"
            })
        )

        # ==========================================
        # SUMMARY METRICS
        # ==========================================

        st.markdown("---")

        st.subheader("📊 Batch Prediction Summary")

        total_customers = len(results_df)

        churn_customers = len(

            results_df[
                results_df["Prediction"] == "Churn"
            ]
        )

        avg_probability = (

            results_df[
                "Churn Probability"
            ].mean()
        )

        col1, col2, col3 = st.columns(3)

        # ==========================================
        # METRIC 1
        # ==========================================

        with col1:

            st.markdown(
                f"""
<div class="metric-card">
    <h3>👥 Total Customers</h3>
    <h1>{total_customers}</h1>
</div>
""",
                unsafe_allow_html=True
            )

        # ==========================================
        # METRIC 2
        # ==========================================

        with col2:

            st.markdown(
                f"""
<div class="metric-card">
    <h3>⚠️ Predicted Churn</h3>
    <h1>{churn_customers}</h1>
</div>
""",
                unsafe_allow_html=True
            )

        # ==========================================
        # METRIC 3
        # ==========================================

        with col3:

            st.markdown(
                f"""
<div class="metric-card">
    <h3>📉 Avg Churn Probability</h3>
    <h1>{avg_probability:.2f}%</h1>
</div>
""",
                unsafe_allow_html=True
            )

        # ==========================================
        # RESULTS TABLE
        # ==========================================

        st.markdown("---")

        st.subheader("📋 Prediction Results")

        st.dataframe(

            results_df,

            use_container_width=True,

            height=500
        )

        # ==========================================
        # DOWNLOAD BUTTON
        # ==========================================

        csv = results_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="📥 Download Predictions CSV",

            data=csv,

            file_name="batch_predictions.csv",

            mime="text/csv"
        )

        # ==========================================
        # AI BUSINESS INSIGHTS
        # ==========================================

        st.markdown("---")

        st.subheader("🤖 Executive AI Insights")

        if st.button(
            "Generate Executive AI Report"
        ):

            with st.spinner(
                "AI is analyzing customer churn trends..."
            ):

                insights = generate_batch_ai_insights(
                    results_df
                )

            st.markdown(
                """
                <div class="custom-card">
                """,
                unsafe_allow_html=True
            )

            st.markdown(insights)

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            # ==========================================
            # PDF REPORT
            # ==========================================

            pdf_path = generate_pdf_report(
                insights
            )

            if pdf_path is not None:

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(

                        label="📄 Download Executive PDF Report",

                        data=pdf_file,

                        file_name="executive_churn_report.pdf",

                        mime="application/pdf"
                    )

        # ==========================================
        # SUCCESS MESSAGE
        # ==========================================

        premium_alert(
    "Batch prediction completed successfully.",
    "success"
)

    except Exception as e:

        st.error(
            f"""
            Batch prediction failed.

            Details:
            {e}
            """
        )