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
import io  # Correct import for StringIO

# Load environment variables (including GitHub token)
load_dotenv()

# GitHub Authentication: Read your token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = 'derricknguyen132/Plant-Health-Chatbot'
GITHUB_FILE_PATH = 'data/FAQ.csv'  # Path to the file in the repo

# Function to fetch a file from GitHub using the GitHub API (requires authentication)
def fetch_file_from_github():
    if GITHUB_TOKEN is None:
        st.error("GitHub token not found. Please make sure it's set in the .env file.")
        st.stop()

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        
        # Decode the content from base64
        file_content = base64.b64decode(response.json()['content']).decode('utf-8')
        
        # Load CSV content into pandas DataFrame using io.StringIO
        df = pd.read_csv(io.StringIO(file_content), encoding='latin1')
        return df
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching file from GitHub: {e}")
        st.stop()

# Streamlit App Configuration
st.set_page_config(
    layout="centered",
    page_title="Plant Health Chatbot"
)

st.title("Plant Health Chatbot")

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# Fetch the FAQ data from GitHub
df = fetch_file_from_github()

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
