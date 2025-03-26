# auth.py
import streamlit as st

# Approved mobile numbers (in production, store securely)
APPROVED_NUMBERS = {"123456", "+919876543210"}


def authenticate():
    """Handle mobile number authentication"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "mobile_number" not in st.session_state:
        st.session_state.mobile_number = None

    if not st.session_state.authenticated:
        st.title("🔒 Mobile Authentication")
        mobile = st.text_input("Enter Mobile Number (with country code)",
                               placeholder="9807589099")

        if st.button("Verify"):
            if mobile in APPROVED_NUMBERS:
                st.session_state.authenticated = True
                st.session_state.mobile_number = mobile
                st.success("Verified! Loading app...")
                st.rerun()
            else:
                st.error("This number is not authorized")
        return False
    return True


def logout():
    """Handle logout functionality"""
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.mobile_number = None
        st.rerun()
