import streamlit as st
import pandas as pd
from logics.plant_health_handler import chatbot_response

# Streamlit App Configuration
st.set_page_config(
    layout="centered",
    page_title="Plant Health Chatbot"
)

st.title("Plant Health Chatbot")

form = st.form(key="form")
form.subheader("Ask your gardening question")

user_prompt = form.text_area("Enter your question here", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")

    response = chatbot_response(user_prompt)
    st.write(response)
