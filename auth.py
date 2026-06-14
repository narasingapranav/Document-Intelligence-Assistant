import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

cred = credentials.Certificate("serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def verify_user(id_token):
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None