"""Simple Flask app for testing camera capture from a browser (desktop or mobile)."""

import base64
import binascii
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)

CAPTURE_DIR = os.path.join(app.root_path, "static", "captures")
os.makedirs(CAPTURE_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/capture", methods=["POST"])
def capture():
    data = request.get_json(silent=True) or {}
    image_data = data.get("image", "")

    if "," not in image_data:
        return jsonify({"error": "No image data received"}), 400

    _, encoded = image_data.split(",", 1)
    try:
        binary = base64.b64decode(encoded)
    except (binascii.Error, ValueError):
        return jsonify({"error": "Invalid image data"}), 400

    filename = f"capture_{datetime.now():%Y%m%d_%H%M%S_%f}.jpg"
    with open(os.path.join(CAPTURE_DIR, filename), "wb") as f:
        f.write(binary)

    return jsonify({
        "filename": filename,
        "url": url_for("static", filename=f"captures/{filename}"),
    })


@app.route("/gallery")
def gallery():
    files = sorted(os.listdir(CAPTURE_DIR), reverse=True)
    images = [
        url_for("static", filename=f"captures/{name}")
        for name in files
        if name.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    return render_template("gallery.html", images=images)


if __name__ == "__main__":
    # ssl_context="adhoc" serves over HTTPS with a self-signed cert.
    # Browsers require HTTPS (or localhost) to grant camera access.
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context="adhoc")
