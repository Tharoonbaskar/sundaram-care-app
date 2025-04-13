import streamlit as st
import pandas as pd
from datetime import datetime
import math

# Excel saving function
def save_to_excel(filename, data):
    df = pd.DataFrame([data])
    df['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel(filename, index=False)

# Loan Eligibility Helper Functions
def get_tenure(age, product_type):
    max_age = 65
    max_tenure = 25 if product_type in ["Home Loan", "Plot Loan", "Plot Loan + Construction"] else 15
    return min(max_tenure, max_age - age)

def get_foir(income):
    if income <= 300000:
        return 0.5
    elif 300000 < income <= 600000:
        return 0.55
    elif 600000 < income <= 1200000:
        return 0.6
    else:
        return 0.65

def calculate_loan_eligibility(monthly_income, monthly_obligation, age, product_type):
    net_income = monthly_income - monthly_obligation
    annual_income = monthly_income * 12
    interest_rates = {
        "Home Loan": 8.85,
        "Plot Loan": 9.25,
        "Plot Loan + Construction": 8.85,
        "LAP": 11.25
    }
    if product_type not in interest_rates:
        return "Invalid product type."

    tenure = get_tenure(age, product_type)
    roi = interest_rates[product_type] / 100 / 12
    foir = get_foir(annual_income)
    eligible_emi = net_income * foir

    loan_eligible = eligible_emi * ((1 - (1 + roi) ** (-tenure * 12)) / roi)
    return round(loan_eligible), tenure

# Streamlit App
st.set_page_config(page_title="Sundaram Loan App", layout="wide")
st.title("🏠 Sundaram Home Finance - Loan Services")

menu = st.sidebar.radio("Main Menu", [
    "Home", "Loan Eligibility", "Apply Online", "Make Payment",
    "Customer Login", "Deposits Info", "Document Upload",
    "Branch Connect", "Contact Info Update"])

if menu == "Home":
    st.header("Welcome to Sundaram Home Finance")
    st.markdown("""
    Access loan-related services like checking your eligibility,
    uploading documents, connecting with branches, and more.
    """)

elif menu == "Loan Eligibility":
    st.header("📊 Loan Eligibility Calculator")
    with st.form("eligibility_form"):
        name = st.text_input("Full Name")
        mobile = st.text_input("10-digit Mobile Number")
        address = st.text_input("Address")
        monthly_income = st.number_input("Gross Monthly Income", min_value=0)
        monthly_obligation = st.number_input("Monthly Obligations", min_value=0)
        age = st.slider("Your Age", min_value=18, max_value=65)
        product_type = st.selectbox("Loan Product", ["Home Loan", "Plot Loan", "Plot Loan + Construction", "LAP"])
        submitted = st.form_submit_button("Check Eligibility")

        if submitted:
            if len(mobile) == 10 and mobile.isdigit():
                loan_amount, tenure = calculate_loan_eligibility(monthly_income, monthly_obligation, age, product_type)
                st.success(f"Eligible Loan Amount: ₹{loan_amount}")
                st.info(f"Suggested Tenure: {tenure} years")
                st.caption("Note: Final loan amount subject to legal and technical valuation.")
                data = {
                    "Name": name, "Mobile": mobile, "Address": address,
                    "Monthly Income": monthly_income, "Monthly Obligation": monthly_obligation,
                    "Age": age, "Product Type": product_type,
                    "Eligible Loan": loan_amount, "Tenure": tenure
                }
                save_to_excel("loan_eligibility_data.xlsx", data)
            else:
                st.error("Please enter a valid 10-digit mobile number.")

elif menu == "Apply Online":
    st.markdown("[Apply for a Loan Now](https://online.sundaramhome.in/signup/new-customer)", unsafe_allow_html=True)

elif menu == "Make Payment":
    st.markdown("[Make Your Payment Here](https://www.sfhome.in/onlineservices/#no-back-button)", unsafe_allow_html=True)

elif menu == "Customer Login":
    st.markdown("[Customer Portal Login](https://a2b.sundaramhome.in/shflcustomerportal/faces/index#no-back-button)", unsafe_allow_html=True)

elif menu == "Deposits Info":
    st.markdown("[Check Deposit Details](https://deposits.sundaramhome.in/shfldepositportal/faces/sflogin.jsf?tempId=1)", unsafe_allow_html=True)

elif menu == "Document Upload":
    st.markdown("[Upload Your Documents](https://online.sundaramhome.in/docupload/)", unsafe_allow_html=True)

elif menu == "Contact Info Update":
    st.header("📱 Update Contact Information")
    with st.form("contact_update_form"):
        name = st.text_input("Your Name")
        account = st.text_input("Loan Account Number")
        mobile = st.text_input("New Mobile Number")
        email = st.text_input("New Email")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Your contact update request has been submitted.")

elif menu == "Branch Connect":
    st.header("🔗 Branch Connect Request")
    with st.form("branch_form"):
        name = st.text_input("Your Name")
        account_number = st.text_input("Loan Account Number")
        branch_name = st.text_input("Branch Name")
        mobile = st.text_input("10-digit Mobile Number")
        service = st.selectbox("Select Service", [
            "Statement of Accounts", "IT Certificate for Tax", "Principal Outstanding",
            "Rate of Interest", "Repraising", "AMORT Schedule"])
        submitted = st.form_submit_button("Request Service")
        if submitted:
            if len(mobile) == 10 and mobile.isdigit():
                st.success(f"✅ Request for '{service}' submitted. Branch officer will contact you.")
                data = {
                    "Name": name, "Loan Account Number": account_number,
                    "Branch Name": branch_name, "Mobile": mobile,
                    "Requested Service": service
                }
                save_to_excel("branch_connect_data.xlsx", data)
            else:
                st.error("Invalid mobile number. Please enter a valid 10-digit number.")
