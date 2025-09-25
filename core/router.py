class Router:
    def __init__(self, skills):
        self.registry = {}
        for skill in skills:
            for intent in skill.intents:
                if intent in self.registry:
                    raise ValueError(f"Intent duplicado detectado: {intent}")
                self.registry[intent] = skill

    def route(self, intent: str, entities: dict) -> bool:
        skill = self.registry.get(intent)
        if not skill:
            return False
        return skill.handle(intent, entities)