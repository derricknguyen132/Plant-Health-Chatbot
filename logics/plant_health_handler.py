import streamlit as st
import openai

openai.api_key = st.secrets['OPENAI_API_KEY']

# Main chatbot function that integrates all components
def chatbot_response(prompt, df, model):
    if not is_prompt_relevant(prompt):
        return "I'm sorry, it appears I have trouble understanding your request or your request is out of my scope. Please consider rephrasing, elaborating or changing your question."

    combined_answers = find_similar_questions_and_answers(prompt, df)

    if combined_answers:
        final_answer = synthesize_final_answer(prompt, combined_answers)
    else:
        final_answer = "*Disclaimer: The following response may not be accurate as your question was not found in the verified database.*"
        final_answer += f'\n\n{generate_self_response(prompt)}'


    return final_answer