from pymongo import MongoClient
import streamlit as st

client = MongoClient(st.secrets["MONGO_URI"])

db = client["rag_chatbot"]

users = db["users"]
documents = db["documents"]