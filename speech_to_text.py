from openai import OpenAI
client = OpenAI()

def speech_to_text():
    audio_file= open("audio.wav", "rb")
    transcript = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )

    return transcript