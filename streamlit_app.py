import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Display Title and Description
st.title("Tenant Feedback")
st.markdown("Provide your thoughts below")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing Tenant data (including the newly added row)
existing_data = conn.read(worksheet="Tenant", usecols=list(range(3)), ttl=5)
existing_data = existing_data.dropna(how="all")

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
        feedback_data = pd.DataFrame(
            [
                {
                    "Date": date.strftime("%Y-%m-%d"),  # Format date as YYYY-MM-DD
                    "Name": name if name else "Anonymous",  # Use 'Anonymous' if name is not provided
                    "Feedback": comment,
                }
            ]
        )

        # Add the new feedback to the existing data
        updated_df = pd.concat([existing_data, feedback_data], ignore_index=True)

        # Update Google Sheets with the new feedback data
        conn.update(worksheet="Tenant", data=updated_df)

        st.success(f"Thank you {name if name else 'Anonymous'}! Your feedback has been submitted.")
