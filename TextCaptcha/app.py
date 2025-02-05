from flask import Flask, render_template, request, redirect, url_for, session, send_file
from captcha.image import ImageCaptcha
import os
import random
import string

app = Flask(__name__)
app.secret_key = "secret_key"

font_path = "static/fonts/arial.ttf" 

# Captcha image
captcha_dir = "static/captcha"
if not os.path.exists(captcha_dir):
    os.makedirs(captcha_dir)

def generate_random_text(length=5):
    """Generate random string for CAPTCHA."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_captcha():
    """Generate CAPTCHA image and save it to disk."""
    captcha_text = generate_random_text()
    session["captcha_text"] = captcha_text

    image = ImageCaptcha(width=300, height=100, fonts=[font_path])
    captcha_path = os.path.join(captcha_dir, "captcha.png")
    image.write(captcha_text, captcha_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        user_input = request.form.get("captcha_input")
        captcha_text = session.get("captcha_text")

        if user_input == captcha_text:
            session.pop("captcha_text", None) #delete the captcha code after user success
            return "Correct CAPTCHA. Proceeding...."
        else:
            # Regenerate CAPTCHA on failure
            create_captcha()
            return render_template("index.html", error="CAPTCHA failed. Please try again.")

    # Generate CAPTCHA for initial GET request
    create_captcha()
    return render_template("index.html")

@app.route("/captcha-image")
def captcha_image():
    """Serve the CAPTCHA image."""
    captcha_path = os.path.join(captcha_dir, "captcha.png")
    return send_file(captcha_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
