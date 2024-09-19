import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def calculate_savings_growth(monthly_savings, initial_savings, months, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12
    savings = [initial_savings]
    for _ in range(1, months + 1):
        new_balance = savings[-1] * (1 + monthly_interest_rate) + monthly_savings
        savings.append(new_balance)
    return savings

st.set_page_config(layout="wide")
st.title("Savings Comparison: Monthly Savings vs Initial Lump Sum")

# Sidebar for user inputs
with st.sidebar:
    st.header("Input Parameters")
    monthly_savings = st.number_input("Monthly savings amount", min_value=0.0, value=500.0, step=100.0)
    initial_lump_sum = st.number_input("Initial lump sum", min_value=0.0, value=300000.0, step=1000.0)
    annual_interest_rate = st.slider("Annual interest rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    years = st.slider("Number of years to project", min_value=1, max_value=30, value=10)

# Calculate savings growth for both scenarios
months = years * 12
monthly_savings_growth = calculate_savings_growth(monthly_savings, 0, months, annual_interest_rate)
lump_sum_growth = calculate_savings_growth(0, initial_lump_sum, months, annual_interest_rate)

# Create DataFrame for plotting
df = pd.DataFrame({
    'Month': range(months + 1),
    'Monthly Savings': monthly_savings_growth,
    'Initial Lump Sum': lump_sum_growth
})

# Create interactive graph
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Month'], y=df['Monthly Savings'], mode='lines', name='Monthly Savings'))
fig.add_trace(go.Scatter(x=df['Month'], y=df['Initial Lump Sum'], mode='lines', name='Initial Lump Sum'))

fig.update_layout(
    title='Savings Growth Comparison',
    xaxis_title='Month',
    yaxis_title='Total Savings ($)',
    legend_title='Scenario',
    height=600
)

# Display the graph
st.plotly_chart(fig, use_container_width=True)

# Display additional information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Savings Scenario")
    st.write(f"Monthly contribution: ${monthly_savings:.2f}")
    st.write(f"Total saved after {years} years: ${monthly_savings_growth[-1]:.2f}")
    st.write(f"Total contributions: ${monthly_savings * months:.2f}")
    st.write(f"Interest earned: ${monthly_savings_growth[-1] - (monthly_savings * months):.2f}")

with col2:
    st.subheader("Initial Lump Sum Scenario")
    st.write(f"Initial investment: ${initial_lump_sum:.2f}")
    st.write(f"Total value after {years} years: ${lump_sum_growth[-1]:.2f}")
    st.write(f"Total contributions: ${initial_lump_sum:.2f}")
    st.write(f"Interest earned: ${lump_sum_growth[-1] - initial_lump_sum:.2f}")

# Comparison and Advice
st.subheader("Comparison and Advice")
if monthly_savings_growth[-1] > lump_sum_growth[-1]:
    difference = monthly_savings_growth[-1] - lump_sum_growth[-1]
    st.write(f"The monthly savings approach results in ${difference:.2f} more after {years} years.")
    st.write("This suggests that regular monthly savings might be more beneficial in the long run.")
elif lump_sum_growth[-1] > monthly_savings_growth[-1]:
    difference = lump_sum_growth[-1] - monthly_savings_growth[-1]
    st.write(f"The initial lump sum approach results in ${difference:.2f} more after {years} years.")
    st.write("This suggests that investing a larger sum upfront might be more beneficial in this case.")
else:
    st.write("Both approaches yield the same result in this scenario.")

st.write("Remember that this is a simplified model. In reality, factors such as tax implications, risk tolerance, and personal financial situations should be considered when making investment decisions.")
