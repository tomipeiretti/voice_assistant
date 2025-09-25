import os
import subprocess
from dotenv import load_dotenv

class SkillApps:
    intents = ["open_app"]

    def __init__(self, say):
        self.say = say
        load_dotenv()
        # Diccionario de apps conocidas
        self.apps = {
            "word": os.getenv("APP_WORD"),
            "excel": os.getenv("APP_EXCEL"),
            "powerpoint": os.getenv("APP_POWERPOINT"),
            "spotify": os.getenv("APP_SPOTIFY"),
            "visual studio code": os.getenv("APP_VSCODE"),
            "chrome": os.getenv("APP_CHROME"),
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
                            subprocess.Popen(["start", cmd], shell=True) #Path corto
                    except Exception as e:
                        print("Error al abrir app:", e)
                        self.say(f"No pude abrir {key}")
                    return True

            # Si no la encontramos
            self.say(f"No tengo configurada la aplicación {app_name}")
            return True

        return False
