
import streamlit as st
import pandas as pd
from datetime import datetime

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

# Loan Eligibility UI
def loan_eligibility_ui():
    st.header("🏠 Loan Eligibility Calculator")
    with st.form("eligibility_form"):
        name = st.text_input("Full Name")
        mobile = st.text_input("10-digit Mobile Number", key="le_mobile")
        address = st.text_area("Address")
        monthly_income = st.number_input("Gross Monthly Salary (INR)", min_value=0)
        monthly_obligation = st.number_input("Total Monthly Obligations (INR)", min_value=0)
        age = st.number_input("Age", min_value=18, max_value=65)
        product_type = st.selectbox("Loan Product", ["Home Loan", "Plot Loan", "Plot Loan + Construction", "LAP"])
        submitted = st.form_submit_button("Check Eligibility")

    if submitted:
        if len(mobile) != 10 or not mobile.isdigit():
            st.error("❌ Invalid mobile number.")
            return

        if age >= 65 or monthly_income <= 0:
            st.error("❌ Invalid input values.")
            return

        net_income = monthly_income - monthly_obligation
        annual_income = monthly_income * 12

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

        interest_rates = {
            "Home Loan": 8.85,
            "Plot Loan": 9.25,
            "Plot Loan + Construction": 8.85,
            "LAP": 11.25
        }

        tenure = get_tenure(age, product_type)
        roi = interest_rates[product_type] / 100 / 12
        foir = get_foir(annual_income)
        eligible_emi = net_income * foir

        loan_eligible = eligible_emi * ((1 - (1 + roi) ** (-tenure * 12)) / roi)
        loan_eligible = round(loan_eligible)

        st.success(f"✅ Eligible Loan Amount: INR {loan_eligible}")
        st.info(f"Tenure: {tenure} years")
        st.caption("NOTE: Final Loan Amount subject to Legal & Technical Valuation")

        data = {
            "Name": name,
            "Mobile": mobile,
            "Address": address,
            "Monthly Income": monthly_income,
            "Monthly Obligation": monthly_obligation,
            "Age": age,
            "Product Type": product_type,
            "Eligible Loan": loan_eligible,
            "Tenure": tenure
        }
        save_to_excel("loan_eligibility_data.xlsx", data)

# Branch Connect UI
def branch_connect_ui():
    st.header("🔗 Branch Connect Services")
    with st.form("branch_form"):
        name = st.text_input("Full Name", key="bc_name")
        account_number = st.text_input("Loan Account Number")
        branch_name = st.text_input("Branch Name")
        mobile = st.text_input("10-digit Mobile Number", key="bc_mobile")
        service_options = [
            "Statement of Accounts", "IT Certificate for Tax",
            "Principal Outstanding", "Rate of Interest",
            "Repraising", "AMORT Schedule"
        ]
        selected_service = st.selectbox("Select Service", service_options)
        submitted = st.form_submit_button("Submit Request")

    if submitted:
        if len(mobile) != 10 or not mobile.isdigit():
            st.error("❌ Invalid mobile number.")
        else:
            st.success(f"✅ Your request for '{selected_service}' has been registered.")
            st.info("📨 A branch support officer will contact you shortly.")
            data = {
                "Name": name,
                "Loan Account Number": account_number,
                "Branch Name": branch_name,
                "Mobile": mobile,
                "Requested Service": selected_service
            }
            save_to_excel("branch_connect_data.xlsx", data)

# Main App
st.set_page_config(page_title="Sundaram CARE", layout="centered")
st.sidebar.title("🏢 Sundaram CARE Menu")
menu = st.sidebar.radio("Navigate to:", [
    "Loan Eligibility", "Branch Connect", "Apply Online",
    "Payment Link", "Customer Login", "Deposits",
    "Document Upload", "Exit"
])

if menu == "Loan Eligibility":
    loan_eligibility_ui()
elif menu == "Branch Connect":
    branch_connect_ui()
elif menu == "Apply Online":
    st.markdown("[👉 Apply Online](https://online.sundaramhome.in/signup/new-customer)")
elif menu == "Payment Link":
    st.markdown("[💳 Payment Link](https://www.sfhome.in/onlineservices/#no-back-button)")
elif menu == "Customer Login":
    st.markdown("[🔐 Customer Login](https://a2b.sundaramhome.in/shflcustomerportal/faces/index#no-back-button)")
elif menu == "Deposits":
    st.markdown("[🏦 Deposits](https://deposits.sundaramhome.in/shfldepositportal/faces/sflogin.jsf?tempId=1)")
elif menu == "Document Upload":
    st.markdown("[📤 Upload Documents](https://online.sundaramhome.in/docupload/)")
elif menu == "Exit":
    st.balloons()
    st.success("🎉 Thank you for using Sundaram CARE!")
