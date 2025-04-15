import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

# Setup
st.set_page_config(layout='wide', page_title="Tech Stocks Dashboard")
st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)
st.title("📈 Tech Stocks Dashboard (2020 - 2024)")

# Sidebar options
tech_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG']
st.sidebar.header("Filters")

# Date range input
start_date = st.sidebar.date_input("Start Date", datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2025, 1, 1))

show_ma = st.sidebar.checkbox("Show Moving Averages (20 & 50 Day)", value=True)
show_volatility = st.sidebar.checkbox("Show 30-Day Volatility", value=False)

# Load data
@st.cache_data
def load_data(tickers, start, end):
    return yf.download(tickers, start=start, end=end)['Close']

data = load_data(tech_stocks, start_date, end_date)

# Stock Returns Summary
st.subheader("📊 Returns Summary")
returns = pd.DataFrame()
returns['7D %'] = data.pct_change(7).iloc[-1] * 100
returns['30D %'] = data.pct_change(30).iloc[-1] * 100
returns['1Y %'] = data.pct_change(252).iloc[-1] * 100
st.dataframe(returns.style.format("{:.2f}").background_gradient(cmap="coolwarm"), use_container_width=True)

st.divider()

# Interactive stock price charts in 2-column grid
st.subheader("📈 Stock Prices")
for i in range(0, len(tech_stocks), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(tech_stocks):
            stock = tech_stocks[i + j]
            with cols[j]:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data[stock], name=f"{stock} Price", line=dict(color='cyan')))
                if show_ma:
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[stock].rolling(20).mean(),
                        name="20-Day MA", line=dict(color='orange', dash='dot')
                    ))
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[stock].rolling(50).mean(),
                        name="50-Day MA", line=dict(color='green', dash='dot')
                    ))
                fig.update_layout(
                    title=f"{stock} Closing Price",
                    xaxis_title="Date", yaxis_title="Price (USD)",
                    template="plotly_dark", height=350, margin=dict(l=10, r=10, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

st.divider()

# Comparison Chart
st.subheader("🔍 Compare Two Stocks")
col1, col2 = st.columns(2)
with col1:
    stock1 = st.selectbox("Select Stock 1", tech_stocks, index=0)
with col2:
    stock2 = st.selectbox("Select Stock 2", tech_stocks, index=1)

fig_compare = go.Figure()
fig_compare.add_trace(go.Scatter(x=data.index, y=data[stock1], name=stock1, line=dict(color='violet')))
fig_compare.add_trace(go.Scatter(x=data.index, y=data[stock2], name=stock2, line=dict(color='gold')))
fig_compare.update_layout(
    title=f"Price Comparison: {stock1} vs {stock2}",
    xaxis_title="Date", yaxis_title="Price (USD)",
    template="plotly_dark", height=400
)
st.plotly_chart(fig_compare, use_container_width=True)

st.divider()

# Correlation Heatmap
st.subheader("📌 Correlation Heatmap")
fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax_corr)
st.pyplot(fig_corr)

st.divider()

# Volatility
if show_volatility:
    st.subheader("📉 30-Day Rolling Volatility")
    for i in range(0, len(tech_stocks), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(tech_stocks):
                stock = tech_stocks[i + j]
                with cols[j]:
                    vol = data[stock].rolling(30).std()
                    fig_vol = go.Figure()
                    fig_vol.add_trace(go.Scatter(x=vol.index, y=vol, name="Volatility", line=dict(color='magenta')))
                    fig_vol.update_layout(
                        title=f"{stock} Volatility (30-Day Std Dev)",
                        xaxis_title="Date", yaxis_title="Volatility",
                        template="plotly_dark", height=300
                    )
                    st.plotly_chart(fig_vol, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<center>Made by Shweta K | Powered by Python & Streamlit</center>", unsafe_allow_html=True)
