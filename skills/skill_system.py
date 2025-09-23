import psutil

class SkillSystem:
    intents = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "disk_space"
        "battery_status",
        "temperature_status",
    ]

    def __init__(self, say):
        self.say = say

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "cpu_usage":
            usage = psutil.cpu_percent(interval=1)
            self.say(f"El uso de CPU es de {usage} por ciento")
            return True

        if intent == "memory_usage":
            mem = psutil.virtual_memory()
            self.say(f"El uso de memoria es de {mem.percent} por ciento")
            return True

        if intent == "disk_usage":
            disk = psutil.disk_usage('/')
            self.say(f"El uso de disco es de {disk.percent} por ciento")
            return True

        if intent == "disk_space":
            disk = psutil.disk_usage('/')
            total = round(disk.total / (1024 ** 3), 1)  # GB con 1 decimal
            used = round(disk.used / (1024 ** 3), 1)
            free = round(disk.free / (1024 ** 3), 1)
            self.say(f"El disco tiene {total} gigas en total. Usaste {used} y te quedan {free} libres.")
            return True

        if intent == "battery_status":
            batt = psutil.sensors_battery()
            if batt:
                plugged = "conectada" if batt.power_plugged else "desconectada"
                self.say(f"La batería está al {batt.percent} por ciento y está {plugged}")
            else:
                self.say("No pude obtener información de la batería")
            return True

        if intent == "temperature_status":
            try:
                temps = psutil.sensors_temperatures()
            except AttributeError:
                self.say("Este sistema no soporta lectura de temperaturas con psutil")
                return True
            if not temps:
                self.say("No pude obtener la temperatura del sistema en este equipo")
                return True
            # CPU
            cpu_temps = temps.get("coretemp") or temps.get("cpu-thermal") or []
            if cpu_temps:
                cpu_avg = sum([t.current for t in cpu_temps]) / len(cpu_temps)
                self.say(f"La temperatura promedio de la CPU es {cpu_avg:.1f} grados")
            else:
                self.say("No encontré sensores de CPU")
            # GPU
            gpu_temps = temps.get("amdgpu") or temps.get("gpu") or temps.get("nvidia") or []
            if gpu_temps:
                gpu_avg = sum([t.current for t in gpu_temps]) / len(gpu_temps)
                self.say(f"La temperatura de la GPU es {gpu_avg:.1f} grados")
            else:
                self.say("No encontré sensores de GPU")
            return True

        return False
