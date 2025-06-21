# utils/eleven_labs.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

def generate_voice_reminder(message, voice_id="default-voice-id"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Authorization": f"Bearer {ELEVEN_LABS_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": message,
        "model_id": "eleven_multilingual_v2"
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        audio_path = f"static/audio/reminder_{message_id}.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        return audio_path
    else:
        raise Exception("Erreur lors de la génération du rappel vocal")

def create_reminder_message(rdv):
    heure = rdv['heure'].split(':')[0]
    if int(heure) < 12:
        moment = "avant de prendre votre petit-déjeuner"
    elif int(heure) < 17:
        moment = "avant de prendre un taxi"
    else:
        moment = "avant d'aller dormir"
    return f"Rappel : Vous avez un rendez-vous {rdv['titre']} demain à {rdv['heure']} {moment}."