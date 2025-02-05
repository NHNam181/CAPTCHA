from flask import Flask, render_template, request, redirect, url_for, session, send_file
from captcha.audio import AudioCaptcha
import os
import random
import string

app = Flask(__name__)
app.secret_key = "secret_key"

# Captcha audio directory
audio_captcha_dir = "static/audio_captcha"
if not os.path.exists(audio_captcha_dir):
    os.makedirs(audio_captcha_dir)

def generate_random_text(length=5):
    """Generate random string for CAPTCHA."""
    return ''.join(random.choices(string.digits, k=length))  # Audio CAPTCHA works best with digits

def create_audio_captcha():
    """Generate an audio CAPTCHA and save it to disk."""
    captcha_text = generate_random_text()
    session["captcha_text"] = captcha_text

    audio = AudioCaptcha()
    captcha_path = os.path.join(audio_captcha_dir, "captcha.wav")
    audio.write(captcha_text, captcha_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        user_input = request.form.get("captcha_input")
        captcha_text = session.get("captcha_text")

        if user_input == captcha_text:
            session.pop("captcha_text", None) #delete the captcha code after user success
            return "Correct CAPTCHA. Proceeding..."
        else:
            # Regenerate CAPTCHA on failure
            create_audio_captcha()
            return render_template("index.html", error="CAPTCHA failed. Please try again.")

    # Generate CAPTCHA for initial GET request
    create_audio_captcha()
    return render_template("index.html")

@app.route("/captcha-audio")
def captcha_audio():
    """Serve the CAPTCHA audio file."""
    captcha_path = os.path.join(audio_captcha_dir, "captcha.wav")
    return send_file(captcha_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True)
