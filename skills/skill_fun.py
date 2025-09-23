import pyjokes

class SkillFun:
    intents = ["tell_joke"]

    def __init__(self, say):
        self.say = say

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "tell_joke":
            try:
                # pyjokes soporta 'es' para algunos chistes
                self.say(pyjokes.get_joke("es"))
            except Exception:
                self.say("No tengo un chiste ahora mismo, probá otra vez")
            return True
        return False