# Asistente de Voz en Python 🎙️🤖

Este proyecto es un **asistente de voz en Python** que permite interactuar con el sistema operativo y obtener información a través de comandos hablados.


## 📂 Arquitectura del Proyecto

voice_assistant/
├── main.py # Punto de entrada del asistente
├── core/
│ ├── nlu.py # Motor NLU (intents y entities vía regex)
│ ├── router.py # Router: despacha intents a las skills
├── adapters/
│ ├── asr.py # ASR (voz → texto) con SpeechRecognition
│ ├── tts.py # TTS simple con pyttsx3
├── skills/
│ ├── skill_web.py # Búsquedas en web, Wikipedia, YouTube
│ ├── skill_fun.py # Funciones lúdicas (contar chistes)
│ ├── skill_system.py # Información del sistema (CPU, RAM, batería, discos)
│ ├── skill_process.py # Listar / terminar procesos
│ ├── skill_network.py # Estado de red, IPs, interfaces
│ ├── skill_metrics_logger.py # Logger y análisis histórico de CPU/RAM
│ │── skill_apps.py # Aperturas de apps configurables
│ │── skill_notes.py # Generar notas dictadas
│ │── skill_calc.py # Calculadora por voz
├─ requirements.txt # Dependencias del proyecto

---

## ⚡ Funcionalidades

### 🛠️ Skills disponibles

#### 🌐 SkillWeb
- Buscar en Wikipedia.
- Buscar en Internet.
- Abrir YouTube y reproducir videos.
- Abrir el navegador

#### 🎉 SkillFun
- Contar chistes.

#### 💻 SkillSystem
- Consultar uso de CPU y RAM en tiempo real.
- Estado de la batería.
- Temperatura de CPU/GPU (si el sistema lo soporta).
- Tiempo de encendido (*uptime*).
- Listado de discos y espacio libre.

#### ⚙️ SkillProcess
- Listar procesos abiertos.
- Cerrar/matar procesos específicos.
- Mostrar proceso que más consume CPU o RAM.

#### 🌐 SkillNetwork
- Mostrar interfaces de red y dirección IP.
- Medir consumo de red (enviados / recibidos).

#### 📊 SkillMetricsLogger
- Guarda cada minuto CPU y RAM en `metrics_log.csv`.
- Consulta histórico:
  - Promedio CPU/RAM última hora.
  - Consumo CPU/RAM en una hora específica.
  - Pico CPU/RAM en el día (en desarrollo).
- **Alertas automáticas**:
  - Si CPU o RAM llegan al 99%, avisa con voz.

#### 📂 SkillApps
- Abrir aplicaciones instaladas en el sistema.
- Configuración mediante variables de entorno (`.env`).
- Si la aplicación está configurada con ruta absoluta, la abre directamente.
- Si la aplicación está configurada por nombre, la abre usando el `PATH` del sistema.

#### 📝 SkillNotes
- Crear notas rápidas dictadas por voz o a partir de texto reconocido.

#### ➗ SkillCalc
- Resolver cálculos matemáticos dictados en lenguaje natural.
- Soporta operaciones básicas:
  - Suma, resta, multiplicación, división.
  - Potencias y raices.