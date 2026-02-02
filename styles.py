import streamlit as st


def apply_css():
    st.markdown("""
    <style>

    /* App background */
    .stApp {
        background-color: #0D0F12;
        color: #e5e7eb;
    }

    /* Headers */
    h1, h2, h3 {
        color: #e5e7eb;
    }
    h2 {
        text-align: center !important;      
    }

    /* Text inputs, number inputs */
    div[data-baseweb="input"] > div {
        background-color: #111827;
        border: 1px solid #8B7BFF;
        border-radius: 8px;
        color: #5454C5;
    }

    /* Placeholder text */
    input::placeholder {
        color: #1B211A;
    }

    /* Target the input element when it is focused */
    div[data-baseweb="input"]:focus-within > div {
        border-color: #FFFFFF !important;
        box-shadow: 0 0 0 1px #FFFFFF !important;
    }

    /* Labels */
    label {
        color: #e5e7eb !important;
        font-weight: 500;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #2563eb;
        border-radius: 8px;
    }

    /* Charts background 
    svg {
        background-color: transparent !important;
    }          
    */

    </style>
    """, unsafe_allow_html=True)