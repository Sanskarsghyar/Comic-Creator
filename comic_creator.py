import streamlit as st
import requests
import io
from PIL import Image

API_URL = "https://xdwvg9no7pefghrn.us-east-1.aws.endpoints.huggingface.cloud"
HEADERS = {
    "Accept": "image/png",
    "Authorization": "Bearer VknySbLLTUjbxXAXCjyfaFIPwUTCeRXbFSOjwRiCxsxFyhbnGjSFalPKrpvvDAaPVzWEevPljilLVDBiTzfIbWFdxOkYJxnOPoHhkkVGzAknaOulWggusSFewzpqsNWM",
    "Content-Type": "application/json"
}

def generate_image(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        return image
    else:
        print("Failed to generate image. Status code:", response.status_code)
        return None

st.title("Comic Creator")

# Collect text inputs for panels
texts = []
for i in range(1, 11):
    text = st.text_input(f"Panel {i}:", key=f"text{i}")
    texts.append(text)

# Generate comics button
if st.button("Generate Comics"):
    images = [generate_image(text) for text in texts]

    st.write("---")  # Add a separator between rows

    # Display images in two rows with five images each
    for i in range(0, 10, 5):
        st.image(images[i:i + 5], caption=[f"Panel {i + j + 1}" for j in range(5)], width=250)

    st.write("---")  # Add another separator
