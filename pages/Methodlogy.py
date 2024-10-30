import streamlit as st
from PIL import Image  # Import PIL to handle image loading

# Function to check password (replace with your actual password checking logic)
def check_password():
    password = st.text_input("Enter your password:", type="password")
    if password == "your_password":  # Replace "your_password" with your actual password
        return True
    else:
        st.warning("⚠️ Incorrect password.")
        return False

# Password protection for the About Us page
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