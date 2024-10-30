import streamlit as st
from utility import check_password

# Password protection for the About Us page
if not check_password():
    st.stop()

# About Us Page Content
st.title("About Us")

st.header("Problem Statement")
st.write("""
Plant enthusiasts and hobbyists often face challenges in nurturing and maintaining their plants' health. 
Many lack the expertise to swiftly identify issues related to pests, diseases, and nutrient deficiencies, 
leading to plant deterioration, loss of cherished specimens, and increasing frustration. 
The current approach to obtaining timely and accurate plant health information is cumbersome. 
Enthusiasts must navigate multiple websites, compare various gardening resources, 
and sift through potentially conflicting advice, which can be overwhelming, 
especially when immediate action is necessary to rescue a struggling plant. 
This often leaves hobbyists feeling helpless and discouraged in their gardening journey.
""")

st.header("Objectives")
st.write("""
In response to these challenges, our team aims to develop an AI-powered chatbot tailored for plant enthusiasts. 
This chatbot will provide:
- **General Gardening Information**: Insights into current trends, plant selection, and best practices.
- **Expert Advice on Plant Growth**: Tailored guidance to optimize plant care.
- **Pest and Disease Control**: Practical solutions for maintaining plant health.
""")

st.header("Data Source")
st.write("""
The AI-powered chatbot will leverage our extensive library of FAQs and expert responses developed 
over the years through the Plant Clinic at Gardener Day Out.
""")

st.header("Features")
st.write("""
The chatbot will offer the following capabilities:
- **Comprehensive Gardening Guidance**: Users can access advice on gardening, plant growth, 
and pest and disease management.
- **Query Compilation**: User-submitted queries will be aggregated and pushed to a designated 
GitHub repository for further analysis and database enhancement.
""")
