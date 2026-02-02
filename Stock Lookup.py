import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

from styles import apply_css

apply_css()

st.write("## Welcome to the Trading Dashboard!")

#get user input
inp, timeframe = st.columns(2)
with inp:
    inp = st.text_input("Enter a ticker symbol:", placeholder = "VOO, AAPL, SCHD, etc.", autocomplete="off")
with timeframe:
    timeframe = st.text_input("(Optional) Enter the period, in years, to examine:", placeholder = "1, 2, 3, etc. (integers)", autocomplete="off")   

if inp:
    st.write(f"Symbol Entered: {inp.upper()}")
    df = yf.download(f"{inp}", period=f"{1 if (not timeframe or not timeframe.isdigit()) else timeframe}y")
    df.columns = df.columns.get_level_values(0) #flatten to remove multindex (not needed for single stock query)
    stock = yf.Ticker(inp)
    stock_name = stock.info.get('longName', 'Company Name Not Found')

    st.write("\n")
    
    # Error check - incorrect ticker
    if df.empty:
        st.write(f"Error: Data not found for {inp.upper()}. Please double check ticker symbol and try again.")
        st.stop()

    buy_signals = st.toggle("Moving Averages", help="Displays 50 day and 200 day moving averages by default, helping investors find golden crosses.")
    plot_cols = ["Close"]

    # calculate 50 day moving average and 200 day moving average and tell whether to buy or not 
    if buy_signals:
        ma_one, ma_two = st.columns(2)
        with ma_one:
            ma_one = st.number_input("Moving Average One:", min_value=1, value=50)
        with ma_two:
            ma_two = st.number_input("Moving Average Two:", min_value=1, value=200)


        df["MA_ONE"] = df["Close"].rolling(window=50 if not ma_one else ma_one).mean()
        df["MA_TWO"] = df["Close"].rolling(window=200).mean()

        plot_cols += ["MA_ONE", "MA_TWO"]

    # data found
    if not df.empty:
        # plot data
        figure = go.Figure()

        # Main Line (WHITE)
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name="Price",
                line=dict(color="white", width=2)
            )
        )

        if buy_signals: 
            # MA50 (RED)
            figure.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["MA_ONE"],
                    mode="lines",
                    name="First MA",
                    line=dict(color="red", width=2)
                )
            )

            # MA_TWO (BLUE)
            figure.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["MA_TWO"],
                    mode="lines",
                    name="Second MA",
                    line=dict(color="blue", width=2)
                )
            )

        #Display graph
        figure.update_layout(
            title={
                'text': f'Price Action for {stock_name}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center', 
                'yanchor': 'top'
                },
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified",
        )

        st.plotly_chart(figure, use_container_width=True)

