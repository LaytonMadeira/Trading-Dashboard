import streamlit as st

import constants as cons
from styles import apply_css


apply_css()

# override certain styles
st.markdown("""
    <style>
        h2,h3 {
        text-align: left !important;      
        }
    </style>
    """, unsafe_allow_html=True)


st.markdown("# Helpful Information", unsafe_allow_html=True)

st.write("### Program Usage")
st.write(f"""
         On the main page, "{cons.PAGE_ONE}", the user may enter a ticker symbol (case does not matter). 
         Optionally, the user can also specify the number of years. 
         This is an integer indicating how far to look back from the current day. 
         If unspecified, the number of years will default to 1.
         \nFurthermore, the user may also display moving averages, allowing them to locate golden crosses. 
         Golden Crosses are one of the many indicators investors use to decide whether to buy or sell a stock.
         The most common moving averages used together are 50 and 200 day moving averages.
         A Golden Cross occurs when the 50-day moving average crosses above the 200-day moving average, indicating positive momentum
         and possibly a good buying opportunity. A Death Cross occurs when the 50-day moving average crosses below the 200 day moving average, 
         indicating negative momentum and a possible shorting or selling opportunity.        
           """)

st.write("### Errors")
st.write(f"""
        On the main page, "{cons.PAGE_ONE}", if an error message is displayed instead of a price action line graph,
        it indicates there was an error fetching the data. In such cases, the user should double-check the entered ticker symbol
        to ensure correctness. 
        If the ticker symbol is correct, there may be a server issue fetching the data. 
        In this case, the user should try again at a later time. 
        \nThank you!
         """)
