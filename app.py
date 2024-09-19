import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def calculate_mortgage_payment(loan_amount, annual_rate, total_years, interest_only_years):
    monthly_rate = annual_rate / 12
    total_months = total_years * 12
    interest_only_months = interest_only_years * 12
    amortization_months = total_months - interest_only_months

    if amortization_months > 0:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**amortization_months) / ((1 + monthly_rate)**amortization_months - 1)
    else:
        monthly_payment = 0

    return monthly_payment

def calculate_monthly_interest(loan_amount, annual_rate):
    return (loan_amount * annual_rate) / 12

def calculate_house_budget(loan_amount, annual_rate, total_years, interest_only_years, house_insurance, tax):
    monthly_payment = calculate_mortgage_payment(loan_amount, annual_rate, total_years, interest_only_years)
    monthly_interest = calculate_monthly_interest(loan_amount, annual_rate)
    
    if interest_only_years > 0:
        return monthly_interest + house_insurance + tax
    else:
        return monthly_payment + house_insurance + tax

def calculate_apartment_budget(monthly_rent):
    return monthly_rent

def calculate_savings_growth(monthly_savings, initial_savings, months, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12
    savings = [initial_savings]
    for _ in range(1, months + 1):
        new_balance = savings[-1] * (1 + monthly_interest_rate) + monthly_savings
        savings.append(new_balance)
    return savings

def format_currency(amount, currency):
    if currency == "DKK":
        return f"{amount:,.0f} kr"
    elif currency == "USD":
        return f"${amount:,.0f}"
    elif currency == "EUR":
        return f"€{amount:,.0f}"

st.set_page_config(layout="wide")
st.title("Comprehensive Budget and Savings Comparison")

# Sidebar for user inputs
with st.sidebar:
    st.header("General Settings")
    currency = st.selectbox("Select Currency", ["DKK", "USD", "EUR"])
    
    st.header("House vs Apartment Inputs")
    house_price = st.number_input(f"House: Total price", min_value=0, step=10000, value=500000)
    down_payment = st.number_input(f"House: Down payment", min_value=0, step=10000, value=100000)
    loan_amount = house_price - down_payment
    st.write(f"Loan amount: {format_currency(loan_amount, currency)}")
    
    annual_rate = st.slider("Mortgage interest rate (%)", min_value=0.0, max_value=10.0, value=4.0, step=0.1) / 100
    total_years = st.slider("Total loan term (years)", min_value=1, max_value=30, value=30)
    interest_only_years = st.slider("Interest-only period (years)", min_value=0, max_value=min(10, total_years), value=0)
    
    house_insurance = st.number_input(f"House: Insurance (per month)", min_value=0, step=10, value=100)
    tax = st.number_input(f"House: Property tax (per month)", min_value=0, step=10, value=200)
    
    monthly_rent = st.number_input(f"Apartment: Monthly rent", min_value=0, step=100, value=2000)
    
    st.header("Savings Comparison Inputs")
    monthly_savings = st.number_input("Monthly savings amount", min_value=0, value=500, step=100)
    initial_lump_sum = st.number_input("Initial lump sum", min_value=0, value=50000, step=1000)
    savings_interest_rate = st.slider("Savings interest rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    years = st.slider("Number of years to project", min_value=1, max_value=30, value=10)

# Calculate budgets
house_budget = calculate_house_budget(loan_amount, annual_rate, total_years, interest_only_years, house_insurance, tax)
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
    yaxis_title=f'Monthly Cost ({currency})',
    height=400
)

fig_housing.update_traces(text=[format_currency(cost, currency) for cost in comparison_df['Monthly Cost']], textposition='auto')

st.plotly_chart(fig_housing, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("House Costs")
    monthly_payment = calculate_mortgage_payment(loan_amount, annual_rate, total_years, interest_only_years)
    monthly_interest = calculate_monthly_interest(loan_amount, annual_rate)
    
    st.write(f"Total monthly cost: {format_currency(house_budget, currency)}")
    st.write(f"Down payment: {format_currency(down_payment, currency)}")
    if interest_only_years > 0:
        st.write(f"Monthly interest payment: {format_currency(monthly_interest, currency)}")
        st.write(f"Monthly principal payment: {format_currency(0, currency)} (during interest-only period)")
    else:
        st.write(f"Monthly mortgage payment: {format_currency(monthly_payment, currency)}")
        st.write(f"  - Principal: {format_currency(monthly_payment - monthly_interest, currency)}")
        st.write(f"  - Interest: {format_currency(monthly_interest, currency)}")
    st.write(f"Insurance: {format_currency(house_insurance, currency)}")
    st.write(f"Property tax: {format_currency(tax, currency)}")
    
    if interest_only_years > 0:
        st.write(f"Interest-only period: {interest_only_years} years")
        st.write(f"Full mortgage payments start after {interest_only_years} years")
        future_payment = calculate_mortgage_payment(loan_amount, annual_rate, total_years - interest_only_years, 0)
        st.write(f"Future monthly payment after interest-only period: {format_currency(future_payment, currency)}")

with col2:
    st.subheader("Apartment Costs")
    st.write(f"Total monthly cost: {format_currency(apartment_budget, currency)}")
    st.write(f"Monthly rent: {format_currency(monthly_rent, currency)}")

st.write(f"Difference in monthly cost: {format_currency(abs(house_budget - apartment_budget), currency)}")
if house_budget > apartment_budget:
    st.write(f"Living in a house is {format_currency(house_budget - apartment_budget, currency)} more expensive per month.")
else:
    st.write(f"Living in an apartment is {format_currency(apartment_budget - house_budget, currency)} more expensive per month.")

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
    yaxis_title=f'Total Savings ({currency})',
    legend_title='Scenario',
    height=400
)

st.plotly_chart(fig_savings, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Monthly Savings Scenario")
    st.write(f"Monthly contribution: {format_currency(monthly_savings, currency)}")
    st.write(f"Total saved after {years} years: {format_currency(monthly_savings_growth[-1], currency)}")
    st.write(f"Total contributions: {format_currency(monthly_savings * months, currency)}")
    st.write(f"Interest earned: {format_currency(monthly_savings_growth[-1] - (monthly_savings * months), currency)}")

with col4:
    st.subheader("Initial Lump Sum Scenario")
    st.write(f"Initial investment: {format_currency(initial_lump_sum, currency)}")
    st.write(f"Total value after {years} years: {format_currency(lump_sum_growth[-1], currency)}")
    st.write(f"Total contributions: {format_currency(initial_lump_sum, currency)}")
    st.write(f"Interest earned: {format_currency(lump_sum_growth[-1] - initial_lump_sum, currency)}")

# Comparison and Advice
st.subheader("Savings Comparison and Advice")
if monthly_savings_growth[-1] > lump_sum_growth[-1]:
    difference = monthly_savings_growth[-1] - lump_sum_growth[-1]
    st.write(f"The monthly savings approach results in {format_currency(difference, currency)} more after {years} years.")
    st.write("This suggests that regular monthly savings might be more beneficial in the long run.")
elif lump_sum_growth[-1] > monthly_savings_growth[-1]:
    difference = lump_sum_growth[-1] - monthly_savings_growth[-1]
    st.write(f"The initial lump sum approach results in {format_currency(difference, currency)} more after {years} years.")
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
st.write(f"Monthly housing cost: {format_currency(monthly_housing_cost, currency)}")
st.write(f"Planned monthly savings: {format_currency(monthly_savings, currency)}")
st.write(f"Remaining for savings after adjusting for housing cost difference: {format_currency(remaining_for_savings, currency)}")

if remaining_for_savings < monthly_savings:
    st.write("Note: The selected housing option may impact your ability to meet your savings goal.")
    adjusted_savings_growth = calculate_savings_growth(remaining_for_savings, 0, months, savings_interest_rate)
    st.write(f"Adjusted total savings after {years} years: {format_currency(adjusted_savings_growth[-1], currency)}")
    st.write(f"Difference from original savings plan: {format_currency(monthly_savings_growth[-1] - adjusted_savings_growth[-1], currency)}")
