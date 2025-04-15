# streamlit_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')

st.title("📈 Tech Stocks Dashboard (2020 - 2024)")

# Sidebar controls
tech_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG']
selected_stock = st.selectbox("Select a Stock", tech_stocks)
show_ma = st.checkbox("Show Moving Averages (20 & 50 day)", value=True)
show_volatility = st.checkbox("Show 30-Day Volatility", value=False)

# Fetch data
@st.cache_data
def load_data():
    data = yf.download(tech_stocks, start="2020-01-01", end="2025-01-01")['Close']
    return data

data = load_data()

# Plot stock price
st.subheader(f"{selected_stock} Price History")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data[selected_stock], label=f'{selected_stock} Price')

if show_ma:
    ma20 = data[selected_stock].rolling(window=20).mean()
    ma50 = data[selected_stock].rolling(window=50).mean()
    ax.plot(ma20, label='20-Day MA')
    ax.plot(ma50, label='50-Day MA')

ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)

# Correlation heatmap
st.subheader("Correlation Heatmap")
corr = data.corr()
fig2, ax2 = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

# Volatility
if show_volatility:
    st.subheader(f"{selected_stock} - Rolling 30-Day Volatility")
    vol = data[selected_stock].rolling(window=30).std()
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(vol, label='30-Day Std Dev')
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Volatility")
    ax3.legend()
    st.pyplot(fig3)
