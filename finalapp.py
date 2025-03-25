import streamlit as st
#from backend import classify_meme
from PIL import Image
import io

# Streamlit UI
st.title("Meme Quality Checker")
st.sidebar.header("Upload Your Meme")

uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
