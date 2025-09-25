# NLU por palabras clave/regex  NLU --> Natural Languaje Understanding
import re #módulo de expresiones regulares de Python. Sirve para buscar patrones de texto en strings.
from typing import Dict, Any

# Patrones básicos
_re_open_youtube = re.compile(r"\babrir\s+youtube\b|\babrí\s+youtube\b", re.I)
_re_open_browser = re.compile(r"\babrir\s+el?\s*navegador\b|\babrí\s+el?\s*navegador\b|\babrir\s+navegador\b", re.I)
_re_wiki = re.compile(r"\bbusca?r?\s+en\s+wikipedia\b", re.I)
_re_web = re.compile(r"\bbusca?r?\s+en\s+internet\b", re.I)
_re_play = re.compile(r"\breproducir\b", re.I)
_re_joke = re.compile(r"\bchiste\b", re.I)
_re_cpu = re.compile(r"\buso\s+de\s+cpu\b", re.I)
_re_mem = re.compile(r"\buso\s+de\s+memoria\b", re.I)
_re_batt = re.compile(r"\bbatería\b|\bnivel\s+de\s+batería\b", re.I)
_re_list_proc = re.compile(r"\b(procesos|aplicaciones|programas)\s+(abiertos|corriendo|ejecutando)\b", re.I)
_re_kill_proc = re.compile(r"\b(cerrar|matar|terminar)\s+(proceso|aplicaci[oó]n|programa)\b", re.I)
_re_top_mem = re.compile(r"\b(proceso|aplicaci[oó]n)\s+(que\s+m[aá]s\s+memoria|consumo\s+de\s+memoria)\b", re.I)
_re_top_cpu = re.compile(r"\b(proceso|aplicaci[oó]n)\s+(que\s+m[aá]s\s+cpu|consumo\s+de\s+cpu)\b", re.I)
_re_temp = re.compile(r"\btemperatura\b.*\b(cpu|gpu)\b|\btemperaturas?\b", re.I)
_re_uptime = re.compile(r"\b(tiempo\s+de\s+(uso|encendida|encendido)|uptime|último\s+arranque)\b", re.I)
_re_list_disks = re.compile(r"\b(discos|particiones)\b(gigas|gigabytes|espacio\s+libre|libres|almacenamiento|tamaño\s+del\s+disco)\buso\s+de\s+disco\b|\bdisco\b", re.I)
_re_net_usage = re.compile(r"\b(consumo\s+de\s+red|datos\s+(enviados|recibidos)|uso\s+de\s+red)\b", re.I) # Consumo de red
_re_net_if = re.compile(r"\b(interfaz|interfaces|ip|direcci[oó]n\s+ip)\b", re.I) # Interfaces e IP
_re_mem_avg = re.compile(r"\b(promedio|media)\b.*\b(ram|memoria)\b.*(hora)", re.I) # Promedio RAM última hora
_re_cpu_avg = re.compile(r"\b(promedio|media)\b.*\b(cpu|procesador)\b.*(hora)", re.I) # Promedio CPU última hora
_re_cpu_peak = re.compile(r"\b(m[aá]ximo|mayor|pico)\b.*\bcpu\b.*(hoy|d[ií]a)", re.I) # Pico CPU del día
_re_mem_peak = re.compile(r"\b(m[aá]ximo|mayor|pico)\b.*\b(ram|memoria)\b.*(hoy|d[ií]a)", re.I) # Pico RAM del día
_re_cpu_at_time = re.compile(r"\bcpu\b.*a\s+las\s+(\d{1,2}:\d{2})", re.I) # CPU en un momento específico
_re_mem_at_time = re.compile(r"\b(ram|memoria)\b.*a\s+las\s+(\d{1,2}:\d{2})", re.I) # RAM en un momento específico
_re_note = re.compile(r"\b(crea?r?\s+nota|guardar?\s+nota|escribir?\s+nota)\b", re.I) #Crear notas
_re_open_app = re.compile(r"\babrir\s+(.+)", re.I) #abrir apps conocidas

_re_bye = re.compile(r"\badiós\b|\bchau\b|\bhasta luego\b|\bsalir\b", re.I)

class SimpleNLU:
    def parse(self, text: str) -> Dict[str, Any]:
        t = (text or "").strip()
        if not t:
            return {"intent": "__none__", "entities": {}}

        if _re_open_youtube.search(t):
            return {"intent": "open_youtube", "entities": {}}
        if _re_open_browser.search(t):
            return {"intent": "open_browser", "entities": {}}
        if _re_wiki.search(t):
            q = re.sub(_re_wiki, "", t, count=1).strip()
            return {"intent": "wiki_search", "entities": {"q": q}}
        if _re_web.search(t):
            q = re.sub(_re_web, "", t, count=1).strip()
            return {"intent": "web_search", "entities": {"q": q}}
        if _re_play.search(t):
            q = re.sub(_re_play, "", t, count=1).strip()
            return {"intent": "play_youtube", "entities": {"q": q}}
        if _re_joke.search(t):
            return {"intent": "tell_joke", "entities": {}}
        if _re_batt.search(t):
            return {"intent": "battery_status", "entities": {}}
        if _re_list_proc.search(t):
            return {"intent": "list_processes", "entities": {}}
        if _re_kill_proc.search(t):
            q = re.sub(_re_kill_proc, "", t, count=1).strip()
            return {"intent": "kill_process", "entities": {"q": q}}
        if _re_top_mem.search(t):
            return {"intent": "top_memory_process", "entities": {}}
        if _re_top_cpu.search(t):
            return {"intent": "top_cpu_process", "entities": {}}
        if _re_temp.search(t):
            return {"intent": "temperature_status", "entities": {}}
        if _re_uptime.search(t):
            return {"intent": "uptime", "entities": {}}
        if _re_list_disks.search(t):
            return {"intent": "list_disks", "entities": {}}
        if _re_net_usage.search(t):
            return {"intent": "network_usage", "entities": {}}
        if _re_net_if.search(t):
            return {"intent": "network_interfaces", "entities": {}}
        if _re_mem_avg.search(t):
            return {"intent": "mem_average_last_hour", "entities": {}}
        if _re_cpu_avg.search(t):
            return {"intent": "cpu_average_last_hour", "entities": {}}
        if _re_cpu_peak.search(t):
            return {"intent": "cpu_peak_day", "entities": {}}
        if _re_mem_peak.search(t):
            return {"intent": "mem_peak_day", "entities": {}}
        m = _re_cpu_at_time.search(t)
        if m:
            return {"intent": "cpu_at_time", "entities": {"time": m.group(1)}}
        m = _re_mem_at_time.search(t)
        if m:
            return {"intent": "mem_at_time", "entities": {"time": m.group(1)}}
        if _re_cpu.search(t):
            return {"intent": "cpu_usage", "entities": {}}
        if _re_mem.search(t):
            return {"intent": "memory_usage", "entities": {}}
        if _re_note.search(t):
            q = re.sub(_re_note, "", t, count=1).strip()
            return {"intent": "create_note", "entities": {"content": q}}
        if _re_open_app.search(t):
            app = _re_open_app.search(t).group(1).strip()
            return {"intent": "open_app", "entities": {"app": app}}

        if _re_bye.search(t):
            return {"intent": "goodbye", "entities": {}}


        return {"intent": "__fallback__", "entities": {"raw": t}}