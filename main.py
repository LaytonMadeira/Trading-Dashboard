import streamlit as st
import yfinance as yf


st.write("## Welcome to the Trading Dashboard!")

#get user input
inp, timeframe = st.columns(2)
with inp:
    inp = st.text_input("Enter a ticker symbol below:", placeholder = "VOO, AAPL, SCHD, etc.", autocomplete="off")
with timeframe:
    timeframe = st.text_input("Enter the number of years to look back", placeholder = "1, 2, 3, etc. (integers)", autocomplete="off")

df = None

if inp:
    st.write(f"Searching for value: {inp}")
    df = yf.download(f"{inp}", period=f"{1 if not timeframe else timeframe}y")

    # display whether stock data was acquired
    st.write("\n")
    st.write(f"Data aquisition status: {not df.empty}")
    # st.write()

    # data found
    if not df.empty:
        st.line_chart(df["Close"])
