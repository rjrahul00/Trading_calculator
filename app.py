
import streamlit as st
from auth import authenticate, logout
from PIL import Image
import os

# Authentication check

if not authenticate():
    st.stop()  # Stop execution if not authenticated

# --- Main App Content ---
st.title("📈 Trading Calculator")
st.markdown(f"""
    <div style="text-align: right; font-size: 16px; font-weight: bold;">
        Logged in as: {st.session_state.mobile_number}<br><br>
    </div>
    """,
            unsafe_allow_html=True)

# Market Mood Dropdown
market_mood = "Good"

# Display with centered text and border
st.markdown(f"""
    <div style="
        border: 2px solid #4CAF50;
        padding: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #4CAF50;
        border-radius: 10px;
        width: 50%;
        margin: auto;">
        Current Market Mood: {market_mood}
    </div>
    """,
            unsafe_allow_html=True)

# User Inputs
capital = st.number_input("Capital (Rs)", value=10000.0, step=10000.0)

# Determine the number of rows based on capital division
if capital < 150000:  # Below 1.5 lakh
    num_rows = 3  # Divide into 3 parts
elif 150000 <= capital <= 500000:  # Between 1.5 lakh and 5 lakh
    num_rows = 4  # Divide into 4 parts
else:  # Above 5 lakh
    num_rows = 5  # Divide into 5 parts

# Display the number of rows

# Calculate Position Sizing
position_sizing = int(capital /
                      num_rows)  # Divide capital equally among trades

# Main Calculate Button at the Top
if st.button("Calculate"):
    st.session_state.show_trade_details = True  # Show trade details after clicking

st.write(f"Number of Trades: {num_rows}")

# Check if trade details should be shown
if st.session_state.get("show_trade_details", False):
    st.subheader("Trade Details")

    # Generate rows based on the number of trades
    for i in range(num_rows):
        # Input fields for Entry and SL
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            entry = st.number_input(f"Entry {i + 1} (Rs)",
                                    value=0,
                                    step=1,
                                    key=f"entry_{i}")

        with col2:
            sl = st.number_input(f"SL {i + 1} (Rs)",
                                 value=0,
                                 step=1,
                                 key=f"sl_{i}")

        with col3:
            # Calculate Quantity
            quantity = int(position_sizing /
                           entry) if entry > 0 else 0  # Avoid division by zero
            st.text_input("Quantity",
                          value=quantity,
                          disabled=True,
                          key=f"quantity_{i}")

        with col4:
            # Display Position Sizing
            st.text_input("Position Sizing",
                          value=position_sizing,
                          disabled=True,
                          key=f"position_sizing_{i}")

        with col5:
            # Calculate Target based on Market Mood
            if market_mood == "Best":
                target = int(
                    entry *
                    1.18) if entry > 0 else 0  # 18% target, rounded to integer
            elif market_mood == "Good":
                target = int(
                    entry *
                    1.11) if entry > 0 else 0  # 11% target, rounded to integer
            elif market_mood == "Bad":
                target = int(
                    entry *
                    1.08) if entry > 0 else 0  # 8% target, rounded to integer

            # Display Target
            st.text_input("Target",
                          value=target,
                          disabled=True,
                          key=f"target_{i}")

# Disclaimer
st.info(
    "This calculator is for educational purposes only. Always use proper risk management."
)
logout()

# Path to the local logo image
logo_path = "images/logo.png"

# Custom HTML for fixed footer
st.markdown(f"""
    <style>
    .fixed-bottom {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 15px;
        background: white;
        border-top: 1px solid #eee;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }}

    .logo {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
    }}

    .text {{
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }}
    </style>

    <div class="fixed-bottom">
        <img class="logo" src="{logo_path}" alt="Logo">
        <span class="text">Swing Niveshak</span>
    </div>
    """,
            unsafe_allow_html=True)
