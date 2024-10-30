import streamlit as st

from utility import check_password

# Password protection for the About Us page
if not check_password():
    st.stop()

# Title of the page
st.title("Using Guide for Chatbot")

# Welcome message
st.write("Hello, welcome to our gardening advice app! For the best experience, please take note of the following:")

# Guidelines
st.write("1. This app is strictly for gardening information and related topics. The chatbot will not process queries outside gardening.")
st.write("2. You should ask one question at a time.")
st.write("3. Be specific about what plant and the issue you are facing or the information you are seeking. For example, instead of 'why is my plant wilted?', you should try 'why is my lettuce wilted although I water regularly?'")
st.write("4. If the chatbot does not provide you a satisfactory response and deems your question out of its scope, rephrasing your prompt can help.")

# Closing message
st.write("Happy gardening!")