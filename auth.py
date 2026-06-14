import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

if not firebase_admin._apps:

    cred_dict = {
        "type": st.secrets["FIREBASE_TYPE"],
        "project_id": st.secrets["FIREBASE_PROJECT_ID"],
        "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
        "private_key": st.secrets["FIREBASE_PRIVATE_KEY"],
        "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
        "client_id": st.secrets["FIREBASE_CLIENT_ID"],
        "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    }

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)


def verify_user(id_token):
    try:
        return auth.verify_id_token(id_token)
    except:
        return None