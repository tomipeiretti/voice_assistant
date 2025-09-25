import datetime
import os

class SkillNotes:
    intents = ["create_note"]

    def __init__(self, say, asr):
        self.say = say
        self.asr = asr
        self.folder = "notas"
        os.makedirs(self.folder, exist_ok=True)

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "create_note":
            content = entities.get("content", "").strip()

            if not content:
                # No vino texto → pedimos interacción
                self.say("¿Qué querés escribir en la nota?")
                content = self.asr.listen(timeout=10, phrase_time_limit=15).strip()

            if not content:
                self.say("No entendí lo que dijiste, no pude crear la nota")
                return True

            filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
            path = os.path.join(self.folder, filename)

            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.say(f"Guardé tu nota en {filename}")
            except Exception as e:
                print("Error al guardar nota:", e)
                self.say("No pude guardar la nota")

            return True

        return False
