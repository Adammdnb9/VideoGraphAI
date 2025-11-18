"""
ElevenLabs TTS wrapper.
This uses ElevenLabs REST API for text->speech. It requires ELEVENLABS_API_KEY in env.
Docs: https://api.elevenlabs.io
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", None)

if not ELEVEN_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY not set in environment")

BASE_URL = "https://api.elevenlabs.io/v1"

HEADERS = {
    "xi-api-key": ELEVEN_KEY,
    "Content-Type": "application/json"
}

def tts_generate_wav(text, voice_id=None, output_path="output.wav"):
    """
    Generate a wav from text and save to output_path.
    Returns the path to the saved file.
    """
    voice = voice_id or ELEVEN_VOICE_ID
    if not voice:
        raise RuntimeError("No voice_id provided and ELEVENLABS_VOICE_ID not set")

    url = f"{BASE_URL}/text-to-speech/{voice}"
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }
    h = {"xi-api-key": ELEVEN_KEY, "Accept": "audio/wav"}
    r = requests.post(url, json=payload, headers=h, stream=True)
    r.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return output_path
