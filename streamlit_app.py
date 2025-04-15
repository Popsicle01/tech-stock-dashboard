import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')
st.title("📈 Tech Stocks Dashboard (2020 - 2024)")

# Sidebar filters
tech_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG']
show_ma = st.sidebar.checkbox("Show Moving Averages (20 & 50 Day)", value=True)
show_volatility = st.sidebar.checkbox("Show 30-Day Volatility", value=False)

# Load data (cache to speed up app)
@st.cache_data
def load_data():
    data = yf.download(tech_stocks, start="2020-01-01", end="2025-01-01")['Close']
    return data

data = load_data()

st.subheader("📊 Stock Prices")

# Grid layout for stock price charts
cols = st.columns(2)
for i, stock in enumerate(tech_stocks):
    with cols[i % 2]:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(data[stock], label=f"{stock} Price")
        ax.set_title(f"{stock} Closing Price")

        if show_ma:
            ma20 = data[stock].rolling(window=20).mean()
            ma50 = data[stock].rolling(window=50).mean()
            ax.plot(ma20, label="20-Day MA", linestyle='--')
            ax.plot(ma50, label="50-Day MA", linestyle='--')

        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        st.pyplot(fig)

st.divider()

# Correlation Heatmap
st.subheader("📈 Correlation Heatmap Between Stocks")
fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
corr = data.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax_corr)
st.pyplot(fig_corr)

st.divider()

# Volatility Charts
if show_volatility:
    st.subheader("📉 30-Day Rolling Volatility")
    cols_vol = st.columns(2)
    for i, stock in enumerate(tech_stocks):
        with cols_vol[i % 2]:
            vol = data[stock].rolling(window=30).std()
            fig_vol, ax_vol = plt.subplots(figsize=(6, 3))
            ax_vol.plot(vol, label="Volatility")
            ax_vol.set_title(f"{stock} Volatility")
            ax_vol.set_xlabel("Date")
            ax_vol.set_ylabel("Std Dev")
            ax_vol.legend()
            st.pyplot(fig_vol)
