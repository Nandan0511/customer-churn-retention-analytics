# app/pages/2_Prediction.py
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

APP_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.append(APP_DIR)

import streamlit as st

from utils import (
    predict_churn,
    get_risk_level,
    generate_ai_recommendation,
    generate_shap_plot,
    get_customer_segment,
    calculate_revenue_risk,
    generate_single_prediction_pdf,
    load_css,
    get_top_shap_contributors
)

from config import THRESHOLD

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="Prediction",

    page_icon="🤖",

    layout="wide"
)

load_css()

# ==========================================
# TITLE
# ==========================================

st.title("🤖 Customer Churn Prediction")

st.caption(
    "Predict customer churn probability using "
    "Machine Learning and AI-powered insights."
)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    """
    <div class="custom-card">

    <h2>
    🚀 AI-Powered Customer Retention Intelligence
    </h2>

    <p>
    Predict customer churn using XGBoost,
    SHAP Explainability, and AI-generated
    business retention strategies.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# FORM
# ==========================================

with st.form("prediction_form"):

    # ==========================================
    # TABS
    # ==========================================

    tab1, tab2, tab3 = st.tabs([

        "👤 Demographics",

        "📡 Services",

        "💳 Financial"
    ])

    # ==========================================
    # DEMOGRAPHICS
    # ==========================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )

            senior_citizen = st.selectbox(
                "Senior Citizen",
                [0, 1]
            )

            partner = st.selectbox(
                "Partner",
                ["Yes", "No"]
            )

        with col2:

            dependents = st.selectbox(
                "Dependents",
                ["Yes", "No"]
            )

            tenure = st.slider(
                "Tenure (Months)",
                0,
                72,
                12
            )

    # ==========================================
    # SERVICES
    # ==========================================

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            phone_service = st.selectbox(
                "Phone Service",
                ["Yes", "No"]
            )

            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["Yes", "No", "No phone service"]
            )

            internet_service = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"]
            )

            online_security = st.selectbox(
                "Online Security",
                ["Yes", "No", "No internet service"]
            )

        with col2:

            online_backup = st.selectbox(
                "Online Backup",
                ["Yes", "No", "No internet service"]
            )

            device_protection = st.selectbox(
                "Device Protection",
                ["Yes", "No", "No internet service"]
            )

            tech_support = st.selectbox(
                "Tech Support",
                ["Yes", "No", "No internet service"]
            )

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["Yes", "No", "No internet service"]
            )

            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["Yes", "No", "No internet service"]
            )

    # ==========================================
    # FINANCIAL
    # ==========================================

    with tab3:

        col1, col2 = st.columns(2)

        with col1:

            contract = st.selectbox(
                "Contract Type",
                [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ]
            )

            paperless_billing = st.selectbox(
                "Paperless Billing",
                ["Yes", "No"]
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

        with col2:

            monthly_charges = st.number_input(
                "Monthly Charges",
                0.0,
                1000.0,
                70.0
            )

            total_charges = st.number_input(
                "Total Charges",
                0.0,
                10000.0,
                1000.0
            )

    # ==========================================
    # SUBMIT BUTTON
    # ==========================================

    submitted = st.form_submit_button(
        "🔍 Predict Churn"
    )

# ==========================================
# PREDICTION LOGIC
# ==========================================

if submitted:

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================

    avg_charges_per_month = (
        total_charges / (tenure + 1)
    )

    is_long_term = int(
        tenure > 24
    )

    # ==========================================
    # INPUT DATA
    # ==========================================

    input_data = {

        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,

        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,

        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,

        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,

        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,

        "AvgChargesPerMonth": avg_charges_per_month,
        "IsLongTerm": is_long_term
    }

    # ==========================================
    # VALIDATION
    # ==========================================

    if total_charges < monthly_charges:

        st.warning(
            "⚠️ Total charges seem unusually low."
        )

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction, probability = predict_churn(
        input_data
    )

    if probability is None:

        st.error(
            """
            Prediction failed.

            Please check:
            - model pipeline
            - feature columns
            """
        )

        st.stop()

    risk_level = get_risk_level(
        probability
    )

    customer_segment = (
    get_customer_segment(

        probability,

        tenure,

        monthly_charges,

        contract
       )
    )

    monthly_risk, annual_risk = (
    calculate_revenue_risk(

        monthly_charges,

        probability
      )
    )

    # ==========================================
    # AI RECOMMENDATION
    # ==========================================

    with st.spinner(
        "Generating AI retention insights..."
    ):

        shap_drivers = (
            get_top_shap_contributors(
                input_data
            )
        )

        recommendation = (
            generate_ai_recommendation(
                input_data,
                probability,
                shap_drivers
            )
        )
    churn_percentage = probability * 100

    st.markdown("---")

    # ==========================================
    # RESULTS
    # ==========================================

    st.subheader("📊 Prediction Results")

    if prediction == 1:

        st.markdown(
        """
        <div class="prediction-danger-card">
            <div class="prediction-icon">
                ⚠️
            </div>
            <div>
                <div class="prediction-title">
                    Customer is Likely to Churn
                </div>
                <div class="prediction-subtitle">
                    High churn probability detected.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    else:
            st.markdown(
        """
        <div class="prediction-success-card">
            <div class="prediction-icon">
                ✅
            </div>
            <div>
                <div class="prediction-title">
                    Customer is Likely to Stay
                </div>
                <div class="prediction-subtitle">
                    Low churn probability detected.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # PREMIUM METRICS
    # ==========================================

    col1, col2, col3,= st.columns(3)

    # ==========================================
    # CHURN PROBABILITY
    # ==========================================

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>📉 Churn Probability</h3>
                <h1>{churn_percentage:.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================
    # RISK LEVEL
    # ==========================================

    with col2:

        risk_color = "#22c55e"

        if probability >= 0.3:
            risk_color = "#facc15"

        if probability >= 0.6:
            risk_color = "#ef4444"

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>⚠️ Risk Level</h3>
                <h1 style="color:{risk_color};">
                {risk_level}
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================
    # THRESHOLD
    # ==========================================

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>🎯 Threshold</h3>
                <h1>{THRESHOLD * 100:.0f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ==========================================
    # REVENUE ANALYTICS
    # ==========================================

    st.markdown(
    f"""
    <div class="revenue-card">
        <div class="revenue-header">
            Estimated Financial Impact
        </div>
        <div class="revenue-content">
            <div class="revenue-item">
                <h3>💰 Monthly Loss</h3>
                <h1>${monthly_risk:0.2f}</h1>
            </div>
            <div class="revenue-divider"></div>
            <div class="revenue-item">
                <h3>📉 Annual Loss</h3>
                <h1>${annual_risk:0.2f}</h1>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    # ==========================================
    # CUSTOMER SEGMENT
    # ==========================================

    st.markdown("### 🎯 Customer Segment")

    st.markdown(
        f"""
        <div class="segment-card">
            {customer_segment}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # RISK BAR
    # ==========================================

    st.subheader("📈 Risk Score")

    st.progress(float(probability))

    if probability < 0.3:

        st.success(
            "🟢 Low Churn Risk"
        )

    elif probability < 0.6:

        st.warning(
            "🟡 Medium Churn Risk"
        )

    else:

        st.error(
            "🔴 High Churn Risk"
        )

    # ==========================================
    # AI BUSINESS RECOMMENDATION
    # ==========================================

    st.markdown(
        """
        <div class="custom-card">
        """,
        unsafe_allow_html=True
    )

    with st.expander(
        "🤖 View AI Retention Strategy",
        expanded=True
    ):

        st.markdown(recommendation)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # ==========================================
    # SHAP EXPLAINABILITY
    # ==========================================

    st.subheader("🧠 AI Explainability")

    with st.spinner(
        "Generating SHAP explanations..."
    ):

        shap_fig = generate_shap_plot(
            input_data
        )

    if shap_fig is not None:

        st.pyplot(shap_fig)

    else:

        st.warning(
            "SHAP visualization unavailable."
        )

    # ==========================================
    # EXECUTIVE PDF DOWNLOAD
    # ==========================================

    st.markdown(
    "## 🧠 Executive AI Insights"
    )

    pdf_path = (
        generate_single_prediction_pdf(

        input_data,

        churn_percentage,

        risk_level,

        customer_segment,

        monthly_risk,

        annual_risk,

        recommendation
    )
)

    if pdf_path:

       with open(pdf_path, "rb") as pdf_file:

        st.download_button(

            label="📄 Generate Executive AI Report",

            data=pdf_file,

            file_name="customer_churn_report.pdf",

            mime="application/pdf",

            use_container_width=True
        )
    # ==========================================
    # FOOTER
    # ==========================================

    st.caption(
        "Prediction generated using "
        "XGBoost + AI business analysis."
    )