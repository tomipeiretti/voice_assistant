import psutil

# Procesos que nunca se deben cerrar
PROCESOS_PROHIBIDOS = {
    "system", "idle", "explorer.exe", "python.exe", "pythonw.exe",
    "svchost.exe", "wininit.exe", "csrss.exe", "services.exe", "lsass.exe"
}

def es_app_valida(nombre: str) -> bool:
    if not nombre:
        return False
    n = nombre.lower()
    if n in PROCESOS_PROHIBIDOS:
        return False
    if n.endswith(".exe") and len(n) > 3:
        return True
    return False

class SkillProcess:
    intents = ["list_processes", "kill_process", "top_memory_process", "top_cpu_process"]

    def __init__(self, say):
        self.say = say

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "list_processes":
            procesos = []
            for p in psutil.process_iter(['name']):
                nombre = p.info['name']
                if es_app_valida(nombre):
                    procesos.append(nombre)
            # Eliminar duplicados
            procesos = list(dict.fromkeys(procesos))
            visibles = procesos[:10]
            if visibles:
                self.say("Algunas aplicaciones abiertas son: " + ", ".join(visibles))
            else:
                self.say("No encontré aplicaciones de usuario abiertas")
            return True

        if intent == "kill_process":
            q = (entities.get("q") or "").strip().lower()
            if not q:
                self.say("Decime qué aplicación querés cerrar")
                return True

            cerrado = False
            for proc in psutil.process_iter(['pid', 'name']):
                name = (proc.info['name'] or "").lower()
                if q in name and name not in PROCESOS_PROHIBIDOS:
                    try:
                        proc.terminate()
                        proc.wait(timeout=2)
                        if proc.is_running():
                            proc.kill()
                        if not proc.is_running():
                            cerrado = True
                    except Exception:
                        pass

            if cerrado:
                self.say(f"Cerré la aplicación {q}")
            else:
                self.say(f"No encontré o no pude cerrar la aplicación {q}")
            return True

        if intent == "top_memory_process":
            try:
                procesos = [
                    p for p in psutil.process_iter(['name', 'memory_info'])
                    if es_app_valida(p.info['name'])
                ]
                if not procesos:
                    self.say("No encontré procesos de usuario activos")
                    return True

                # Ordenar por RAM usada
                top = max(procesos, key=lambda p: p.info['memory_info'].rss)
                nombre = top.info['name']
                memoria_mb = round(top.info['memory_info'].rss / (1024 ** 2), 1)
                self.say(f"La aplicación que más memoria consume es {nombre}, usando {memoria_mb} megas de RAM")
            except Exception:
                self.say("No pude obtener la información de memoria")
            return True

        if intent == "top_cpu_process":
            try:
                # Para CPU conviene pedir cpu_percent de todos los procesos
                procesos = [
                    p for p in psutil.process_iter(['name'])
                    if es_app_valida(p.info['name'])
                ]
                if not procesos:
                    self.say("No encontré procesos de usuario activos")
                    return True

                # Primera pasada para inicializar mediciones
                for p in procesos:
                    try:
                        p.cpu_percent(interval=None)
                    except Exception:
                        pass

                # Esperar 1 segundo y medir otra vez
                psutil.cpu_percent(interval=1)

                max_proc = None
                max_cpu = 0.0
                for p in procesos:
                    try:
                        uso = p.cpu_percent(interval=None)
                        if uso > max_cpu:
                            max_cpu = uso
                            max_proc = p
                    except Exception:
                        pass

                if max_proc:
                    self.say(
                        f"La aplicación que más CPU consume es {max_proc.info['name']}, usando {max_cpu:.1f} por ciento de CPU")
                else:
                    self.say("No pude calcular el consumo de CPU")
            except Exception:
                self.say("No pude obtener la información de CPU")
            return True

        return False

