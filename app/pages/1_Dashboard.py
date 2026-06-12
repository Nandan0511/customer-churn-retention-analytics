# app/pages/1_Dashboard.py

import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
APP_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

sys.path.append(APP_DIR)

import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    load_css
)

from auth import (
    check_auth,
    logout
)
# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)

load_css()

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

if df is None:

    st.stop()

# ==========================================
# TITLE
# ==========================================

st.title("📈 Customer Churn Dashboard")
st.markdown("""
<div class="custom-card">

<h2>🚀 Enterprise Customer Analytics</h2>

<p>
Analyze churn trends, customer behavior,
AI-powered business insights, and
predictive analytics in one platform.
</p>

</div>
""", unsafe_allow_html=True)
st.caption(
    "Business insights and churn analytics."
)

st.markdown("---")

# ==========================================
# KPI METRICS
# ==========================================

total_customers = len(df)

churn_rate = (
    (df["Churn"] == "Yes").mean() * 100
)

avg_monthly = (
    df["MonthlyCharges"].mean()
)

avg_tenure = (
    df["tenure"].mean()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>👥 Customers</h3>
        <h1>{total_customers}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📉 Churn Rate</h3>
        <h1>{churn_rate:.2f}%</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰 Avg Monthly</h3>
        <h1>${avg_monthly:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📆 Avg Tenure</h3>
        <h1>{avg_tenure:.1f}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# CHARTS
# ==========================================

col1, col2 = st.columns(2)

# ==========================================
# PIE CHART
# ==========================================

with col1:

    fig = px.pie(

        df,

        names="Churn",

        title="📊 Churn Distribution",

        hole=0.55,

        color="Churn",

        color_discrete_map={

            "Yes": "#ef4444",

            "No": "#3b82f6"
        }
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white"
        ),

        title_font_size=24,

        legend_font_size=14,

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
# TENURE HISTOGRAM
# ==========================================

with col2:

    fig = px.histogram(

        df,

        x="tenure",

        color="Churn",

        title="📈 Tenure Distribution",

        color_discrete_map={

            "Yes": "#ef4444",

            "No": "#3b82f6"
        }
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white"
        ),

        title_font_size=24,

        legend_font_size=14,

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
# SECOND ROW
# ==========================================

col3, col4 = st.columns(2)

# ==========================================
# BOX PLOT
# ==========================================

with col3:

    fig = px.box(

        df,

        x="Churn",

        y="MonthlyCharges",

        title="💰 Monthly Charges vs Churn",

        color="Churn",

        color_discrete_map={

            "Yes": "#ef4444",

            "No": "#3b82f6"
        }
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white"
        ),

        title_font_size=24,

        legend_font_size=14,

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
# CONTRACT HISTOGRAM
# ==========================================

with col4:

    fig = px.histogram(

        df,

        x="Contract",

        color="Churn",

        barmode="group",

        title="📑 Contract Type vs Churn",

        color_discrete_map={

            "Yes": "#ef4444",

            "No": "#3b82f6"
        }
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white"
        ),

        title_font_size=24,

        legend_font_size=14,

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