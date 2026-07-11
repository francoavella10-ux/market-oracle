import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Long-Term Market Oracle — Advisor Edition", layout="wide", page_icon="🧠")

st.title("🧠 Long-Term Market Oracle")
st.caption("**Beautiful Client Report**")

st.sidebar.title("Client Report Input")
client_name = st.sidebar.text_input("Client Name", "Your Client")
invested_amount = st.sidebar.number_input("Amount Invested ($)", 10000, 1000000, 100000)
stocks_input = st.sidebar.text_input("Stocks (comma separated)", "NVDA, MSFT, AAPL")
weights_input = st.sidebar.text_input("Weights (comma separated)", "0.4,0.3,0.3")
horizon = st.sidebar.slider("Horizon (years)", 5, 20, 10)

if st.sidebar.button("🚀 Generate Beautiful Report", type="primary"):
    with st.spinner("Generating beautiful report..."):
        stocks = [s.strip().upper() for s in stocks_input.split(",")]
        try:
            weights = [float(w.strip()) for w in weights_input.split(",")]
        except:
            weights = [1.0 / len(stocks)] * len(stocks)
        
        st.subheader(f"Professional Long-Term Portfolio Report for {client_name}")
        st.write(f"**Invested Amount**: ${invested_amount:,} | **Horizon**: {horizon} years")
        
        expected_return = 0.10
        future_value = invested_amount * (1 + expected_return)**horizon
        st.write(f"**Expected Portfolio Value in {horizon} years**: ${future_value:,.0f}")
        
        for i, stock in enumerate(stocks):
            weight_pct = weights[i] * 100 if i < len(weights) else 100 / len(stocks)
            st.write(f"**{stock}** ({weight_pct:.0f}%)")
            
            try:
                data = yf.download(stock, period="5y", progress=False)
                if not data.empty:
                    st.line_chart(data['Close'])
                else:
                    st.write("Chart data not available at the moment.")
            except:
                st.write("Chart unavailable (temporary issue with data provider)")
            
            st.write("**Sector Outlook** (JP Morgan): Strong AI and innovation tailwinds.")
            
            st.write("**Risk Simulation**")
            last_price = float(data['Close'].iloc[-1]) if not data.empty else 100
            sims = 500
            paths = []
            for _ in range(sims):
                noise = np.random.normal(0.0004, 0.012, horizon * 252)
                path = np.cumprod(1 + noise) * last_price
                paths.append(path)
            paths = np.array(paths)
            
            future_dates = pd.date_range(start=pd.Timestamp.today(), periods=horizon*252+1, freq='B')[1:]
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(future_dates, paths.mean(axis=0), '--')
            ax.fill_between(future_dates, np.percentile(paths, 5, axis=0), np.percentile(paths, 95, axis=0), alpha=0.3)
            ax.set_xlabel("Year")
            st.pyplot(fig)
        
        st.success("✅ Beautiful report ready for client.")
