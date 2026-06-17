import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

if not firebase_admin._apps:
firebase_config = {
"type": st.secrets["FIREBASE_ADMIN"]["FIREBASE_TYPE"],
"project_id": st.secrets["FIREBASE_PROJECT_ID"],
"private_key_id": st.secrets["FIREBASE_ADMIN"]["FIREBASE_PRIVATE_KEY_ID"],
"private_key": st.secrets["FIREBASE_ADMIN"]["FIREBASE_PRIVATE_KEY"],
"client_email": st.secrets["FIREBASE_ADMIN"]["FIREBASE_CLIENT_EMAIL"],
"client_id": st.secrets["FIREBASE_ADMIN"]["FIREBASE_CLIENT_ID"],
"auth_uri": st.secrets["FIREBASE_ADMIN"]["FIREBASE_AUTH_URI"],
"token_uri": st.secrets["FIREBASE_ADMIN"]["FIREBASE_TOKEN_URI"],
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40rag-chatbot-636b3.iam.gserviceaccount.com"
}

```
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
```

def verify_user(id_token):
try:
return admin_auth.verify_id_token(id_token)
except Exception:
return None

def login(email, password):
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={st.secrets['FIREBASE_API_KEY']}"

```
payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

response = requests.post(url, json=payload)

if response.status_code != 200:
    raise Exception(response.text)

return response.json()
```

def register(email, password):
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={st.secrets['FIREBASE_API_KEY']}"

```
payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

response = requests.post(url, json=payload)

if response.status_code != 200:
    raise Exception(response.text)

return response.json()
```
