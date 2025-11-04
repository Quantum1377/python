from flask import Flask, render_template, request, redirect, url_for
from generator.model import generate_image
from generator.utils import save_image

import os
app = Flask(__name__)

# Pasta onde as imagens geradas são salvas
OUTPUT_FOLDER = "static/generated"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    generated_image = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        if not prompt:
            return render_template("index.html", error="Por favor, insira um prompt.")

        image_bytes = generate_image(prompt)
        image_path = save_image(image_bytes, OUTPUT_FOLDER)
        generated_image = image_path

    return render_template("index.html", generated_image=generated_image)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)
