import streamlit as st
from PIL import Image
import io
import torch
from backend import classify_meme  # Import classification function

# Streamlit UI - Twitter Style
st.set_page_config(page_title="Meme Checker", layout="wide")
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #1DA1F2; /* Twitter blue */
    }
    .tweet-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        margin: 20px auto;
        width: 60%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .tweet-card img {
        border-radius: 12px;
        max-width: 100%;
        height: auto;
    }
    .error-message {
        color: #e0245e; /* Twitter error red */
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">Meme Quality Checker 🕵️‍♂️</h1>', unsafe_allow_html=True)

# Sidebar Upload
st.sidebar.header("Upload Your Meme 📤")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Save image to a temporary buffer
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")

    # Classify meme using the function
    label = classify_meme(img_bytes)

    # Display meme inside a Twitter-style card
    st.markdown('<div class="tweet-card">', unsafe_allow_html=True)

    if label == 0:
        st.image(image, caption="✅ This is a good meme!", use_container_width=True)
    else:
        st.image(image, caption="❌ Hateful meme detected!", use_container_width=True)
        st.markdown('<p class="error-message">This meme contains racism, sexism, nationality, religion, or disability hate. It cannot be uploaded.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
