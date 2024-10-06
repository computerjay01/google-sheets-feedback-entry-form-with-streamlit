import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Load Google Sheets credentials from secrets.toml
credentials = {
    "type": st.secrets["connections"]["gsheets"]["type"],
    "project_id": st.secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["connections"]["gsheets"]["client_email"],
    "client_id": st.secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
    "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
}

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account credentials
creds = Credentials.from_service_account_info(credentials, scopes=scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"]).worksheet("Tenant")  # Replace 'Tenant' with the actual worksheet name

# Display Title and Description
st.title("Tenant Feedback")
st.markdown("Provide your thoughts below")

# Fetch existing Tenant data (including the newly added row)
existing_data = pd.DataFrame(sheet.get_all_records())

# Display the data in a table
st.subheader("Existing Feedback")
st.dataframe(existing_data)

# Form for submitting new feedback
with st.form(key='feedback_form'):
    # Input fields
    date = st.date_input("Date*", value=datetime.today())
    name = st.text_input("Name (Optional)")
    comment = st.text_area("Comment*")
    
    # Mark mandatory fields
    st.markdown("**required*")
    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

# If the form is submitted
if submit_button:
    if not comment:  # Check if the comment (mandatory) field is filled
        st.warning("Please ensure all mandatory fields are filled.")
        st.stop()
    else:
        # Create a new row of feedback data
        feedback_data = [date.strftime("%Y-%m-%d"), name if name else "Anonymous", comment]
        
        # Append the new feedback to Google Sheets
        sheet.append_row(feedback_data)
        
        st.success(f"Thank you {name if name else 'Anonymous'}! Your feedback has been submitted.")
        
        # Refresh the data after submission
        existing_data = pd.DataFrame(sheet.get_all_records())
        st.dataframe(existing_data)
