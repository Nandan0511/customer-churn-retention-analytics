# app/app.py
import streamlit as st

from auth import (
    login,
    check_auth,
    logout
)

from utils import load_css

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="Churn AI Platform",

    page_icon="📊",

    layout="wide"
)

load_css()

# ==========================================
# LOGIN FLOW
# ==========================================

if not check_auth():

    st.navigation(

        [

            st.Page(

                "Home.py",

                title="Home",

                icon="🏠"
            )

        ]

    ).run()

    login()

    st.stop()

# ==========================================
# USER ROLE
# ==========================================

role = st.session_state["role"]

# ==========================================
# USER ROLE
# ==========================================

role = st.session_state["role"]

# ==========================================
# PAGE DEFINITIONS
# ==========================================

home_page = st.Page(

    "Home.py",

    title="Home",

    icon="🏠"
)

dashboard_page = st.Page(

    "pages/1_Dashboard.py",

    title="Dashboard",

    icon="📈"
)

prediction_page = st.Page(

    "pages/2_Prediction.py",

    title="Prediction",

    icon="🤖"
)

insights_page = st.Page(

    "pages/3_Model_Insights.py",

    title="Model Insights",

    icon="📊"
)

batch_page = st.Page(

    "pages/4_Batch_Prediction.py",

    title="Batch Prediction",

    icon="📂"
)

# ==========================================
# ROLE NAVIGATION
# ==========================================

if role == "Admin":

    pages = [

        home_page,

        dashboard_page,

        prediction_page,

        batch_page,

        insights_page
    ]

elif role == "Analyst":

    pages = [

        home_page,

        dashboard_page,

        prediction_page,

        batch_page
    ]

elif role == "User":

    pages = [

        home_page,

        dashboard_page,

        prediction_page
    ]

else:

    pages = [

        home_page,

        dashboard_page
    ]

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(
    f"""
    <div class="user-role-card">
        <div class="role-label">
            Logged in as
        </div>
        <div class="role-name">
            👤 {role}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Logout"):

    logout()

# ==========================================
# NAVIGATION
# ==========================================

pg = st.navigation(pages)

pg.run()