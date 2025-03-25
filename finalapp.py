import streamlit as st
from PIL import Image
import io
import torch
from backend import classify_meme  # Import your function

# Streamlit UI
st.title("Meme Quality Checker")
st.sidebar.header("Upload Your Meme")

uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Save image to a temporary buffer
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    
    # Classify meme using the local function
    label = classify_meme(img_bytes)  # Directly calling the function

    if label == 0:
        st.image(image, caption="This is a good meme!", use_container_width=True)
    else:
        st.error("This is a hateful meme containing racism, sexism, nationality, religion or disability, so it cannot be uploaded.")
