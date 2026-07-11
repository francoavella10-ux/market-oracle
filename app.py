import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Long-Term Market Oracle", layout="wide", page_icon="🧠")

st.title("🧠 Long-Term Market Oracle")
st.caption("**Client Portfolio Report**")

st.sidebar.title("Client Report Input")
client_name = st.sidebar.text_input("Client Name", "Your Client")
invested_amount = st.sidebar.number_input("Amount Invested ($)", 10000, 1000000, 100000)
horizon = st.sidebar.slider("Horizon (years)", 5, 20, 10)

if st.sidebar.button("🚀 Generate Report", type="primary"):
    with st.spinner("Generating report..."):
        st.subheader(f"Professional Long-Term Portfolio Report for {client_name}")
        st.write(f"**Invested Amount**: ${invested_amount:,} | **Horizon**: {horizon} years")
        
        expected_return = 0.10
        future_value = invested_amount * (1 + expected_return)**horizon
        st.write(f"**Expected Portfolio Value in {horizon} years**: ${future_value:,.0f}")
        
        st.write("**Portfolio Risk Simulation (Monte Carlo)**")
        st.info("The shaded area shows the likely range of outcomes over the next " + str(horizon) + " years.")
        
        last_price = invested_amount
        sims = 500
        paths = []
        for _ in range(sims):
            noise = np.random.normal(0.0004, 0.012, horizon * 252)
            path = np.cumprod(1 + noise) * last_price
            paths.append(path)
        paths = np.array(paths)
        
        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=horizon*252+1, freq='B')[1:]
        fig, ax = plt.subplots(figsize=(10, 6))
        mean_path = paths.mean(axis=0)
        ax.plot(future_dates, mean_path, '--', label="Mean Path")
        ax.fill_between(future_dates, np.percentile(paths, 5, axis=0), np.percentile(paths, 95, axis=0), alpha=0.3, label="Likely Range")
        ax.set_xlabel("Year")
        ax.set_ylabel("Portfolio Value ($)")
        ax.legend()
        st.pyplot(fig)
        
        st.success("✅ Report ready for client.")
