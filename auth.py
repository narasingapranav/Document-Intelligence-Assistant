import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

# -----------------------------
# FIREBASE ADMIN INIT (backend)
# -----------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE_ADMIN"])
    firebase_admin.initialize_app(cred)


# -----------------------------
# VERIFY ID TOKEN (backend use)
# -----------------------------
def verify_user(id_token):
    try:
        decoded = admin_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None


# -----------------------------
# LOGIN (REST API - frontend safe)
# -----------------------------
def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={st.secrets['FIREBASE_API_KEY']}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    res = requests.post(url, json=payload)
    return res.json()


# -----------------------------
# REGISTER (REST API)
# -----------------------------
def register(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={st.secrets['FIREBASE_API_KEY']}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    res = requests.post(url, json=payload)
    return res.json()