import streamlit as st
from streamlit_theme import st_theme

def apply_css():
    # detects the theme AND forces a rerun if the user changes it
    theme_info = st_theme()
    
    active_theme = theme_info.get("base") if theme_info else "dark"

    if active_theme == "dark":
        bg_color = "#0D0F12"
        text_color = "#e5e7eb"
        input_bg = "#111827"
        input_border = "#8B7BFF"
        input_text = "#5454C5"        
        placeholder_color = "#1B211A" 
        focus_border = "#FFFFFF"
    else:
        bg_color = "#FFFFFF"
        text_color = "#111827"
        input_bg = "#F3F4F6"
        input_border = "#4F46E5"  
        input_text = "#111827"
        placeholder_color = "#6B7280"
        focus_border = "#000000"

    st.markdown(f"""
    <style>
    /* App background */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    /* Headers */
    h1, h2, h3 {{
        color: {text_color};
    }}
    h2 {{
        text-align: center !important;      
    }}
    /* Text inputs, number inputs */
    div[data-baseweb="input"] > div {{
        background-color: {input_bg};
        border: 1px solid {input_border};
        border-radius: 8px;
        color: {input_text};
    }}
    /* Placeholder text */
    input::placeholder {{
        color: {placeholder_color};
    }}
    /* Target the input element when it is focused */
    div[data-baseweb="input"]:focus-within > div {{
        border-color: {focus_border} !important;
        box-shadow: 0 0 0 1px {focus_border} !important;
    }}
    /* Labels */
    label {{
        color: {text_color} !important;
        font-weight: 500;
    }}
    /* Buttons */
    button[kind="primary"] {{
        background-color: #2563eb;
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    return active_theme