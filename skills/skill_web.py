import webbrowser
import wikipedia
import pywhatkit

class SkillWeb:
    intents = [
        "open_youtube",
        "open_browser",
        "wiki_search",
        "web_search",
        "play_youtube",
    ]

    def __init__(self, say):
        self.say = say
        wikipedia.set_lang("es")

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "open_youtube":
            self.say("Estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
            return True

        if intent == "open_browser":
            self.say("Estoy abriendo el navegador")
            webbrowser.open("https://www.google.com.ar")
            return True

        if intent == "wiki_search":
            self.say("Buscando en Wikipedia")
            q = (entities.get("q") or "").strip()
            if q:
                try:
                    resumen = wikipedia.summary(q, sentences=1)
                    self.say("Encontré esta información en Wikipedia")
                    self.say(resumen)
                except Exception:
                    self.say("No pude obtener el resumen")
            else:
                self.say("Decime qué querés buscar en Wikipedia")
            return True

        if intent == "web_search":
            q = (entities.get("q") or "").strip()
            if q:
                self.say("Buscando información")
                pywhatkit.search(q)
                self.say("Esto es lo que he encontrado")
            else:
                self.say("Decime qué querés buscar en internet")
            return True

        if intent == "play_youtube":
            q = (entities.get("q") or "").strip()
            if q:
                self.say("Reproduciendo")
                pywhatkit.playonyt(q)
            else:
                self.say("Decime qué querés reproducir")
            return True

        return False