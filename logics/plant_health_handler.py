import pandas as pd
import openai
from sentence_transformers import SentenceTransformer, util
import re
from transformers import pipeline

# Initialize OpenAI API
openai.api_key = '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'  # Replace with your actual API key


# Load environment variables
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Load the questions and answers from the CSV file
df = pd.read_csv('./data/FAQ.csv')

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Main chatbot function that integrates all components
def chatbot_response(prompt):
    if not is_prompt_relevant(prompt):
        return "I'm sorry, it appears I have trouble understanding your request or your request is out of my scope. Please consider rephrasing, elaborating or changing your question."

    combined_answers = find_similar_questions_and_answers(prompt, df)

    if combined_answers:
        final_answer = synthesize_final_answer(prompt, combined_answers)
    else:
        final_answer = "*Disclaimer: The following response may not be accurate as your question was not found in the verified database.*"
        final_answer += f'\n\n{generate_self_response(prompt)}'


    return final_answer