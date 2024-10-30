import os
import pandas as pd
import streamlit as st
import requests
import base64
from datetime import datetime
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from helper_functions.llm import is_prompt_relevant, log_conversation
from logics.plant_health_handler import chatbot_response
from utility import check_password

# Streamlit App Configuration
st.set_page_config(
    layout="centered",
    page_title="Plant Health Chatbot"
)

st.title("Plant Health Chatbot")

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# Check if the CSV file exists

faq_file_path = './data/FAQ.csv'
if not os.path.isfile(faq_file_path):
    st.error("The file FAQ.csv does not exist at the specified path.")
    st.stop()  # Stop the app if the file does not exist

# Load the database of questions and answers from the CSV file 
try:
    df = pd.read_csv(faq_file_path, encoding='latin1')
except Exception as e:
    st.error(f"Error loading FAQ.csv: {e}")
    st.stop()

# Initialize SentenceTransformer model 
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    st.error(f"Error initializing the SentenceTransformer model: {e}")
    st.stop()

# Create input form for user query
form = st.form(key="form")
form.subheader("Ask your gardening question")

user_prompt = form.text_area("Enter your question here", height=200)

# Process the user's input upon submission
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")

    if is_prompt_relevant(user_prompt):
        response, source = chatbot_response(user_prompt, df, model)
        st.write(response)
        log_conversation(user_prompt, response, source) # append query and final answer to log file
    else:
        st.warning("Your question seems to be outside the scope of gardening. Please try again.")
