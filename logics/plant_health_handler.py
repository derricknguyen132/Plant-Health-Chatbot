from helper_functions.llm import find_similar_questions_and_answers, synthesize_final_answer, generate_self_response

# Main chatbot function that integrates all components
def chatbot_response(prompt, df, model):
    combined_answers = find_similar_questions_and_answers(prompt, df, model)

    if combined_answers: #Similar questions are found in database and corresponding answers are synthesized for final answer
        final_answer = synthesize_final_answer(prompt, combined_answers)
        response_source = "database"
    else: #No similar questions are found in database and gpt is allowed to come up with its own answer
        final_answer = "*Disclaimer: The following response may not be accurate as your question was not found in the verified database.*"
        final_answer += f'\n\n{generate_self_response(prompt)}'
        response_source = "self_generate"

    return final_answer, response_source