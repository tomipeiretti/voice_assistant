import psutil

class SkillNetwork:
    intents = [
        "network_usage",     # Consumo de red (bytes enviados/recibidos)
        "network_interfaces" # Interfaces activas e IPs
    ]

    def __init__(self, say):
        self.say = say

    def handle(self, intent: str, entities: dict) -> bool:
        if intent == "network_usage":
            try:
                net = psutil.net_io_counters()
                enviados = round(net.bytes_sent / (1024**2), 1)   # MB
                recibidos = round(net.bytes_recv / (1024**2), 1)
                self.say(f"Desde el arranque enviaste {enviados} megas y recibiste {recibidos} megas de datos")
            except Exception as e:
                print("Error de red:", e)
                self.say("No pude obtener la información de consumo de red")
            return True

        if intent == "network_interfaces":
            try:
                addrs = psutil.net_if_addrs()
                stats = psutil.net_if_stats()
                for nombre, st in stats.items():
                    if st.isup:
                        ip_list = []
                        for addr in addrs.get(nombre, []):
                            # IPv4
                            if hasattr(addr.family, "name") and addr.family.name == "AF_INET":
                                ip_list.append(addr.address)
                        if ip_list:
                            self.say(f"La interfaz {nombre} está activa con dirección IP {', '.join(ip_list)}")
                        else:
                            self.say(f"La interfaz {nombre} está activa pero sin IP asignada")
            except Exception as e:
                print("Error interfaces:", e)
                self.say("No pude obtener la información de interfaces")
            return True

        return False
