# asr --> Automatic Speech Recognition
import speech_recognition as sr

class ASRGoogle:
    def __init__(self):
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self, timeout: float = 5, phrase_time_limit: float = 7) -> str:
        #return "ip"
        with self.mic as source:
            # Ajuste de ruido ambiente breve
            self.rec.adjust_for_ambient_noise(source, duration=0.4)
            print("Ya podés hablar…")
            try:
                audio = self.rec.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("...")
                return ""
        try:
            text = self.rec.recognize_google(audio, language="es-ES")
            print(f">> Dijiste: {text}")
            return text
        except sr.UnknownValueError:
            print("Ups, no entendí")
            return ""
        except sr.RequestError:
            print("Ups, no hay servicio")
            return ""
        except Exception:
            print("Ups, algo salió mal")
            return ""