import os
import subprocess

class SkillApps:
    intents = ["open_app"]

    def __init__(self, say):
        self.say = say
        # Diccionario de apps conocidas
        self.apps = {
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "spotify": "spotify",
            "visual studio code": "code",
            "notepad": "notepad",
        }

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "open_app":
            app_name = entities.get("app", "").lower()
            if not app_name:
                self.say("Decime qué aplicación querés abrir")
                return True

            # Buscar coincidencia en el diccionario
            for key, cmd in self.apps.items():
                if key in app_name:
                    try:
                        self.say(f"Abriendo {key}")
                        if os.path.isabs(cmd): # Esto para abir apps con rutas completas
                            subprocess.Popen([cmd])
                        else:
                            subprocess.Popen([cmd], shell=True) #Path corto
                    except Exception as e:
                        print("Error al abrir app:", e)
                        self.say(f"No pude abrir {key}")
                    return True

            # Si no la encontramos
            self.say(f"No tengo configurada la aplicación {app_name}")
            return True

        return False
