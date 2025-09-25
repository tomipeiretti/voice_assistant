import re
import math

class SkillCalc:
    intents = ["calculate"]

    def __init__(self, say):
        self.say = say

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "calculate":
            expr = entities.get("expr", "").strip()
            if not expr:
                self.say("Decime qué cuenta querés hacer")
                return True

            expr = expr.lower()

            # Reemplazos básicos
            expr = expr.replace("más", "+").replace("mas", "+")
            expr = expr.replace("menos", "-")
            expr = expr.replace("por", "*").replace("multiplicado por", "*")
            expr = expr.replace("x", "*")
            expr = expr.replace("dividido por", "/")
            expr = expr.replace("elevado a la", "**")
            expr = expr.replace("a la", "**")
            expr = re.sub(r"la ra[ií]z cuadrada de (\d+)", r"math.sqrt(\1)", expr)
            expr = re.sub(r"la ra[ií]z c[uú]bica de (\d+)", r"(\1**(1/3))", expr)
            expr = re.sub(r"la ra[ií]z de (\d+)", r"math.sqrt(\1)", expr)

            # Validar que solo queden caracteres seguros
            if not re.match(r"^[0-9\+\-\*/\.\s\(\)mathsqrt]+$", expr):
                self.say("Lo siento, no pude entender la cuenta")
                return True

            try:
                # Evaluar con math disponible
                result = eval(expr, {"__builtins__": None, "math": math})
                self.say(f"El resultado es {result}")
            except Exception as e:
                print("Error en cálculo:", e)
                self.say("No pude hacer la cuenta")
            return True

        return False

