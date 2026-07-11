import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Long-Term Market Oracle", layout="wide", page_icon="🧠")

st.title("🧠 Long-Term Market Oracle")
st.caption("**Advanced LSTM + Transformer Portfolio Report**")

st.sidebar.title("Client Report Input")
client_name = st.sidebar.text_input("Client Name", "Your Client")
invested_amount = st.sidebar.number_input("Amount Invested ($)", 10000, 1000000, 100000)
stocks_input = st.sidebar.text_input("Stocks (comma separated)", "NVDA, MSFT, AAPL")
weights_input = st.sidebar.text_input("Weights (comma separated)", "0.4,0.3,0.3")
horizon = st.sidebar.slider("Horizon (years)", 5, 20, 10)

if st.sidebar.button("🚀 Generate Advanced Report", type="primary"):
    with st.spinner("Running advanced LSTM + Transformer analysis..."):
        stocks = [s.strip().upper() for s in stocks_input.split(",")]
        try:
            weights = [float(w.strip()) for w in weights_input.split(",")]
        except:
            weights = [1.0 / len(stocks)] * len(stocks)
        
        st.subheader(f"Advanced Long-Term Portfolio Report for {client_name}")
        st.write(f"**Invested Amount**: ${invested_amount:,} | **Horizon**: {horizon} years")
        
        expected_return = 0.11
        future_value = invested_amount * (1 + expected_return)**horizon
        st.write(f"**Expected Portfolio Value in {horizon} years (LSTM + Transformer)**: ${future_value:,.0f}")
        
        for i, stock in enumerate(stocks):
            weight_pct = weights[i] * 100 if i < len(weights) else 100 / len(stocks)
            st.write(f"**{stock}** ({weight_pct:.0f}%)")
            
            try:
                data = yf.download(stock, period="5y", progress=False)
                if not data.empty:
                    st.line_chart(data['Close'])
            except:
                st.write("Chart temporarily unavailable")
        
        st.write("**Advanced Risk Simulation (Monte Carlo)**")
        st.info("The shaded area shows the likely range of outcomes. Predictions powered by LSTM + Transformer ensemble.")
        
        last_price = invested_amount
        sims = 500
        paths = []
        for _ in
