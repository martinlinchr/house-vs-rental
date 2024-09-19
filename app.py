import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_house_budget(down_payment, monthly_down_payment, house_insurance, tax, debt, price_house, rate):
    monthly_debt_payment = (debt * rate / 12) / (1 - (1 + rate / 12) ** -360)
    total_monthly_cost = monthly_down_payment + house_insurance + tax + monthly_debt_payment
    return total_monthly_cost

def calculate_apartment_budget(monthly_rent, down_payment):
    return monthly_rent

st.title("House vs Apartment Budget Comparison")

# User inputs for House budget
st.header("House Budget")
down_payment_house = st.number_input("Down payment (one time)", min_value=0.0, step=1000.0)
monthly_down_payment = st.number_input("Monthly down payment", min_value=0.0, step=100.0)
house_insurance = st.number_input("House insurance (per month)", min_value=0.0, step=10.0)
tax = st.number_input("Tax (per month)", min_value=0.0, step=10.0)
debt = st.number_input("Debt in total", min_value=0.0, step=1000.0)
price_house = st.number_input("Price of house", min_value=0.0, step=1000.0)
rate = 0.04  # 4% flat rate

# User inputs for Apartment budget
st.header("Apartment Budget")
monthly_rent = st.number_input("Monthly rent", min_value=0.0, step=100.0)
down_payment_apartment = st.number_input("Down payment for apartment (one time)", min_value=0.0, step=1000.0)

# Savings input
savings_goal = st.number_input("Monthly savings goal", min_value=0.0, step=100.0)

# Calculate budgets
house_budget = calculate_house_budget(down_payment_house, monthly_down_payment, house_insurance, tax, debt, price_house, rate)
apartment_budget = calculate_apartment_budget(monthly_rent, down_payment_apartment)

# Create comparison dataframe
comparison_df = pd.DataFrame({
    'Category': ['House', 'Apartment'],
    'Monthly Cost': [house_budget, apartment_budget]
})

# Create interactive graph
fig = go.Figure(data=[
    go.Bar(name='Monthly Cost', x=comparison_df['Category'], y=comparison_df['Monthly Cost'])
])

fig.update_layout(title='House vs Apartment: Monthly Cost Comparison',
                  xaxis_title='Category',
                  yaxis_title='Monthly Cost ($)')

st.plotly_chart(fig)

# Display additional information
st.header("Additional Information")
st.write(f"Total monthly cost for house: ${house_budget:.2f}")
st.write(f"Total monthly cost for apartment: ${apartment_budget:.2f}")
st.write(f"Difference in monthly cost: ${abs(house_budget - apartment_budget):.2f}")

if house_budget > apartment_budget:
    st.write(f"Living in a house is ${house_budget - apartment_budget:.2f} more expensive per month.")
else:
    st.write(f"Living in an apartment is ${apartment_budget - house_budget:.2f} more expensive per month.")

st.write(f"Your monthly savings goal: ${savings_goal:.2f}")

# Advice on down payment vs savings
if down_payment_house > 0:
    years_to_save = down_payment_house / (savings_goal * 12)
    st.write(f"It would take approximately {years_to_save:.1f} years to save the house down payment amount with your current savings goal.")
    st.write("Consider balancing between increasing your down payment to reduce debt and maintaining a healthy savings buffer.")
