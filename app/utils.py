# app/utils.py
import streamlit as st
import pandas as pd
import joblib
import os

from dotenv import load_dotenv
from openai import OpenAI

from config import *

import shap
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter
# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# OPENROUTER CLIENT
# ==========================================

client = OpenAI(

    api_key=os.getenv("OPENROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1"
)

# ==========================================
# LOAD CSS
# ==========================================

def load_css():

    try:

        with open(CSS_PATH) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except Exception as e:

        st.warning(
            f"CSS could not be loaded:\n{e}"
        )

# ==========================================
# PREMIUM ALERT CARD
# ==========================================

def premium_alert(
    message,
    alert_type="success"
):

    if alert_type == "success":

        icon = "✅"

        css_class = "premium-success-alert"

    elif alert_type == "warning":

        icon = "⚠️"

        css_class = "premium-warning-alert"

    else:

        icon = "❌"

        css_class = "premium-danger-alert"

    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="premium-alert-icon">
                {icon}
            </div>
            <div class="premium-alert-text">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv(DATA_PATH)

        # Remove extra spaces
        df.columns = df.columns.str.strip()

        return df

    except Exception as e:

        st.error(
            f"""
            Error loading dataset.

            Details:
            {e}
            """
        )

        return None

# ==========================================
# LOAD PIPELINE
# ==========================================

@st.cache_resource
def load_pipeline():

    try:

        pipeline = joblib.load(MODEL_PATH)

        return pipeline

    except Exception as e:

        st.error(
            f"""
            Error loading model.

            Details:
            {e}
            """
        )

        return None

# ==========================================
# LOAD SHAP EXPLAINER
# ==========================================

@st.cache_resource
def load_shap_explainer():

    pipeline = load_pipeline()

    if pipeline is None:

        return None

    try:

        # Automatically get final model
        model = pipeline.steps[-1][1]

        explainer = shap.TreeExplainer(
            model
        )

        return explainer

    except Exception as e:

        st.error(
            f"""
            Error loading SHAP explainer.

            Details:
            {e}
            """
        )

        return None

# ==========================================
# PREDICT CHURN
# ==========================================

def predict_churn(input_data):

    pipeline = load_pipeline()

    if pipeline is None:

        return None, None

    try:

        input_df = pd.DataFrame([input_data])

        probability = (
            pipeline
            .predict_proba(input_df)[0][1]
        )

        prediction = int(
            probability >= THRESHOLD
        )

        return prediction, probability

    except Exception as e:

        st.error(
            f"""
            Prediction error occurred.

            Details:
            {e}
            """
        )

        return None, None

# ==========================================
# GET RISK LEVEL
# ==========================================

def get_risk_level(probability):

    if probability < LOW_RISK:

        return LOW_RISK_LABEL

    elif probability < MEDIUM_RISK:

        return MEDIUM_RISK_LABEL

    return HIGH_RISK_LABEL

# ==========================================
# CUSTOMER SEGMENTATION
# ==========================================

def get_customer_segment(

    probability,
    tenure,
    monthly_charges,
    contract
):

    # ==========================================
    # HIGH VALUE CUSTOMER
    # ==========================================

    if (

        tenure >= 48

        and monthly_charges >= 80

        and probability < 0.30
    ):

        return (
            "🏆 High Value Customer"
        )

    # ==========================================
    # AT RISK CUSTOMER
    # ==========================================

    elif probability >= 0.60:

        return (
            "⚠️ At Risk Customer"
        )

    # ==========================================
    # LOYAL CUSTOMER
    # ==========================================

    elif (

        tenure >= 24

        and probability < 0.30
    ):

        return (
            "💎 Loyal Customer"
        )

    # ==========================================
    # NEW CUSTOMER
    # ==========================================

    elif tenure <= 6:

        return (
            "🆕 New Customer"
        )

    # ==========================================
    # LOW ENGAGEMENT
    # ==========================================

    elif (

        contract == "Month-to-month"

        and probability >= 0.40
    ):

        return (
            "📉 Low Engagement Customer"
        )

    # ==========================================
    # DEFAULT
    # ==========================================

    return (
        "📊 Standard Customer"
    )

# ==========================================
# REVENUE RISK ESTIMATION
# ==========================================

def calculate_revenue_risk(

    monthly_charges,
    probability
):

    monthly_risk = (

        monthly_charges *
        probability
    )

    annual_risk = (
        monthly_risk * 12
    )

    return (

        round(monthly_risk, 2),

        round(annual_risk, 2)
    )
# ==========================================
# AI BUSINESS RECOMMENDATION
# ==========================================

def generate_ai_recommendation(
    customer_data,
    probability,
    shap_drivers
):

    try:

        prompt = f"""
You are a senior telecom customer retention strategist.

Analyze the customer profile and generate an executive-level retention report.

Customer Data:
{customer_data}

Churn Probability:
{probability:.2%}

Risk Classification:

- Low Risk: < 25%
- Medium Risk: 25% to 70%
- High Risk: > 70%

Top Churn Drivers:

1. {shap_drivers[0]}
2. {shap_drivers[1]}
3. {shap_drivers[2]}

The churn drivers above are the primary reasons for churn risk and must be used when generating the report.

Generate a professional executive business report in markdown.

STRICTLY follow this structure:

## Risk Summary

Write 2 concise executive-level business sentences.

The risk description MUST align with the churn probability:

- Low Risk → low retention risk
- Medium Risk → moderate retention risk
- High Risk → high retention risk

## Main Churn Drivers

Use ONLY the churn drivers listed above.

Explain briefly why each factor increases churn risk.

- Driver 1
- Driver 2
- Driver 3

## Retention Strategy

Provide 3 actionable retention recommendations directly linked to the churn drivers.

Use bullet points only.

Do NOT write:

- Recommendation 1
- Recommendation 2
- Recommendation 3

## Personalized Offer

Write 1 concise personalized retention offer tailored to this customer.

Rules:

- Use markdown formatting
- Keep the report concise and professional
- Use business-friendly language
- Explain factors in plain English
- Base all recommendations on the provided churn drivers
- Do not mention SHAP, machine learning, AI, or model explanations
- Do not repeat information across sections
- Do not create additional sections
- Do not include introductions or conclusions
"""

        response = client.chat.completions.create(

            model="openai/gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are an expert telecom "
                        "customer retention strategist."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            max_tokens=300,

            timeout=30
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            "AI recommendation could "
            f"not be generated.\n\nError:\n{e}"
        )

# ==========================================
# GENERATE SHAP VALUES
# ==========================================

def generate_shap_plot(input_data):

    pipeline = load_pipeline()

    if pipeline is None:

        return None

    try:

        input_df = pd.DataFrame([input_data])

        # ==========================================
        # GET PREPROCESSOR + MODEL
        # ==========================================

        preprocessor = pipeline.steps[0][1]

        model = pipeline.steps[-1][1]

        # ==========================================
        # TRANSFORM DATA
        # ==========================================

        transformed_data = preprocessor.transform(
            input_df
        )

        # ==========================================
        # GET FEATURE NAMES
        # ==========================================

        feature_names = (

            preprocessor
            .get_feature_names_out()
        )

        # ==========================================
        # CLEAN FEATURE NAMES
        # ==========================================

        def clean_feature_name(name):

            name = (

                name
                .replace("cat__", "")
                .replace("num__", "")
                .replace("_", " ")
                .title()
            )

            replacements = {

                "Onlinesecurity": "Online Security",
                "Onlinebackup": "Online Backup",
                "Techsupport": "Tech Support",
                "Internetservice": "Internet Service",
                "Paymentmethod": "Payment Method",
                "Monthlycharges": "Monthly Charges",
                "Totalcharges": "Total Charges",
                "Month To Month": "Month-to-Month",
                "Paperlessbilling": "Paperless Billing",
                "Streamingtv": "Streaming TV",
                "Streamingmovies": "Streaming Movies",
                "Multiplelines": "Multiple Lines",
                "Deviceprotection": "Device Protection",
                "Seniorcitizen": "Senior Citizen"
            }

            for old, new in replacements.items():

                name = name.replace(old, new)

            return name

        feature_names = [

            clean_feature_name(name)

            for name in feature_names
        ]

        # ==========================================
        # SHAP EXPLAINER
        # ==========================================

        explainer = shap.TreeExplainer(
            model
        )

        shap_values = explainer.shap_values(
            transformed_data
        )

        # ==========================================
        # CREATE EXPLANATION
        # ==========================================

        explanation = shap.Explanation(

            values=shap_values[0],

            base_values=explainer.expected_value,

            data=transformed_data[0],

            feature_names=feature_names
        )

        # ==========================================
        # WATERFALL PLOT
        # ==========================================

        plt.style.use("dark_background")

        fig, ax = plt.subplots(

            figsize=(12, 7),

            facecolor="#0f172a"
        )

        ax.set_facecolor("#0f172a")

        shap.plots.waterfall(
            explanation,
            max_display=10,
            show=False
        )

        # ==========================================
        # PREMIUM STYLING
        # ==========================================

        fig.patch.set_facecolor(
            "#0f172a"
        )

        for text in ax.texts:

            text.set_color("white")

        ax.tick_params(
            colors="white"
        )

        for spine in ax.spines.values():

            spine.set_color("#334155")

        return fig

    except Exception as e:

        st.error(
            f"""
            SHAP generation failed.

            Details:
            {e}
            """
        )

        return None

# ==========================================
# GET TOP SHAP CONTRIBUTORS
# ==========================================
def get_top_shap_contributors(input_data):

    pipeline = load_pipeline()

    input_df = pd.DataFrame([input_data])

    preprocessor = pipeline.steps[0][1]
    model = pipeline.steps[-1][1]

    transformed_data = preprocessor.transform(
        input_df
    )

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    explainer = shap.TreeExplainer(
        model
    )

    shap_values = explainer.shap_values(
        transformed_data
    )

    shap_df = pd.DataFrame({

        "Feature": feature_names,

        "Impact": abs(shap_values[0])

    })

    top_features = (

        shap_df

        .sort_values(
            "Impact",
            ascending=False
        )

        .head(3)

    )

    shap_drivers = list(
        top_features["Feature"]
    )

    # ==========================================
    # CLEAN FEATURE NAMES
    # ==========================================

    replacements = {

        "cat__Contract_Month-to-month":
            "Month-to-Month Contract",

        "cat__OnlineSecurity_No":
            "No Online Security",

        "num__MonthlyCharges":
            "Monthly Charges",

        "num__tenure":
            "Customer Tenure",

        "cat__TechSupport_No":
            "No Tech Support",

        "cat__OnlineBackup_No":
            "No Online Backup",

        "cat__DeviceProtection_No":
            "No Device Protection",

        "cat__PaperlessBilling_Yes":
            "Paperless Billing",

        "cat__PaymentMethod_Electronic check":
            "Electronic Check Payment"
    }

    shap_drivers = [

        replacements.get(
            driver,
            driver
        )

        for driver in shap_drivers

    ]

    return shap_drivers
# ==========================================
# GENERATE BATCH AI INSIGHTS
# ==========================================

def generate_batch_ai_insights(results_df):

    try:

        # ==========================================
        # SUMMARY METRICS
        # ==========================================

        total_customers = len(results_df)

        churn_customers = len(

            results_df[
                results_df["Prediction"] == "Churn"
            ]
        )

        churn_rate = (

            churn_customers /
            total_customers
        ) * 100

        avg_probability = (

            results_df[
                "Churn Probability"
            ].mean()
        )

        # ==========================================
        # TOP RISK FACTORS
        # ==========================================

        top_contract = (

            results_df["Contract"]
            .value_counts()
            .idxmax()
        )

        top_payment = (

            results_df["PaymentMethod"]
            .value_counts()
            .idxmax()
        )

        # ==========================================
        # AI PROMPT
        # ==========================================

        prompt = f"""
You are a Senior Telecom Business Analyst preparing a report for the executive leadership team.

Analyze the customer churn prediction summary below and provide business insights.

Dataset Summary:
- Total Customers: {total_customers}
- Predicted Churn Customers: {churn_customers}
- Predicted Churn Rate: {churn_rate:.2f}%
- Average Churn Probability: {avg_probability:.2f}%
- Most Common Contract Type: {top_contract}
- Most Common Payment Method: {top_payment}

Instructions:
1. Interpret the churn risk level (Low, Moderate, High).
2. Explain what the contract and payment method trends may indicate.
3. Identify the key business risks.
4. Recommend realistic retention and revenue-protection actions.
5. Focus on telecom industry best practices.

Format EXACTLY as:

## Executive Summary

(2-3 sentences summarizing overall churn situation)

## Key Churn Insights
- Insight 1
- Insight 2
- Insight 3

## Recommended Business Actions
- Action 1
- Action 2
- Action 3

## Strategic Recommendation

(1 short paragraph explaining the most important business strategy)

Requirements:
- Professional executive tone
- Business-focused, not technical
- Actionable recommendations
- Avoid generic statements
- Maximum 250 words
"""

        # ==========================================
        # AI RESPONSE
        # ==========================================

        response = client.chat.completions.create(

            model="openai/gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are an expert telecom "
                        "business strategist."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            max_tokens=400,

            timeout=30
        )

        return (

            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            "AI insights could not "
            f"be generated.\n\nError: {e}"
        )

# ==========================================
# GENERATE PDF REPORT
# ==========================================

def generate_pdf_report(ai_report):

    try:

        pdf_path = "churn_executive_report.pdf"

        # ==========================================
        # DOCUMENT
        # ==========================================

        doc = SimpleDocTemplate(

            pdf_path,

            pagesize=letter
        )

        styles = getSampleStyleSheet()

        story = []

        # ==========================================
        # TITLE
        # ==========================================

        title = Paragraph(

            "Customer Churn Executive Report",

            styles["Title"]
        )

        story.append(title)

        story.append(
            Spacer(1, 20)
        )

        # ==========================================
        # REPORT CONTENT
        # ==========================================

        paragraphs = ai_report.split("\n")

        for para in paragraphs:

            if para.strip():

                p = Paragraph(

                    para,

                    styles["BodyText"]
                )

                story.append(p)

                story.append(
                    Spacer(1, 10)
                )

        # ==========================================
        # BUILD PDF
        # ==========================================

        doc.build(story)

        return pdf_path

    except Exception as e:

        st.error(
            f"""
            PDF generation failed.

            Details:
            {e}
            """
        )

        return None

# ==========================================
# GENERATE SINGLE PREDICTION PDF
# ==========================================

def generate_single_prediction_pdf(

    customer_data,

    churn_probability,

    risk_level,

    customer_segment,

    monthly_risk,

    annual_risk,

    ai_recommendation
):

    try:

        pdf_path = (
            "single_customer_report.pdf"
        )

        # ==========================================
        # DOCUMENT
        # ==========================================

        doc = SimpleDocTemplate(

            pdf_path,

            pagesize=letter
        )

        styles = getSampleStyleSheet()

        story = []

        # ==========================================
        # TITLE
        # ==========================================

        title = Paragraph(

            "AI Customer Churn Executive Report",

            styles["Title"]
        )

        story.append(title)

        story.append(
            Spacer(1, 20)
        )

        # ==========================================
        # CUSTOMER DETAILS
        # ==========================================

        customer_info = f"""

        <b>Customer Information</b><br/><br/>

        Gender:
        {customer_data['gender']}<br/>

        Senior Citizen:
        {customer_data['SeniorCitizen']}<br/>

        Partner:
        {customer_data['Partner']}<br/>

        Dependents:
        {customer_data['Dependents']}<br/>

        Tenure:
        {customer_data['tenure']} months<br/>

        Contract:
        {customer_data['Contract']}<br/>

        Monthly Charges:
        ${customer_data['MonthlyCharges']}<br/>

        """

        story.append(

            Paragraph(

                customer_info,

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        # ==========================================
        # PREDICTION SUMMARY
        # ==========================================

        prediction_summary = f"""

        <b>Prediction Summary</b><br/><br/>

        Churn Probability:
        {churn_probability:.2f}%<br/>

        Risk Level:
        {risk_level}<br/>

        Customer Segment:
        {customer_segment}<br/>

        Monthly Revenue Risk:
        ${monthly_risk}<br/>

        Annual Revenue Risk:
        ${annual_risk}<br/>

        """

        story.append(

            Paragraph(

                prediction_summary,

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        # ==========================================
        # AI RECOMMENDATION
        # ==========================================

        ai_section = f"""

        <b>AI Business Recommendation</b><br/><br/>

        {ai_recommendation.replace('\n', '<br/>')}

        """

        story.append(

            Paragraph(

                ai_section,

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        # ==========================================
        # BUILD PDF
        # ==========================================

        doc.build(story)

        return pdf_path

    except Exception as e:

        st.error(
            f"""
            Single prediction PDF generation failed.

            Details:
            {e}
            """
        )

        return None