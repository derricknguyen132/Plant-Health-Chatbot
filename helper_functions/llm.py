# Determine relevance of prompt

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
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful analyst."},
            {"role": "user", "content": query},
        ]
    )
    
    answer = response['choices'][0]['message']['content'].strip().lower()
    return answer == "yes"

# Function to find similar questions and combine answers
def find_similar_questions_and_answers(user_input, df):
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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize within 100 words and provide a coherent response based on the following and avoid repitition: {combined_text}"},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to generate a self-generated response when no DB answer is found
def generate_self_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"I cannot find any answers in my database for the following question: '{prompt}'. Please provide a general response in plant and gardening context."},
        ]
    )
    return response['choices'][0]['message']['content'].strip()
