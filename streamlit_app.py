import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')
st.title("📈 Tech Stocks Dashboard (2020 - 2024)")

# Sidebar filters
tech_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOG']
show_ma = st.sidebar.checkbox("Show Moving Averages (20 & 50 Day)", value=True)
show_volatility = st.sidebar.checkbox("Show 30-Day Volatility", value=False)

# Load data
@st.cache_data
def load_data():
    data = yf.download(tech_stocks, start="2020-01-01", end="2025-01-01")['Close']
    return data

data = load_data()

st.subheader("📊 Interactive Price Charts")

# --- Grid layout for charts ---
for i in range(0, len(tech_stocks), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(tech_stocks):
            stock = tech_stocks[i + j]
            with cols[j]:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data[stock], name=f"{stock} Price", line=dict(color='blue')))
                if show_ma:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[stock].rolling(20).mean(),
                        name="20-Day MA",
                        line=dict(dash='dot', color='orange')
                    ))
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[stock].rolling(50).mean(),
                        name="50-Day MA",
                        line=dict(dash='dot', color='green')
                    ))
                fig.update_layout(
                    title=f"{stock} Closing Price",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=350,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Correlation heatmap (still with matplotlib for now) ---
st.subheader("📈 Correlation Heatmap Between Stocks")
fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax_corr)
st.pyplot(fig_corr)

st.divider()

# --- Volatility Charts ---
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
                    fig_vol.add_trace(go.Scatter(x=vol.index, y=vol, name="Volatility", line=dict(color='purple')))
                    fig_vol.update_layout(
                        title=f"{stock} Volatility (30-Day Std Dev)",
                        xaxis_title="Date",
                        yaxis_title="Volatility",
                        height=300,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig_vol, use_container_width=True)
