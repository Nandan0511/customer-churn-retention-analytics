# app/auth.py

import streamlit as st
from credentials import DEMO_USERS
# ==========================================
# LOGIN FUNCTION
# ==========================================

def login():

    st.markdown(
        """
        <div class="custom-card">
        <h2>🔐 Secure Login</h2>
        <p>
        Login to access the AI Churn Platform
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Portfolio Demo • Select a role. Credentials are auto-filled."
   )

    # ==========================================
    # ROLE SELECTION
    # ==========================================

    role = st.selectbox(

        "Login As",

        [
            "Admin",
            "Analyst",
            "User",
            "Viewer"
        ]
    )

    credentials = DEMO_USERS

    # ==========================================
    # PASSWORD
    # ==========================================

    password = st.text_input(
        "Password",
        value= DEMO_USERS[role],
        type="password"
  )

    # ==========================================
    # LOGIN BUTTON
    # ==========================================

    login_btn = st.button(
        "Login"
    )

    # ==========================================
    # LOGIN VALIDATION
    # ==========================================

    if login_btn:

        if password == DEMO_USERS[role]:

            st.session_state["logged_in"] = True

            st.session_state["role"] = role

            st.success(
                f"Welcome {role}"
            )

            st.rerun()

        else:

            st.error(
                "Invalid password"
            )

# ==========================================
# CHECK AUTH
# ==========================================

def check_auth():

    if "logged_in" not in st.session_state:

        st.session_state["logged_in"] = False

    return st.session_state["logged_in"]

# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state["logged_in"] = False

    st.session_state["role"] = None

    st.rerun()