from flask import Flask, render_template, request
import requests
import io
from PIL import Image

app = Flask(__name__)

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
        return response.content
    else:
        print("Failed to generate image. Status code:", response.status_code)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        texts = [request.form.get(f"text{i}", "") for i in range(1, 11)]
        images = [generate_image(text) for text in texts]

        images_texts = []
        for i, img_data in enumerate(images, start=1):
            if img_data:
                image_path = f"static/generated_image_{i}.png"
                with open(image_path, 'wb') as img_file:
                    img_file.write(img_data)
                images_texts.append((image_path, texts[i - 1]))  # texts[i - 1] corresponds to the text for this image

        return render_template('result.html', images_texts=images_texts)

if __name__ == '__main__':
    app.run(debug=True)
