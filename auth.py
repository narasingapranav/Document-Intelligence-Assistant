import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

if not firebase_admin._apps:

    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["FIREBASE_PROJECT_ID"],
        "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
        "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": ""
    })

    firebase_admin.initialize_app(cred)


def verify_user(id_token):
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None