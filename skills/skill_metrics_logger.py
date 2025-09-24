import psutil
import csv
import datetime
import threading
import time
import os

LOG_FILE = "metrics_log.csv"

class SkillMetricsLogger:
    intents = [
        "cpu_average_last_hour",
        "mem_average_last_hour",
        "cpu_at_time",
        "mem_at_time",
        "cpu_peak_day",
        "mem_peak_day",
    ]

    def __init__(self, say):
        self.say = say
        # Crear log si no existe
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "cpu_percent", "mem_percent"])
        # Iniciar thread logger
        t = threading.Thread(target=self._logger_loop, daemon=True)
        t.start()

    def _logger_loop(self):
        """Guarda CPU y RAM cada minuto"""
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([ts, cpu, mem])

            #Alertas
            try:
                self._check_alerts(cpu, mem)
            except Exception as e:
                print("[ERROR ALERT]", e)

            time.sleep(60)


    def _check_alerts(self, cpu, mem):
        """Verifica si CPU o RAM llegaron a niveles críticos"""

        if mem >= 99:
            self.say(" Alerta: La memoria RAM está al 99 por ciento.")

        if cpu >= 99:
            self.say(" Alerta: El procesador está al 99 por ciento. ")

    # --- Promedio CPU última hora ---
    def _get_cpu_avg_last_hour(self):
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(hours=1)
        values = []

        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts >= cutoff:
                    values.append(float(row[1]))

        if values:
            avg = sum(values) / len(values)
            return round(avg, 1), len(values)
        return None, 0

    # --- Promedio RAM última hora ---
    def _get_mem_avg_last_hour(self):
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(hours=1)
        values = []

        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts >= cutoff:
                    values.append(float(row[2]))

        if values:
            avg = sum(values) / len(values)
            return round(avg, 1), len(values)
        return None, 0

    # --- CPU en un momento específico ---
    def _get_cpu_at_time(self, target_time: datetime.datetime):
        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts.replace(second=0, microsecond=0) == target_time.replace(second=0, microsecond=0):
                    return float(row[1])
        return None

    # --- RAM en un momento específico ---
    def _get_mem_at_time(self, target_time: datetime.datetime):
        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts.replace(second=0, microsecond=0) == target_time.replace(second=0, microsecond=0):
                    return float(row[2])
        return None


    # --- Pico CPU en el día ---
    def _get_cpu_peak_day(self):
        today = datetime.date.today()
        max_val = -1
        max_time = None
        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts.date() == today:
                    val = float(row[1])
                    if val > max_val:
                        max_val = val
                        max_time = ts
        return max_val, max_time

    # --- Pico RAM en el día ---
    def _get_mem_peak_day(self):
        today = datetime.date.today()
        max_val = -1
        max_time = None
        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if ts.date() == today:
                    val = float(row[2])
                    if val > max_val:
                        max_val = val
                        max_time = ts
        return max_val, max_time

    # --- Router interno ---
    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "cpu_average_last_hour":
            avg, count = self._get_cpu_avg_last_hour()
            if avg is not None:
                if count < 60:
                    self.say(f"Solo tengo datos de {count} minutos. El promedio de CPU fue {avg}%")
                else:
                    self.say(f"Tu CPU estuvo en promedio al {avg}% en la última hora")
            else:
                self.say("Todavía no tengo datos suficientes")
            return True

        if intent == "mem_average_last_hour":
            avg, count = self._get_mem_avg_last_hour()
            if avg is not None:
                if count < 60:
                    self.say(f"Solo tengo datos de {count} minutos. El promedio de RAM fue {avg}%")
                else:
                    self.say(f"Tu RAM estuvo en promedio al {avg}% en la última hora")
            else:
                self.say("Todavía no tengo datos suficientes")
            return True

        if intent == "cpu_at_time":
            q = entities.get("time")
            try:
                target_time = datetime.datetime.strptime(q, "%H:%M").replace(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day
                )
                val = self._get_cpu_at_time(target_time)
                if val is not None:
                    self.say(f"A las {q} el CPU estaba en {val}%")
                else:
                    self.say(f"No encontré datos de CPU para las {q}")
            except Exception:
                self.say("No entendí la hora que me pediste")
            return True

        if intent == "mem_at_time":
            q = entities.get("time")
            try:
                target_time = datetime.datetime.strptime(q, "%H:%M").replace(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day
                )
                val = self._get_mem_at_time(target_time)
                if val is not None:
                    self.say(f"A las {q} la RAM estaba en {val}%")
                else:
                    self.say(f"No encontré datos de RAM para las {q}")
            except Exception:
                self.say("No entendí la hora que me pediste")
            return True


        if intent == "cpu_peak_day":
            val, ts = self._get_cpu_peak_day()
            if ts:
                hora = ts.strftime("%H:%M")
                self.say(f"Hoy el mayor consumo de CPU fue {val}% a las {hora}")
            else:
                self.say("No tengo datos de CPU para hoy")
            return True

        if intent == "mem_peak_day":
            val, ts = self._get_mem_peak_day()
            if ts:
                hora = ts.strftime("%H:%M")
                self.say(f"Hoy el mayor consumo de RAM fue {val}% a las {hora}")
            else:
                self.say("No tengo datos de RAM para hoy")
            return True

        return False
