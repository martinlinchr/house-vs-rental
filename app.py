import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def calculate_house_budget(down_payment, monthly_down_payment, house_insurance, tax, debt, price_house, rate):
    monthly_debt_payment = (debt * rate / 12) / (1 - (1 + rate / 12) ** -360)
    total_monthly_cost = monthly_down_payment + house_insurance + tax + monthly_debt_payment
    return total_monthly_cost

def calculate_apartment_budget(monthly_rent):
    return monthly_rent

def calculate_savings_growth(monthly_savings, initial_savings, months, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12
    savings = [initial_savings]
    for _ in range(1, months + 1):
        new_balance = savings[-1] * (1 + monthly_interest_rate) + monthly_savings
        savings.append(new_balance)
    return savings

st.set_page_config(layout="wide")
st.title("Comprehensive Budget and Savings Comparison")

# Sidebar for user inputs
with st.sidebar:
    st.header("House vs Apartment Inputs")
    down_payment_house = st.number_input("House: Down payment (one time)", min_value=0.0, step=1000.0, value=50000.0)
    monthly_down_payment = st.number_input("House: Monthly mortgage payment", min_value=0.0, step=100.0, value=1500.0)
    house_insurance = st.number_input("House: Insurance (per month)", min_value=0.0, step=10.0, value=100.0)
    tax = st.number_input("House: Property tax (per month)", min_value=0.0, step=10.0, value=200.0)
    debt = st.number_input("House: Total mortgage debt", min_value=0.0, step=1000.0, value=300000.0)
    price_house = st.number_input("House: Price", min_value=0.0, step=1000.0, value=350000.0)
    rate = st.slider("Mortgage interest rate (%)", min_value=0.0, max_value=10.0, value=4.0, step=0.1) / 100
    
    monthly_rent = st.number_input("Apartment: Monthly rent", min_value=0.0, step=100.0, value=2000.0)
    
    st.header("Savings Comparison Inputs")
    monthly_savings = st.number_input("Monthly savings amount", min_value=0.0, value=500.0, step=100.0)
    initial_lump_sum = st.number_input("Initial lump sum", min_value=0.0, value=50000.0, step=1000.0)
    savings_interest_rate = st.slider("Savings interest rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    years = st.slider("Number of years to project", min_value=1, max_value=30, value=10)

# Calculate budgets
house_budget = calculate_house_budget(down_payment_house, monthly_down_payment, house_insurance, tax, debt, price_house, rate)
apartment_budget = calculate_apartment_budget(monthly_rent)

# Create comparison dataframe for housing
comparison_df = pd.DataFrame({
    'Category': ['House', 'Apartment'],
    'Monthly Cost': [house_budget, apartment_budget]
})

# House vs Apartment Comparison
st.header("House vs Apartment: Monthly Cost Comparison")
fig_housing = go.Figure(data=[
    go.Bar(name='Monthly Cost', x=comparison_df['Category'], y=comparison_df['Monthly Cost'])
])

fig_housing.update_layout(
    xaxis_title='Category',
    yaxis_title='Monthly Cost ($)',
    height=400
)

st.plotly_chart(fig_housing, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("House Costs")
    st.write(f"Total monthly cost: ${house_budget:.2f}")
    st.write(f"Down payment: ${down_payment_house:.2f}")
    st.write(f"Monthly mortgage: ${monthly_down_payment:.2f}")
    st.write(f"Insurance: ${house_insurance:.2f}")
    st.write(f"Property tax: ${tax:.2f}")

with col2:
    st.subheader("Apartment Costs")
    st.write(f"Total monthly cost: ${apartment_budget:.2f}")
    st.write(f"Monthly rent: ${monthly_rent:.2f}")

st.write(f"Difference in monthly cost: ${abs(house_budget - apartment_budget):.2f}")
if house_budget > apartment_budget:
    st.write(f"Living in a house is ${house_budget - apartment_budget:.2f} more expensive per month.")
else:
    st.write(f"Living in an apartment is ${apartment_budget - house_budget:.2f} more expensive per month.")

# Savings Comparison
st.header("Savings Comparison: Monthly Savings vs Initial Lump Sum")

months = years * 12
monthly_savings_growth = calculate_savings_growth(monthly_savings, 0, months, savings_interest_rate)
lump_sum_growth = calculate_savings_growth(0, initial_lump_sum, months, savings_interest_rate)

df_savings = pd.DataFrame({
    'Month': range(months + 1),
    'Monthly Savings': monthly_savings_growth,
    'Initial Lump Sum': lump_sum_growth
})

fig_savings = go.Figure()
fig_savings.add_trace(go.Scatter(x=df_savings['Month'], y=df_savings['Monthly Savings'], mode='lines', name='Monthly Savings'))
fig_savings.add_trace(go.Scatter(x=df_savings['Month'], y=df_savings['Initial Lump Sum'], mode='lines', name='Initial Lump Sum'))

fig_savings.update_layout(
    xaxis_title='Month',
    yaxis_title='Total Savings ($)',
    legend_title='Scenario',
    height=400
)

st.plotly_chart(fig_savings, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Monthly Savings Scenario")
    st.write(f"Monthly contribution: ${monthly_savings:.2f}")
    st.write(f"Total saved after {years} years: ${monthly_savings_growth[-1]:.2f}")
    st.write(f"Total contributions: ${monthly_savings * months:.2f}")
    st.write(f"Interest earned: ${monthly_savings_growth[-1] - (monthly_savings * months):.2f}")

with col4:
    st.subheader("Initial Lump Sum Scenario")
    st.write(f"Initial investment: ${initial_lump_sum:.2f}")
    st.write(f"Total value after {years} years: ${lump_sum_growth[-1]:.2f}")
    st.write(f"Total contributions: ${initial_lump_sum:.2f}")
    st.write(f"Interest earned: ${lump_sum_growth[-1] - initial_lump_sum:.2f}")

# Comparison and Advice
st.subheader("Savings Comparison and Advice")
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

# Overall financial picture
st.header("Overall Financial Picture")
selected_housing = st.radio("Select housing option:", ("House", "Apartment"))
monthly_housing_cost = house_budget if selected_housing == "House" else apartment_budget

remaining_for_savings = max(0, monthly_savings - (monthly_housing_cost - min(house_budget, apartment_budget)))
st.write(f"Based on the selected {selected_housing.lower()} option:")
st.write(f"Monthly housing cost: ${monthly_housing_cost:.2f}")
st.write(f"Planned monthly savings: ${monthly_savings:.2f}")
st.write(f"Remaining for savings after adjusting for housing cost difference: ${remaining_for_savings:.2f}")

if remaining_for_savings < monthly_savings:
    st.write("Note: The selected housing option may impact your ability to meet your savings goal.")
    adjusted_savings_growth = calculate_savings_growth(remaining_for_savings, 0, months, savings_interest_rate)
    st.write(f"Adjusted total savings after {years} years: ${adjusted_savings_growth[-1]:.2f}")
    st.write(f"Difference from original savings plan: ${monthly_savings_growth[-1] - adjusted_savings_growth[-1]:.2f}")
