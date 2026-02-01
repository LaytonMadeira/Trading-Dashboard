import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.write("## Welcome to the Trading Dashboard!")

#get user input
inp, timeframe = st.columns(2)
with inp:
    inp = st.text_input("Enter a ticker symbol below:", placeholder = "VOO, AAPL, SCHD, etc.", autocomplete="off")
with timeframe:
    timeframe = st.text_input("Enter the number of years to look back", placeholder = "1, 2, 3, etc. (integers)", autocomplete="off")

df = None

if inp:
    st.write(f"Symbol Entered: {inp.upper()}")
    df = yf.download(f"{inp}", period=f"{1 if not timeframe else timeframe}y")

    df.columns = df.columns.get_level_values(0)

    # display whether stock data was acquired
    st.write("\n")
    st.write(f"Data aquisition status: {not df.empty}")
    buy_signals = st.toggle("Buy Signals", help="Displays 50 day and 200 day moving averages")

    # calculate 50 day moving average and 200 day moving average and tell whether to buy or not 
    if buy_signals:
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()

    plot_cols = ["Close"]

    if buy_signals:
        plot_cols += ["MA50", "MA200"]

    # data found
    if not df.empty:
        st.line_chart(df[plot_cols])


