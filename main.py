import datetime
from adapters.asr import ASRGoogle
from adapters.tts import say
from core.nlu import SimpleNLU
from skills.skill_web import SkillWeb
from skills.skill_fun import SkillFun
from skills.skill_system import SkillSystem
from skills.skill_process import SkillProcess
from skills.skill_network import SkillNetwork
from skills.skill_metrics_logger import SkillMetricsLogger

class Router:
    def __init__(self, skills):
        # Índice intent -> [skill]
        self.registry = {}
        for s in skills:
            for i in getattr(s, 'intents', []):
                self.registry.setdefault(i, []).append(s)

    def route(self, intent: str, entities: dict) -> bool:
        for s in self.registry.get(intent, []):
            if s.handle(intent, entities):
                return True
        return False

# Saludo con contexto horario
def saludo_inicial(say):
    h = datetime.datetime.now().hour
    if h < 6 or h > 20:
        momento = "Buenas noches"
    elif 6 <= h < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    say(f"{momento}. ¿En qué te puedo ayudar?")

def main():
    asr = ASRGoogle()
    nlu = SimpleNLU()

    # Registrar skills
    skills = [
        SkillWeb(say),
        SkillFun(say),
        SkillSystem(say),
        SkillProcess(say),
        SkillNetwork(say),
        SkillMetricsLogger(say),
    ]
    router = Router(skills)

    saludo_inicial(say)

    while True:
        try:
            pedido = asr.listen()
            if not pedido:
                continue

            parsed = nlu.parse(pedido)
            print("DEBUG NLU:", parsed)
            intent, entities = parsed.get("intent"), parsed.get("entities", {})

            if intent == "__none__":
                continue

            if intent == "goodbye":
                say("Nos vemos, avisame si necesitás otra cosa.")
                break

            handled = router.route(intent, entities)
            if not handled:
                say("No entendí. ")
        except KeyboardInterrupt:
            say("Hasta luego.")
            break
        except Exception as e:
            print("Error:", e)
            say("Ocurrió un error. Intentemos de nuevo.")

if __name__ == "__main__":
    main()

