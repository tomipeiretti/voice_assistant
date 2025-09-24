import psutil
import datetime

class SkillSystem:
    intents = [
        "cpu_usage",
        "memory_usage",
        "battery_status",
        "temperature_status",
        "uptime",
        "list_disks",
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

        if intent == "uptime":
            boot_ts = psutil.boot_time()
            boot_time = datetime.datetime.fromtimestamp(boot_ts)
            time = datetime.datetime.now() - boot_time

            hours, resto = divmod(time.total_seconds(), 3600)
            minutes, _ = divmod(resto, 60)

            hours = int(hours)
            minutes = int(minutes)

            if hours > 0:
                self.say(f"La computadora está encendida hace {hours} horas y {minutes} minutos")
            else:
                self.say(f"La computadora está encendida hace {minutes} minutos")
            return True

        if intent == "list_disks":
            try:
                parts = psutil.disk_partitions(all=False)
                if not parts:
                    self.say("No encontré discos o particiones disponibles")
                    return True
                mensajes = []
                for p in parts:
                    try:
                        uso = psutil.disk_usage(p.mountpoint)
                        total = round(uso.total / (1024 ** 3), 1)
                        usado = round(uso.used / (1024 ** 3), 1)
                        libre = round(uso.free / (1024 ** 3), 1)
                        mensajes.append(
                            f"En {p.device} hay {total} gigas en total, usaste {usado} y quedan {libre} libres"
                        )
                    except PermissionError:
                        # Algunas particiones del sistema no permiten consultar
                        continue
                if mensajes:
                    for m in mensajes:
                        self.say(m)
                else:
                    self.say("No pude obtener información de los discos")
            except Exception:
                self.say("Ocurrió un error al consultar los discos")
            return True

        return False
