from helper_functions.llm import find_similar_questions_and_answers, synthesize_final_answer, generate_self_response

# Main chatbot function that integrates all components
def chatbot_response(prompt, df, model):
    combined_answers = find_similar_questions_and_answers(prompt, df, model)

    if combined_answers:
        final_answer = synthesize_final_answer(prompt, combined_answers)
    else:
        final_answer = "*Disclaimer: The following response may not be accurate as your question was not found in the verified database.*"
        final_answer += f'\n\n{generate_self_response(prompt)}'


    return final_answer