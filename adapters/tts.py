# adapters/tts_simple.py  --> tts texto a voz
"""
Implementación simple de TTS con pyttsx3.
Recrea el engine en cada llamada para evitar bloqueos.
"""

import pyttsx3

VOICE_ES = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

def say(text: str):
    """Habla un texto usando pyttsx3"""
    if not text:
        return
    engine = pyttsx3.init()
    try:
        engine.setProperty("voice", VOICE_ES)
    except Exception:
        # fallback: busca voz en español por nombre
        for v in engine.getProperty("voices"):
            if any(tag in v.name.lower() for tag in ["spanish", "es"]):
                engine.setProperty("voice", v.id)
                break
    engine.say(str(text))
    engine.runAndWait()
