import os

import dotenv
import gspread
import pandas as pd
import streamlit as st

dotenv.load_dotenv()


creds = {
    "type": os.environ.get("TYPE"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY"),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
}

gc = gspread.service_account_from_dict(creds)

wks = gc.open("Supplement Limit Calculator").sheet1

df = pd.DataFrame(wks.get_all_records())

df[df.columns[4]] = pd.to_numeric(df[df.columns[4]])


# Update a range

categories = df["category"].unique().tolist()

excipients = {
    "almond": "almond",
    "almond extract": "almond extract",
}

ingredients = df["ingredient"].unique().tolist()

# st.sidebar.write("Filters")

plant_extracts = {"Ginger Roots": {}}

st.write(
    """
    # ⚖️ Supplement Limit Calculator
    #
    ## Filters
    """
)

category_filter = st.multiselect("Category", categories)

st.write(
    """
    ---
    """
)


col1, col2 = st.columns(2)


with col1:

    selected = st.selectbox(label="Select active ingredient 💊", options=ingredients)

with col2:

    number = st.number_input(label="Input amount of active ingredient ⚖️", value=0)


selected_ingredient = df.where(df["ingredient"] == selected).dropna()


st.dataframe(df)

if number > selected_ingredient["tolerable_upper_intake_level_per_day"].values[0]:
    st.write("📝 You have exceeded the tolerable upper intake level per day")


st.write("")
