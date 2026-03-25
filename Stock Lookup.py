import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime, timedelta

# alpaca
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from alpaca.data.enums import Adjustment

# apply site-wide styles
from styles import apply_css
apply_css()

data_client = StockHistoricalDataClient(
    api_key=st.secrets["ALPACA_KEY"],
    secret_key=st.secrets["ALPACA_SECRET"]
)

trading_client = TradingClient(
    st.secrets["ALPACA_KEY"], 
    st.secrets["ALPACA_SECRET"], 
    paper=True
)

@st.cache_data(show_spinner=False)
def get_stock_data(ticker, length, length_units='y'):
    try:
        # check length input 
        if not length or not str(length).isdigit():
            days = 365
        else:
            val = int(length)
            days = val * 365

        start_date = datetime.now() - timedelta(days=days) 
        request_params = StockBarsRequest(
            symbol_or_symbols=ticker.upper(),
            timeframe=TimeFrame.Day,
            start=start_date,

            # adjust prices
            adjustment=Adjustment.ALL
        )

        bars = data_client.get_stock_bars(request_params)
        df = bars.df

        df = df.reset_index(level=0, drop=True) 
        # df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        df.attrs = {}
        asset = trading_client.get_asset(ticker.upper())
        # return fields needed
        info = {
            'longName': asset.name,
            'shortName': asset.name,
            'symbol': asset.symbol,
            'exchange': asset.exchange,
            'tradable': asset.tradable
        }
        return df, info
    except:
        return pd.DataFrame(), None

@st.cache_data()
def get_stock_name(stock_info, ticker):
    return stock_info.get('longName', ticker.upper() if ticker else 'Company Not Found')

def flatten_stock_data(stock_df):
    # flattens multindex for easier indexing of single stock query
    if isinstance(stock_df.columns, pd.MultiIndex):
        stock_df.columns = df.columns.get_level_values(0)    
    return stock_df

st.write("## Welcome to the Trading Dashboard!")

#get user input
inp, timeframe = st.columns(2)
with inp:
    inp = st.text_input("Enter a ticker symbol:", placeholder = "VOO, AAPL, SCHD, etc.", autocomplete="off")
with timeframe:
    timeframe = st.text_input("(Optional) Enter the period, in years, to examine:", placeholder = "1, 2, 3, etc. (integers)", autocomplete="off").strip()   

if inp:
    inp = inp.upper().strip()
    with st.spinner(f"Searching for {inp}..."):
        df, stock_info = get_stock_data(inp, timeframe, 'y')
        # need to flatten here
        df = flatten_stock_data(df)
        if stock_info:
            stock_name = get_stock_name(stock_info, inp)

    # data was not found
    if df.empty or not stock_info:
        st.write(f"ERROR: Data not found for {inp}. Please check the ticker.")
        st.stop()

    # container for graph
    with st.container():
        buy_signals = st.toggle(
            "Moving Averages", 
            help="Moving Averages help investors find Golden Crosses.")
        plot_cols = ["close"]
        # default moving averages
        ma_one_val = 50
        ma_two_val = 200
        # user wants to view moving averages
        if buy_signals:
            ma_one_col, ma_two_col = st.columns(2)
            with ma_one_col:
                ma_one_val = st.number_input("First MA", min_value=1, value=50)
            with ma_two_col:
                ma_two_val = st.number_input("Second MA", min_value=1, value=200)
            #calc moving averages
            df["Ma_One"] = df["close"].rolling(window=ma_one_val).mean()
            df["Ma_Two"] = df["close"].rolling(window=ma_two_val).mean()
            plot_cols+=["Ma_One", "Ma_Two"]

        figure = go.Figure()

        figure.add_trace(go.Scatter(
            x=df.index,
            y=df["close"],
            mode="lines",
            name="Price",
            line=dict(color='white', width=2)
        ) )
        
        if buy_signals:
            figure.add_trace(go.Scatter(
            x=df.index, 
            y=df["Ma_One"], 
            mode="lines", 
            name=f"{ma_one_val} Day MA", 
            line=dict(color="#FF9B05", width=1.5)
            ))
            
            figure.add_trace(go.Scatter(
            x=df.index, 
            y=df["Ma_Two"], 
            mode="lines", 
            name=f"{ma_two_val} Day MA", 
            line=dict(color="#4b63ff", width=1.5)
            ))

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
            height=600
        )

        st.plotly_chart(figure, use_container_width=True)