import streamlit as st
from PIL import Image  # Import PIL to handle image loading
from utility import check_password

# Password protection for the Methodology page
if not check_password():
    st.stop()

# About Us Page Content
st.title("About Us")

# Load and display the image
image_path = './data/User_Prompt.jpg'
try:
    image = Image.open(image_path)
    st.image(image, caption="User Prompt Image", use_column_width=True)
except FileNotFoundError:
    st.error(f"Error: The image file '{image_path}' does not exist.")