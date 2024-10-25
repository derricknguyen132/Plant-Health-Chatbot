import streamlit as st
import pandas as pd
import openai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
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

# Load environment variables once
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


if not os.path.isfile('./data/FAQ.csv'):
    raise FileNotFoundError("The file FAQ.csv does not exist at the specified path.")

# Load the questions and answers from the CSV file once
df = pd.read_csv('./data/FAQ.csv', encoding='latin1')

# Initialize SentenceTransformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')



# Create input form for user query
form = st.form(key="form")
form.subheader("Ask your gardening question")

user_prompt = form.text_area("Enter your question here", height=200)

# Process the user's input upon submission
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    
    # Pass the initialized `df` and `model` to the chatbot logic
    response = chatbot_response(user_prompt, df, model)
    st.write(response)
