from gtts import gTTS

def generate_audio_captcha(text):
    # Generate audio file from text
    tts = gTTS(text, lang='en')
    audio_file = f"audio_{text}.mp3"
    tts.save(audio_file)
    print(f"Audio CAPTCHA saved as {audio_file}")

generate_audio_captcha("5454")
