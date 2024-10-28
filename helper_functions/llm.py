import os
import streamlit as st
import openai
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import util
from datetime import datetime
import requests
import pandas as pd
import base64

# Load the API key from Streamlit secrets
OPENAI_KEY = st.secrets['OPENAI_API_KEY']  # Access open ai API key for language model
OpenAI.api_key = OPENAI_KEY  # Set the OpenAI API key

GITHUB_TOKEN = st.secrets['GITHUB_TOKEN'] # Access git hub api token for logging queries and answers

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)

# Determine relevance of prompt to avoid abuse - checkpoint for future categorizing of queries to access a fragment of big database
def is_prompt_relevant(prompt):
    gardening_keywords = (
        "general greetings, gardening, plant care, fertilization, organic fertilizer, manure, compost, soil health, pests, "
        "diseases, seeds, flowers, fruits, leaves, insect control, "
        "fungal issues, nematodes, bacteria, and viruses."
    )

    query = (
        f"Answer 'Yes' or 'No'. Based on the keywords related to gardening and plant care "
        f"({gardening_keywords}), would someone looking for advice ask this: {prompt}?"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful analyst."},
            {"role": "user", "content": query},
        ]
    )

    answer = response.choices[0].message.content.strip().lower()  # Accessing the response correctly
    return answer == "yes"

# Find similar questions in the database compared to the prompt
def find_similar_questions_and_answers(user_input, df, model):
    df_embeddings = model.encode(df['questions'].tolist(), convert_to_tensor=True)
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(user_embedding, df_embeddings)[0]

    # Collect answers based on similarity
    combined_answers = []
    for index, score in enumerate(cosine_scores):
        if score > 0.65:  
            combined_answers.append(df.iloc[index]['answers'])

    return combined_answers

# Function to synthesize the final answer using GPT
def synthesize_final_answer(prompt, combined_answers):
    combined_text = " ".join(combined_answers)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize within 100 words and provide a coherent response based on the following and avoid repetition: {combined_text}"},
        ]
    )
    return response.choices[0].message.content.strip()  

# Function to generate a self-generated response when no answer in database is found
def generate_self_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"I cannot find any answers in my database for the following question: '{prompt}'. Please provide a response in plant and gardening context."},
        ]
    )
    return response.choices[0].message.content.strip()  # Accessing the response correctly

# Function to log conversation to CSV and upload to GitHub
def log_conversation(user_prompt, response, source, folder='Plant-Health-Chatbot/data', filename='chat_log.csv'):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Full path to the CSV file
    file_path = os.path.join(folder, filename)

    # Prepare data for logging
    log_data = {
        'query': user_prompt,
        'datetime': datetime.now().isoformat(),
        'response': response,
        'source': source
    }
    
    # Create a DataFrame and append to CSV
    log_df = pd.DataFrame([log_data])
    log_df.to_csv(file_path, mode='a', header=not os.path.isfile(file_path), index=False)

    # Upload to GitHub
    upload_to_github(file_path)

def upload_to_github(file_path):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  
    REPO_NAME = 'derricknguyen132/Plant-Health-Chatbot'  

    url = f'https://api.github.com/repos/{REPO_NAME}/contents/{os.path.basename(file_path)}'
    
    # Read the file and encode it
    with open(file_path, 'rb') as f:
        content = f.read()
    content_b64 = base64.b64encode(content).decode('utf-8')

    # Check if the file already exists
    response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
    
    if response.status_code == 200:
        # File exists, need to update it
        sha = response.json()['sha']
        data = {
            'message': 'Updating chat log CSV file',
            'content': content_b64,
            'sha': sha
        }
    else:
        # File does not exist, create it
        data = {
            'message': 'Uploading chat log CSV file',
            'content': content_b64
        }

    # Upload or update the file
    response = requests.put(url, json=data, headers={'Authorization': f'token {GITHUB_TOKEN}'})
    if response.status_code in [200, 201]:
        print('File uploaded successfully!')
    else:
        print('Failed to upload file:', response.json())
