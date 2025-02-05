from flask import Flask, render_template, request, session, send_file
from gtts import gTTS
import os
import random
import string

app = Flask(__name__)
app.secret_key = "secret_key"

# Captcha audio directory
audio_captcha_dir = "static/audio_captcha"
if not os.path.exists(audio_captcha_dir):
    os.makedirs(audio_captcha_dir)

def generate_random_number(length=3):
    """Generate a random 4-digit number for CAPTCHA."""
    return ''.join(random.choices(string.digits, k=length))

def create_audio_captcha():
    """Generate an audio CAPTCHA and save it to disk."""
    captcha_text = generate_random_number()  # Generate a 4-digit random number
    session["captcha_text"] = captcha_text

    # Generate audio CAPTCHA using gTTS
    tts = gTTS(captcha_text, lang='en')
    captcha_path = os.path.join(audio_captcha_dir, "captcha.mp3")
    tts.save(captcha_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        user_input = request.form.get("captcha_input")
        captcha_text = session.get("captcha_text")

        if user_input == captcha_text:
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
    captcha_path = os.path.join(audio_captcha_dir, "captcha.mp3")
    return send_file(captcha_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
