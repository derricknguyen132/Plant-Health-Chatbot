import os
import pandas as pd
import streamlit as st
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

# Check password to proceed
if not check_password():  
    st.stop()

# Load FAQ data
faq_file_path = './data/FAQ.csv'
if not os.path.isfile(faq_file_path):
    st.error("The file FAQ.csv does not exist at the specified path.")
    st.stop()

# Load questions and answers from CSV file
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

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

# Create input form for user query
with st.form(key="form"):
    st.subheader("Ask your gardening question")
    user_prompt = st.text_area("Enter your question here", height=100)
    submitted = st.form_submit_button("Submit")

# Process user input upon submission
if submitted:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if is_prompt_relevant(user_prompt):
        response, source = chatbot_response(user_prompt, df, model)
        st.session_state.messages.append({"role": "bot", "content": response})
        log_conversation(user_prompt, response, source)  # Log conversation
    else:
        response = "Your question seems to be outside the scope of gardening. Please try again."
        st.session_state.messages.append({"role": "bot", "content": response})
