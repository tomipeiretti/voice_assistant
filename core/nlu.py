# NLU simple por palabras clave/regex  NLU --> Natural Languaje Understanding
import re
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
_re_disk_space = re.compile(r"\b(gigas?|gigabytes|espacio\s+libre|libres|almacenamiento|tamaño\s+del\s+disco)\b", re.I)
_re_disk = re.compile(r"\buso\s+de\s+disco\b|\bdisco\b", re.I)
_re_batt = re.compile(r"\bbatería\b|\bnivel\s+de\s+batería\b", re.I)
_re_list_proc = re.compile(r"\b(procesos|aplicaciones|programas)\s+(abiertos|corriendo|ejecutando)\b", re.I)
_re_kill_proc = re.compile(r"\b(cerrar|matar|terminar)\s+(proceso|aplicaci[oó]n|programa)\b", re.I)
_re_top_mem = re.compile(r"\b(proceso|aplicaci[oó]n)\s+(que\s+m[aá]s\s+memoria|consumo\s+de\s+memoria)\b", re.I)
_re_top_cpu = re.compile(r"\b(proceso|aplicaci[oó]n)\s+(que\s+m[aá]s\s+cpu|consumo\s+de\s+cpu)\b", re.I)
_re_temp = re.compile(r"\btemperatura\b.*\b(cpu|gpu)\b|\btemperaturas?\b", re.I)

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
        if _re_cpu.search(t):
            return {"intent": "cpu_usage", "entities": {}}
        if _re_mem.search(t):
            return {"intent": "memory_usage", "entities": {}}
        if _re_disk_space.search(t):
            return {"intent": "disk_space", "entities": {}}
        if _re_disk.search(t):
            return {"intent": "disk_usage", "entities": {}}
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

        if _re_bye.search(t):
            return {"intent": "goodbye", "entities": {}}

        return {"intent": "__fallback__", "entities": {"raw": t}}