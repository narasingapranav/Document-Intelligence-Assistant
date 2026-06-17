import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

# -----------------------------

# FIREBASE ADMIN INIT (backend)

# -----------------------------

if not firebase_admin._apps:

```
firebase_config = {
    "type": st.secrets["FIREBASE_ADMIN"]["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_ADMIN"]["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_ADMIN"]["FIREBASE_PRIVATE_KEY"],
    "client_email": st.secrets["FIREBASE_ADMIN"]["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_ADMIN"]["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_ADMIN"]["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_ADMIN"]["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url":
        "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":
        "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40rag-chatbot-636b3.iam.gserviceaccount.com"
}

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
```

# -----------------------------

# VERIFY ID TOKEN

# -----------------------------

def verify_user(id_token):
try:
decoded = admin_auth.verify_id_token(id_token)
return decoded
except Exception:
return None

# -----------------------------

# LOGIN

# -----------------------------

def login(email, password):

```
url = (
    "https://identitytoolkit.googleapis.com/v1/"
    f"accounts:signInWithPassword?key={st.secrets['FIREBASE_API_KEY']}"
)

payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

res = requests.post(url, json=payload)

if res.status_code != 200:
    raise Exception(res.json())

return res.json()
```

# -----------------------------

# REGISTER

# -----------------------------

def register(email, password):

```
url = (
    "https://identitytoolkit.googleapis.com/v1/"
    f"accounts:signUp?key={st.secrets['FIREBASE_API_KEY']}"
)

payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

res = requests.post(url, json=payload)

if res.status_code != 200:
    raise Exception(res.json())

return res.json()
```
