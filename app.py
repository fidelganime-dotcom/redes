import streamlit as st
import random
import time
import os
import tempfile
import re
import ipaddress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
from groq import Groq
from gtts import gTTS
import speech_recognition as sr

# ---------- CONFIGURACIÓN STREAMLIT ----------
st.set_page_config(
    page_title="REDES BÁSICAS - TECNO KIDS", 
    page_icon="🌐", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CLIENTE GROQ (con tu nueva API key) ----------
client = Groq(api_key="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")

# ==================== CSS PREMIUM (igual que antes) ====================
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap');

:root {
    --primary: #3b82f6;
    --primary-light: #60a5fa;
    --primary-dark: #2563eb;
    --secondary: #8b5cf6;
    --secondary-light: #a78bfa;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --dark: #0f172a;
    --dark-light: #1e293b;
    --gray: #64748b;
    --gray-light: #94a3b8;
    --white: #f8fafc;
    
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    --hover-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}

.glass-card, .metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    border: 1px solid var(--glass-border);
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    animation: fadeInUp 0.6s ease-out;
}

.glass-card {
    padding: 24px;
    margin: 16px 0;
    box-shadow: var(--glass-shadow);
}

.glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: var(--hover-shadow);
}

.metric-card {
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}

.metric-card:hover::before {
    transform: scaleX(1);
}

.metric-card h3 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gray-light);
    margin-bottom: 12px;
}

.metric-card h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.metric-card p {
    font-size: 0.8rem;
    color: var(--gray-light);
}

.premium-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    animation: fadeInDown 0.8s ease-out;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 32px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(59, 130, 246, 0.3);
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    border: none !important;
    border-radius: 40px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    color: white !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
}

[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    color: var(--white) !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 10px !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(30, 41, 59, 0.5);
    border-radius: 60px;
    padding: 6px 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 40px;
    padding: 8px 24px;
    font-weight: 600;
    color: #cbd5e1;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
}

.info-box {
    background: rgba(59, 130, 246, 0.08);
    border-radius: 20px;
    padding: 20px;
    margin: 16px 0;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.4);
    border-radius: 10px;
}

.area-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.1);
}
.area-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.1);
    border-color: var(--primary);
}
.area-icon { font-size: 2.5rem; }
.area-name { font-weight: 600; color: #f1f5f9; margin-top: 8px; }

.component-card {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 12px 16px;
    margin: 8px;
    border-left: 3px solid var(--primary);
    transition: all 0.3s ease;
}
.component-card:hover {
    transform: translateX(5px);
    background: rgba(255,255,255,0.08);
}

.latency-container {
    background: rgba(0,0,0,0.3);
    border-radius: 16px;
    padding: 15px;
    margin: 10px 0;
}

.question-box {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.85), rgba(37, 99, 235, 0.85));
    border-radius: 28px;
    padding: 1.8rem;
    margin: 1rem 0;
}
.question-text {
    font-size: 1.3rem;
    font-weight: 700;
    color: #FEF08A;
    background: rgba(0,0,0,0.3);
    padding: 1rem;
    border-radius: 20px;
}
.feedback-correcto {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80;
    padding: 1rem;
    border-radius: 16px;
    border-left: 4px solid #22c55e;
}
.feedback-incorrecto {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    padding: 1rem;
    border-radius: 16px;
    border-left: 4px solid #ef4444;
}
.medalla {
    font-size: 1.3rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.2));
    padding: 12px;
    border-radius: 60px;
    margin: 10px 0;
}
.puntaje {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    padding: 8px 20px;
    border-radius: 60px;
    font-weight: bold;
    font-size: 1.5rem;
    color: white;
    display: inline-block;
}
.mascota-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999;
    cursor: pointer;
    animation: bounce 2s infinite;
}
.mascota-container:hover { transform: scale(1.1); }
.mascota-speech {
    position: absolute;
    bottom: 70px;
    right: 10px;
    background: white;
    color: #1e293b;
    padding: 10px 18px;
    border-radius: 20px 20px 5px 20px;
    font-weight: 500;
    font-size: 0.8rem;
    white-space: nowrap;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    animation: fadeInOut 4s infinite;
}
@keyframes fadeInOut {
    0%,100% { opacity: 0; transform: scale(0.9); }
    10%,90% { opacity: 1; transform: scale(1); }
}
.watermark {
    position: fixed;
    bottom: 15px;
    left: 15px;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(10px);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.7rem;
    color: #94a3b8;
    z-index: 999;
}
@media (max-width: 768px) {
    .premium-title { font-size: 1.8rem; }
    .section-title { font-size: 1.2rem; }
    .question-text { font-size: 1rem; }
}
</style>
<div class="watermark">🌐 REDES BÁSICAS</div>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# ==================== FUNCIONES DE VOZ (Cloud-friendly) ====================
def text_to_speech(text, lang="es"):
    """Genera archivo de audio MP3 a partir del texto y devuelve bytes para reproducir con st.audio"""
    if not text.strip():
        return None
    try:
        tts = gTTS(text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp_path)
        return audio_bytes
    except Exception as e:
        st.error(f"Error generando audio: {e}")
        return None

def speak(text, voice_type=None, speed=None):
    """Reproduce audio en la interfaz usando st.audio (no bloqueante). 
       voice_type y speed se ignoran para simplicidad en la nube."""
    audio_bytes = text_to_speech(text)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")

# ==================== BASE DE CONOCIMIENTO ====================
knowledge = {
    "¿qué es una red?": "Una red de computadoras es un conjunto de dispositivos conectados que comparten recursos e información. Permite la comunicación entre equipos y el acceso a datos de forma remota.",
    "¿para qué sirve una red?": "Sirve para compartir datos, impresoras, internet, comunicarse entre dispositivos, realizar videollamadas, enviar correos, jugar en línea y acceder a información desde cualquier lugar.",
    "diferencias entre lan y wan": "LAN es red local (corto alcance, alta velocidad, baja latencia, propiedad privada). WAN es red amplia (Internet, conexiones entre ciudades, mayor latencia, operada por empresas de telecomunicaciones).",
    "¿qué es el modelo osi?": "Modelo de 7 capas que estandariza la comunicación: Física (cables), Enlace (MAC), Red (IP), Transporte (TCP/UDP), Sesión, Presentación, Aplicación. Creado por ISO en 1984.",
    "capas del modelo osi": "1️⃣ Física, 2️⃣ Enlace de Datos, 3️⃣ Red, 4️⃣ Transporte, 5️⃣ Sesión, 6️⃣ Presentación, 7️⃣ Aplicación.",
    "¿qué hace la capa de red?": "La capa de red (capa 3) se encarga del direccionamiento IP, el enrutamiento de paquetes entre redes diferentes, y la fragmentación de datos cuando es necesario.",
    "¿qué es una dirección ipv4?": "Es un número único de 32 bits que identifica cada dispositivo en una red IP. Se escribe como 4 números decimales entre 0 y 255 separados por puntos. Ejemplo: 192.168.1.1",
    "¿qué es una máscara de subred?": "Indica qué parte de la IP es red y qué parte es host. Ejemplo: 255.255.255.0 significa que los primeros 24 bits son red y los últimos 8 son para hosts.",
    "¿qué es subneteo?": "Subneteo es dividir una red grande en redes más pequeñas llamadas subredes. Esto mejora la administración, reduce broadcasts y aumenta la seguridad y el rendimiento.",
    "¿qué es un router?": "Dispositivo de capa 3 que conecta redes diferentes y envía paquetes IP entre ellas usando tablas de enrutamiento. También hace NAT y firewall básico.",
    "¿qué es un switch?": "Dispositivo de capa 2 que conecta dispositivos dentro de una misma red usando direcciones MAC. Es inteligente: envía datos solo al puerto del destinatario.",
    "comandos cisco básicos": "enable (modo privilegiado), configure terminal (configuración), interface (configurar puerto), ip address (asignar IP), no shutdown (activar), show ip interface brief (ver estado).",
    "tipos de cables de red": "UTP (cable de par trenzado sin blindaje) el más común, STP (blindado), fibra óptica (largas distancias, alta velocidad), coaxial (antiguo, ahora en cablemódem).",
    "¿qué es un gateway?": "Puerta de enlace, dispositivo que permite a una red local comunicarse con redes externas. Normalmente es un router con IP como 192.168.1.1 o 192.168.0.1.",
    "¿qué es arp?": "Protocolo de resolución de direcciones que traduce direcciones IP a direcciones MAC dentro de una red local. Funciona con broadcasts.",
    "¿qué es icmp?": "Protocolo usado para mensajes de error y diagnóstico. El comando ping usa ICMP Echo Request y Echo Reply. Traceroute también lo usa.",
    "tcp vs udp": "TCP es orientado a conexión, confiable, ordena paquetes, tiene control de flujo. UDP es más rápido, sin conexión, no garantiza entrega. Ideal para streaming y juegos.",
    "seguridad en router": "Cambiar contraseñas por defecto, usar WPA2/WPA3, desactivar WPS, actualizar firmware, deshabilitar administración remota, activar firewall.",
    "¿qué es dhcp?": "Protocolo que asigna automáticamente direcciones IP a los dispositivos de una red. Usa DORA: Discover, Offer, Request, Acknowledge.",
    "¿qué es vlan?": "Red virtual que separa el tráfico en capa 2, mejorando seguridad y reduciendo broadcasts. Permite tener múltiples redes lógicas en un mismo switch físico.",
    "¿qué es nat?": "Network Address Translation: traduce IPs privadas a una o varias públicas. Permite que dispositivos con IPs privadas accedan a Internet.",
}
preguntas_db = list(knowledge.keys())
respuestas_db = list(knowledge.values())
vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2))
preguntas_tfidf = vectorizer.fit_transform(preguntas_db)

def buscar_respuesta_semantica(user_input):
    texto = user_input.lower().strip()
    texto = re.sub(r'[¿?¡!]', '', texto)
    user_vec = vectorizer.transform([texto])
    sim = cosine_similarity(user_vec, preguntas_tfidf).flatten()
    best = np.argmax(sim)
    conf = sim[best]
    if conf > 0.25:
        return respuestas_db[best], conf
    return None, conf

# ==================== PREGUNTAS PARA QUIZ ====================
areas_quiz = {
    "Conceptos básicos de redes": [],
    "Modelo OSI": [],
    "Direccionamiento IPv4": [],
    "Subneteo y máscaras": [],
    "Dispositivos y comandos": [],
    "Cables y conexiones": [],
    "Inteligencia Artificial Claude AI": [],
    "Seguridad, DHCP, VLAN, NAT": [],
}

def generar_preguntas():
    cb = [
        ("¿Qué es una red de computadoras?", ["Conjunto de dispositivos conectados", "Una sola computadora", "Un programa", "Un cable"], "Conjunto de dispositivos conectados"),
        ("¿Qué significa LAN?", ["Local Area Network", "Large Area Network", "Logical Area Network", "Long Area Network"], "Local Area Network"),
        ("¿Qué significa WAN?", ["Wide Area Network", "Wireless Area Network", "Wired Area Network", "Web Area Network"], "Wide Area Network"),
        ("¿Qué dispositivo conecta una LAN a Internet?", ["Router", "Switch", "Hub", "Repetidor"], "Router"),
        ("¿Qué topología usa un switch central?", ["Estrella", "Bus", "Anillo", "Malla"], "Estrella"),
        ("¿Qué es un servidor?", ["Dispositivo que ofrece servicios", "Un cable", "Un conector", "Un protocolo"], "Dispositivo que ofrece servicios"),
        ("¿Qué es un cliente en redes?", ["Dispositivo que solicita servicios", "El cable principal", "El switch", "El router"], "Dispositivo que solicita servicios"),
        ("¿Cuál es la red más grande del mundo?", ["Internet", "Intranet", "Extranet", "LAN"], "Internet"),
        ("¿Qué es una topología de red?", ["Forma de conectar dispositivos", "Tipo de cable", "Velocidad", "Protocolo"], "Forma de conectar dispositivos"),
        ("¿Qué significa NIC?", ["Network Interface Card", "Network Internet Card", "New Interface Card", "Null Interface Card"], "Network Interface Card"),
    ]
    osi = [
        ("¿Cuántas capas tiene el modelo OSI?", ["7", "5", "4", "6"], "7"),
        ("¿Cuál es la capa 3 del modelo OSI?", ["Red", "Transporte", "Enlace", "Física"], "Red"),
        ("¿Qué capa se encarga del direccionamiento IP?", ["Red", "Transporte", "Aplicación", "Sesión"], "Red"),
        ("¿Qué capa usa direcciones MAC?", ["Enlace de Datos", "Red", "Física", "Transporte"], "Enlace de Datos"),
        ("¿Qué capa transmite bits?", ["Física", "Enlace", "Red", "Transporte"], "Física"),
        ("¿Qué capa asegura entrega confiable?", ["Transporte", "Red", "Sesión", "Presentación"], "Transporte"),
        ("¿Qué protocolo trabaja en capa de transporte?", ["TCP", "IP", "ARP", "HTTP"], "TCP"),
        ("¿Cuál es la PDU en capa de red?", ["Paquete", "Trama", "Segmento", "Bit"], "Paquete"),
        ("¿Qué capa hace enrutamiento?", ["Red", "Transporte", "Enlace", "Física"], "Red"),
    ]
    ipv4 = [
        ("¿Cuántos bits tiene IPv4?", ["32", "64", "128", "16"], "32"),
        ("¿Cuántos octetos tiene IPv4?", ["4", "3", "5", "6"], "4"),
        ("¿Rango de clase A?", ["1-126", "128-191", "192-223", "224-239"], "1-126"),
        ("¿Dirección de loopback?", ["127.0.0.1", "0.0.0.0", "255.255.255.255", "192.168.1.1"], "127.0.0.1"),
        ("¿Qué es IP privada?", ["No accesible desde Internet", "Accesible mundialmente", "Solo servidores", "IP de broadcast"], "No accesible desde Internet"),
        ("¿IP privada clase C?", ["192.168.x.x", "10.x.x.x", "172.16.x.x", "169.254.x.x"], "192.168.x.x"),
        ("¿Comando para ver IP en Windows?", ["ipconfig", "ifconfig", "netstat", "ping"], "ipconfig"),
        ("¿Hosts útiles en /24?", ["254", "256", "128", "512"], "254"),
        ("¿Máscara clase C por defecto?", ["255.255.255.0", "255.255.0.0", "255.0.0.0", "255.255.255.255"], "255.255.255.0"),
    ]
    subnet = [
        ("¿Máscara /24?", ["255.255.255.0", "255.255.0.0", "255.0.0.0", "255.255.255.128"], "255.255.255.0"),
        ("¿Bits de host en /26?", ["6", "8", "2", "4"], "6"),
        ("¿Hosts por subred en /28?", ["14", "16", "30", "62"], "14"),
        ("¿Máscara /30?", ["255.255.255.252", "255.255.255.248", "255.255.255.240", "255.255.255.224"], "255.255.255.252"),
        ("¿Para qué subnetear?", ["Optimizar direcciones", "Aumentar velocidad", "Reducir colisiones", "Conectar redes"], "Optimizar direcciones"),
        ("¿Hosts útiles en /29?", ["6", "8", "10", "14"], "6"),
    ]
    dispositivos = [
        ("¿Qué conecta redes diferentes?", ["Router", "Switch", "Hub", "Bridge"], "Router"),
        ("¿Qué usa direcciones MAC?", ["Switch", "Router", "Gateway", "Repetidor"], "Switch"),
        ("¿Comando modo privilegiado Cisco?", ["enable", "config t", "interface", "show"], "enable"),
        ("¿Comando ver tabla MAC?", ["show mac address-table", "show ip interface brief", "show running-config", "show vlan"], "show mac address-table"),
        ("¿Qué hace 'no shutdown'?", ["Activar interfaz", "Desactivar", "Borrar", "Reiniciar"], "Activar interfaz"),
        ("¿Guardar configuración Cisco?", ["copy running-config startup-config", "write memory", "save config", "write"], "copy running-config startup-config"),
        ("¿Capa del switch?", ["Capa 2", "Capa 1", "Capa 3", "Capa 4"], "Capa 2"),
        ("¿Capa del router?", ["Capa 3", "Capa 2", "Capa 4", "Capa 1"], "Capa 3"),
    ]
    cables = [
        ("¿Conector UTP común?", ["RJ45", "BNC", "LC", "USB"], "RJ45"),
        ("¿Distancia máxima UTP?", ["100 m", "50 m", "200 m", "500 m"], "100 m"),
        ("¿Cable para dos PCs directo?", ["Crossover", "Directo", "Rollover", "Fibra"], "Crossover"),
        ("¿Cable PC a switch?", ["Directo", "Crossover", "Rollover", "Fibra"], "Directo"),
        ("¿Categoría Gigabit?", ["Cat5e", "Cat5", "Cat3", "Cat4"], "Cat5e"),
        ("¿Ventaja fibra vs cobre?", ["Inmunidad EMI", "Menor costo", "Más fácil", "No conectores"], "Inmunidad EMI"),
        ("¿Qué significa UTP?", ["Unshielded Twisted Pair", "Universal TP", "Unidirectional TP", "Unshielded Transmission"], "Unshielded Twisted Pair"),
    ]
    claude = [
        ("¿Qué es Claude y cuál es su principal objetivo?", ["Asistente conversacional útil, honesto e inofensivo", "Motor de búsqueda", "Sistema operativo", "Antivirus"], "Asistente conversacional útil, honesto e inofensivo"),
        ("¿Por qué Claude es considerado confiable?", ["Entrenado con principios éticos e IA constitucional", "Acceso a todo internet", "Modelo único", "Reemplaza humanos"], "Entrenado con principios éticos e IA constitucional"),
        ("¿Qué tareas puede realizar Claude para estudiantes?", ["Explicar temas, resumir, ayudar con código", "Solo jugar", "Conducir autos", "Hacer tareas físicas"], "Explicar temas, resumir, ayudar con código"),
        ("¿Razón principal de creación de Anthropic?", ["Enfocarse en IA segura y ética", "Ganar dinero", "Copiar modelos", "Vender datos"], "Enfocarse en IA segura y ética"),
        ("¿Año de creación de Anthropic?", ["2021", "2018", "2020", "2022"], "2021"),
        ("La seguridad y ética son importantes en Claude. (V/F)", ["Verdadero", "Falso"], "Verdadero"),
        ("¿Cómo ha evolucionado Claude?", ["Mejor comprensión, contexto y razonamiento", "Sigue igual", "Ha empeorado", "Solo nombre"], "Mejor comprensión, contexto y razonamiento"),
        ("¿Mejora importante en programación?", ["Generar y depurar código", "Reemplazar programadores", "Solo Java", "No entiende código"], "Generar y depurar código"),
        ("Diferencia entre versiones?", ["Más rápida, precisa y mayor capacidad", "Solo nombre", "Más lenta", "Sin diferencias"], "Más rápida, precisa y mayor capacidad"),
        ("Cada nueva versión es más inteligente. (V/F)", ["Verdadero", "Falso"], "Verdadero"),
        ("Beneficio a estudiantes?", ["Ayuda a entender temas y resolver dudas", "Hace exámenes", "Respuestas literales", "No es útil"], "Ayuda a entender temas y resolver dudas"),
        ("Uso de docentes?", ["Apoyo para explicar y generar material", "Enseñar en su lugar", "Solo calificar", "No puede ayudar"], "Apoyo para explicar y generar material"),
        ("Ayuda a programadores?", ["Escribir código, encontrar errores", "Hackear", "Diseñar hardware", "Solo correos"], "Escribir código, encontrar errores"),
        ("¿Por qué usan empresas a Claude?", ["Automatizar tareas, atención al cliente", "Espiar empleados", "Es gratuito", "Eliminar puestos"], "Automatizar tareas, atención al cliente"),
        ("Funciones en análisis de info?", ["Resumir, extraer datos, responder preguntas", "Modificar archivos", "Borrar info", "Crear virus"], "Resumir, extraer datos, responder preguntas"),
        ("Influencia en transformación digital educativa?", ["Acceso a conocimiento personalizado", "Reemplazar escuelas", "Limitar aprendizaje", "Solo entretenimiento"], "Acceso a conocimiento personalizado"),
        ("Importancia de Claude en IA actual?", ["IA potente, útil y alineada con valores humanos", "Modelo único", "Sin competencia", "Código abierto"], "IA potente, útil y alineada con valores humanos"),
        ("Importancia del NLP en Claude?", ["Núcleo para entender y generar lenguaje", "No usa NLP", "Solo traducir", "Reconocer imágenes"], "Núcleo para entender y generar lenguaje"),
        ("Contribución al aprendizaje conversacional?", ["Diálogos fluidos adaptados al usuario", "Respuestas fijas", "Interrupciones", "Solo lectura"], "Diálogos fluidos adaptados al usuario"),
        ("¿Por qué usar IA éticamente?", ["Evitar sesgos, desinformación, impacto positivo", "Obligatorio", "No importante", "Solo cumplir leyes"], "Evitar sesgos, desinformación, impacto positivo"),
    ]
    seg_nat = [
        ("¿Qué hace DHCP?", ["Asigna IP automática", "Resuelve nombres", "Enruta", "Cifra"], "Asigna IP automática"),
        ("¿Qué significa NAT?", ["Network Address Translation", "Network Access Translation", "Network Address Table", "Network Automatic Translation"], "Network Address Translation"),
        ("¿Para qué sirve NAT?", ["IPs privadas a Internet", "Aumentar velocidad", "Cifrar", "Filtrar"], "IPs privadas a Internet"),
        ("¿Qué significa PAT?", ["Port Address Translation", "Packet Address Translation", "Protocol Address Translation", "Private Address Translation"], "Port Address Translation"),
        ("¿Qué es VLAN?", ["Red virtual capa 2", "Red de área local", "VPN", "Red inalámbrica"], "Red virtual capa 2"),
        ("¿IPs privadas clase C?", ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12", "169.254.0.0/16"], "192.168.0.0/16"),
    ]
    return cb, osi, ipv4, subnet, dispositivos, cables, claude, seg_nat

preguntas_quiz = []
areas_nombres = list(areas_quiz.keys())
bases = generar_preguntas()
for idx, base in enumerate(bases):
    for p in base:
        if isinstance(p[1], list):
            opciones = p[1].copy()
            random.shuffle(opciones)
            preguntas_quiz.append({
                "area": areas_nombres[idx],
                "tipo": "multiple",
                "pregunta": p[0],
                "opciones": opciones,
                "respuesta": p[2]
            })
        else:
            preguntas_quiz.append({
                "area": areas_nombres[idx],
                "tipo": "vf",
                "pregunta": p[0],
                "opciones": ["Verdadero", "Falso"],
                "respuesta": p[2]
            })

# ==================== SIMULACIONES ====================
if "latency_data" not in st.session_state:
    st.session_state.latency_data = deque(maxlen=20)
    for _ in range(5):
        st.session_state.latency_data.append(random.uniform(20,80))
    st.session_state.latency_activo = False

def actualizar_latencia():
    nueva = random.uniform(20,150)
    st.session_state.latency_data.append(nueva)
    return nueva

def simulador_ping(ip_destino):
    st.markdown(f'<div class="glass-card"><h3 style="margin-top:0;">📡 Ping a {ip_destino}</h3>', unsafe_allow_html=True)
    st.markdown('<div class="latency-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Latencia en Tiempo Real")
    placeholder = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Iniciar monitoreo", key="start_monitor", use_container_width=True):
            st.session_state.latency_activo = True
    with col2:
        if st.button("⏹️ Detener monitoreo", key="stop_monitor", use_container_width=True):
            st.session_state.latency_activo = False
    if st.session_state.latency_activo:
        for _ in range(5):
            nueva = actualizar_latencia()
            fig, ax = plt.subplots(figsize=(10,4))
            ax.set_facecolor('#1e1e2e')
            fig.patch.set_facecolor('#1e1e2e')
            tiempos = list(range(len(st.session_state.latency_data)))
            latencias = list(st.session_state.latency_data)
            ax.plot(tiempos, latencias, linewidth=2, color='#3b82f6')
            ax.fill_between(tiempos, latencias, alpha=0.3, color='#3b82f6')
            ax.axhline(y=100, color='#ef4444', linestyle='--', label='Alerta (>100ms)')
            ax.set_xlabel('Paquete #', color='white')
            ax.set_ylabel('Latencia (ms)', color='white')
            ax.set_title(f'Latencia hacia {ip_destino} - Actual: {nueva:.1f} ms', color='white')
            ax.tick_params(colors='white')
            ax.legend(facecolor='#1e1e2e', labelcolor='white')
            ax.grid(True, alpha=0.2)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(1.5)
            st.rerun()
    else:
        fig, ax = plt.subplots(figsize=(10,4))
        ax.set_facecolor('#1e1e2e')
        fig.patch.set_facecolor('#1e1e2e')
        tiempos = list(range(len(st.session_state.latency_data)))
        latencias = list(st.session_state.latency_data)
        ax.plot(tiempos, latencias, linewidth=2, color='#3b82f6')
        ax.fill_between(tiempos, latencias, alpha=0.3, color='#3b82f6')
        ax.set_xlabel('Paquete #', color='white')
        ax.set_ylabel('Latencia (ms)', color='white')
        ax.set_title(f'Historial de latencia hacia {ip_destino}', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)
        plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("📤 Enviar ping", key="send_ping", use_container_width=True):
        perdida = random.randint(0,20)
        rtt = random.uniform(1,200)
        time.sleep(0.5)
        if perdida > 10:
            st.error(f"⚠️ {perdida}% pérdida de paquetes")
        else:
            st.success(f"✅ Respuesta recibida - Tiempo: {rtt:.1f} ms")
    col_min, col_max, col_prom = st.columns(3)
    with col_min:
        st.metric("📉 Mínimo", f"{min(st.session_state.latency_data):.1f} ms" if st.session_state.latency_data else "N/A")
    with col_max:
        st.metric("📈 Máximo", f"{max(st.session_state.latency_data):.1f} ms" if st.session_state.latency_data else "N/A")
    with col_prom:
        st.metric("📊 Promedio", f"{np.mean(st.session_state.latency_data):.1f} ms" if st.session_state.latency_data else "N/A")
    st.markdown('</div>', unsafe_allow_html=True)

def calculadora_subredes():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧮 Calculadora de Subredes")
    df_mascaras = pd.DataFrame({
        "CIDR": ["/24","/25","/26","/27","/28","/29","/30"],
        "Máscara": ["255.255.255.0","255.255.255.128","255.255.255.192","255.255.255.224","255.255.255.240","255.255.255.248","255.255.255.252"],
        "Hosts útiles": [254,126,62,30,14,6,2]
    })
    st.dataframe(df_mascaras, use_container_width=True, hide_index=True)
    ip_input = st.text_input("📝 Dirección IP con CIDR (ej. 192.168.1.0/24)", placeholder="192.168.1.0/24")
    if ip_input:
        try:
            red = ipaddress.ip_network(ip_input, strict=False)
            col_red1, col_red2 = st.columns(2)
            with col_red1:
                st.info(f"**Red:** {red.network_address}")
                st.info(f"**Máscara:** {red.netmask}")
            with col_red2:
                st.info(f"**Broadcast:** {red.broadcast_address}")
                st.info(f"**Hosts útiles:** {red.num_addresses-2}")
            st.success(f"**Rango de direcciones:** {red[1]} → {red[-2]}")
        except:
            st.error("❌ Formato inválido. Ejemplo: 192.168.1.0/24")
    st.markdown('</div>', unsafe_allow_html=True)

def simulador_traceroute(dominio):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"### 🗺️ Traceroute a {dominio}")
    saltos = random.randint(5,12)
    progress_bar = st.progress(0)
    for i in range(1, saltos+1):
        ip_salto = f"10.0.{i}.1"
        rtt = random.uniform(5,50)
        st.write(f"`{i:2}   {ip_salto}   {rtt:.1f} ms`")
        progress_bar.progress(i/saltos)
        time.sleep(0.2)
    st.success("✅ Rastreo completado exitosamente")
    st.markdown('</div>', unsafe_allow_html=True)

def componentes_red():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🖧 Componentes de Red")
    comps = {
        "🖥️ NIC": "Permite conectar un dispositivo a la red.",
        "🔌 RJ45": "Conector estándar para cables UTP.",
        "🔄 Switch": "Conecta dispositivos en una misma red usando MAC.",
        "🌐 Router": "Conecta redes diferentes y enruta paquetes IP.",
        "📡 Access Point": "Proporciona conectividad WiFi.",
        "🔌 Cable UTP": "Par trenzado sin blindaje.",
        "💡 Fibra óptica": "Utiliza luz, larga distancia, inmune a interferencias.",
        "🛡️ Firewall": "Filtra tráfico según reglas de seguridad.",
        "🗄️ Servidor": "Ofrece servicios (DHCP, DNS, web).",
        "🚪 Gateway": "Puerta de enlace a otras redes."
    }
    cols = st.columns(2)
    for i, (nombre, desc) in enumerate(comps.items()):
        with cols[i%2]:
            st.markdown(f'<div class="component-card"><b>{nombre}</b><br><span style="color:#94a3b8;">{desc}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOPOLOGÍAS ====================
def dibujar_topologia_estrella():
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    ax.set_facecolor('#1e1e2e'); fig.patch.set_facecolor('#1e1e2e')
    centro = (5,4)
    circle = plt.Circle(centro, 0.6, color='#3b82f6', ec='white', lw=2)
    ax.add_patch(circle)
    ax.text(centro[0], centro[1], "Switch", ha='center', va='center', color='white', fontweight='bold')
    dispositivos = [(2,6,"PC1"), (8,6,"PC2"), (2,2,"PC3"), (8,2,"PC4")]
    for x,y,name in dispositivos:
        c = plt.Circle((x,y), 0.4, color='#10b981', ec='white', lw=2)
        ax.add_patch(c)
        ax.text(x, y, name, ha='center', va='center', color='white', fontsize=8)
        ax.plot([x, centro[0]], [y, centro[1]], 'w-', lw=2, alpha=0.7)
    ax.set_title("Topología en Estrella", color='white', fontsize=14)
    return fig

def dibujar_topologia_anillo():
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    ax.set_facecolor('#1e1e2e'); fig.patch.set_facecolor('#1e1e2e')
    angulos = [45,135,225,315]; radios=2.5; centro=(5,4)
    puntos = []
    for ang in angulos:
        rad = np.radians(ang)
        x = centro[0] + radios*np.cos(rad)
        y = centro[1] + radios*np.sin(rad)
        puntos.append((x,y))
    nombres = ["PC1","PC2","PC3","PC4"]
    for i,(x,y) in enumerate(puntos):
        c = plt.Circle((x,y), 0.4, color='#10b981', ec='white', lw=2)
        ax.add_patch(c)
        ax.text(x, y, nombres[i], ha='center', va='center', color='white', fontsize=8)
    for i in range(len(puntos)):
        x1,y1 = puntos[i]
        x2,y2 = puntos[(i+1)%len(puntos)]
        ax.plot([x1,x2],[y1,y2], '#f59e0b', lw=2.5, alpha=0.8)
    ax.set_title("Topología en Anillo", color='white', fontsize=14)
    return fig

def dibujar_topologia_bus():
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    ax.set_facecolor('#1e1e2e'); fig.patch.set_facecolor('#1e1e2e')
    ax.plot([1,9],[4,4], '#ef4444', lw=3, alpha=0.9)
    ax.text(5,4.5, "Cable Principal (Bus)", ha='center', color='#ef4444', fontsize=9, fontweight='bold')
    xs = [2,4,6,8]
    for i,x in enumerate(xs):
        c = plt.Circle((x,3), 0.4, color='#10b981', ec='white', lw=2)
        ax.add_patch(c)
        ax.text(x,3, f"PC{i+1}", ha='center', va='center', color='white', fontsize=8)
        ax.plot([x,x],[3.4,4], 'w-', lw=2, alpha=0.7)
    ax.set_title("Topología en Bus", color='white', fontsize=14)
    return fig

def dibujar_topologia_malla():
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    ax.set_facecolor('#1e1e2e'); fig.patch.set_facecolor('#1e1e2e')
    puntos = [(2,6,"A"), (8,6,"B"), (2,2,"C"), (8,2,"D"), (5,4,"E")]
    coords = [(x,y) for x,y,_ in puntos]
    for x,y,name in puntos:
        c = plt.Circle((x,y), 0.35, color='#10b981', ec='white', lw=2)
        ax.add_patch(c)
        ax.text(x,y,name, ha='center', va='center', color='white', fontsize=9)
    for i in range(len(coords)):
        for j in range(i+1,len(coords)):
            ax.plot([coords[i][0],coords[j][0]],[coords[i][1],coords[j][1]], '#8b5cf6', lw=1.5, alpha=0.5)
    ax.set_title("Topología en Malla (Parcial)", color='white', fontsize=14)
    return fig

def iniciar_topologia(tipo):
    if tipo == "Estrella": return dibujar_topologia_estrella()
    elif tipo == "Anillo": return dibujar_topologia_anillo()
    elif tipo == "Bus": return dibujar_topologia_bus()
    elif tipo == "Malla": return dibujar_topologia_malla()
    return None

# ==================== ESTADO DE SESIÓN ====================
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
    st.session_state.indice = 0
    st.session_state.area = "Conceptos básicos de redes"
    st.session_state.preguntas_juego = []
    st.session_state.feedback = None
    st.session_state.correcta = None
    st.session_state.speed = "Normal"
    st.session_state.voice_type = "Hombre"
    st.session_state.chat_history = []
    st.session_state.topologia_actual = None
    st.session_state.mensaje_mascota = "🌟 ¡Aprende conmigo!"
    st.session_state.messages = []
    st.session_state.mute_audio = False
    st.session_state.input_text = ""

mensajes_mascota = [
    "🌟 ¡Excelente! Sigue así, eres un genio de las redes.",
    "💡 Recuerda: cada gran experto fue una vez principiante. ¡Tú puedes!",
    "🎯 ¡Acertaste! La práctica hace al maestro.",
    "📚 ¿Sabías que las redes son el internet que usas a diario?",
    "🚀 ¡Vamos por más! El conocimiento es poder.",
    "🏆 ¡Eres increíble! Sigue aprendiendo sobre redes.",
    "🔐 La seguridad en redes comienza contigo. ¡Sigue así!"
]

def hablar_mascota():
    mensaje = random.choice(mensajes_mascota)
    st.session_state.mensaje_mascota = mensaje
    speak(mensaje)  # ahora usa gTTS

def nueva_partida(area):
    filtradas = [p for p in preguntas_quiz if p["area"]==area]
    if filtradas:
        cantidad = min(8, len(filtradas))
        st.session_state.preguntas_juego = random.sample(filtradas, cantidad)
    else:
        st.session_state.preguntas_juego = []
        st.warning(f"No hay preguntas para {area}")
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.feedback = None
    st.session_state.correcta = None
    st.session_state.area = area

def responder_quiz(resp, pregunta):
    if resp == pregunta["respuesta"]:
        st.session_state.puntaje += 10
        st.session_state.feedback = f"✅ ¡Correcto! +10 puntos"
        st.session_state.correcta = True
        speak("Correcto. Ganaste 10 puntos.")
    else:
        st.session_state.feedback = f"❌ Incorrecto. Respuesta: {pregunta['respuesta']}"
        st.session_state.correcta = False
        speak(f"Incorrecto. La respuesta correcta es: {pregunta['respuesta']}")
    st.session_state.indice += 1
    st.rerun()

# ==================== MASCOTA ANIMADA ====================
st.markdown(f"""
<div class="mascota-container">
    <div style="font-size:55px; background:linear-gradient(135deg,#3b82f6,#8b5cf6); border-radius:50%; padding:12px; box-shadow:0 8px 25px rgba(0,0,0,0.3);">🦊</div>
    <div class="mascota-speech">{st.session_state.mensaje_mascota}</div>
</div>
""", unsafe_allow_html=True)
col_m1, col_m2, _ = st.columns([1,1,8])
with col_m1:
    if st.button("🦊", key="btn_mascota", help="¡Haz clic para que la mascota te hable!"):
        hablar_mascota()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942783.png", width=70)
    st.markdown("</div>")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Configuración")
    voice_opts = ["👨 Hombre","👩 Mujer","🧒 Niño","👧 Niña"]
    sel = st.selectbox("🎤 Voz", voice_opts, index=0)
    st.session_state.voice_type = sel  # solo para mostrar, no se usa en TTS
    st.session_state.speed = st.selectbox("⚡ Velocidad", ["Normal","Lenta"])
    st.markdown("---")
    st.markdown(f"✅ **Quiz:** {len(preguntas_quiz)} preguntas")
    st.markdown(f"🧠 **Chat:** {len(knowledge)} conceptos + IA Groq")
    st.markdown("---")
    st.markdown("### 🧪 Laboratorio")
    st.markdown("- Ping con gráfico en tiempo real")
    st.markdown("- Calculadora de subredes")
    st.markdown("- Traceroute simulado")
    st.markdown("- Componentes de red")
    st.markdown("- Topologías interactivas")
    st.markdown("---")
    st.markdown("### 🎓 Créditos")
    st.caption("Proyecto educativo de Redes de Computadoras (Redes II) que integra un chat basado en Inteligencia Artificial con tecnología de Groq para apoyar el aprendizaje interactivo de los estudiantes. Developed by Joswii")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TABS ====================
st.markdown('<h1 class="premium-title">🌐 REDES II Y TELECOMUNICACIONES</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; margin-bottom:30px;">✨ INGENIERIA DE SISTEMAS UAP ✨</p>', unsafe_allow_html=True)
tabs = st.tabs(["📝 Quiz de Redes", "💬 Chat Inteligente", "🔧 Laboratorio de Redes", "🤖 IA con Claude"])

# -------------------- TAB 1: QUIZ --------------------
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1,2,1])
    with col_b2:
        if st.button("🎉 Mensaje de Bienvenida", use_container_width=True):
            st.balloons()
            speak("INGENIERIA DE SISTEMAS UNIVERSIDAD AMAZONICA DE PANDO.")
    st.markdown("### 📡 Elige tu área de conocimiento")
    areas_iconos = {
        "Conceptos básicos de redes": "🌐",
        "Modelo OSI": "🥧",
        "Direccionamiento IPv4": "🔢",
        "Subneteo y máscaras": "✂️",
        "Dispositivos y comandos": "🖥️",
        "Cables y conexiones": "🔌",
        "Inteligencia Artificial Claude AI": "🤖",
        "Seguridad, DHCP, VLAN, NAT": "🛡️",
    }
    cols_areas = st.columns(4)
    for i, (area, icono) in enumerate(areas_iconos.items()):
        with cols_areas[i % 4]:
            st.markdown(f'<div class="area-card"><div class="area-icon">{icono}</div><div class="area-name">{area}</div></div>', unsafe_allow_html=True)
            if st.button(f"Seleccionar", key=f"btn_{area}", use_container_width=True):
                nueva_partida(area)
                st.rerun()
    st.markdown("---")
    if st.session_state.area:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1e3a5f, #1e293b); padding: 12px; border-radius: 20px; text-align: center; margin-bottom: 20px;">🎯 Área actual: <strong style="color:#60a5fa;">{st.session_state.area}</strong></div>', unsafe_allow_html=True)
    if st.session_state.preguntas_juego:
        col_prog1, col_prog2 = st.columns([3,1])
        with col_prog1:
            prog = st.session_state.indice / len(st.session_state.preguntas_juego)
            st.progress(prog, text=f"Progreso: {st.session_state.indice}/{len(st.session_state.preguntas_juego)}")
        with col_prog2:
            st.markdown(f'<div class="puntaje" style="float:right;">🏆 {st.session_state.puntaje} pts</div>', unsafe_allow_html=True)
        pts = st.session_state.puntaje
        if pts>=70: medalla="🏆 SUPER GENIO 👑"
        elif pts>=50: medalla="🥇 EXCELENTE ⭐"
        elif pts>=30: medalla="🥈 MUY BIEN 🌟"
        elif pts>=10: medalla="🥉 SIGUE ASÍ 💪"
        else: medalla="🎯 EMPEZAR CON LAS PREGUNTAS 🎮"
        st.markdown(f'<div class="medalla">{medalla}</div>', unsafe_allow_html=True)
        if st.session_state.indice >= len(st.session_state.preguntas_juego):
            st.balloons()
            st.success(f"🎉 ¡Felicidades! Completaste con {st.session_state.puntaje} puntos. {medalla}")
            hablar_mascota()
            if st.button("🎮 Jugar de nuevo", use_container_width=True):
                nueva_partida(st.session_state.area)
                st.rerun()
        else:
            p = st.session_state.preguntas_juego[st.session_state.indice]
            st.markdown('<div class="question-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-text">📝 {p["pregunta"]}</div>', unsafe_allow_html=True)
            if st.button("🔊 Leer pregunta", key="speak_q"):
                texto = p["pregunta"] + ". Opciones: " + ", ".join(p["opciones"])
                speak(texto)
            respuesta = st.radio("Selecciona tu respuesta:", p["opciones"], key=f"q{st.session_state.indice}", label_visibility="collapsed")
            if st.button("✅ Verificar respuesta", use_container_width=True):
                responder_quiz(respuesta, p)
            if st.session_state.feedback:
                cls = "feedback-correcto" if st.session_state.correcta else "feedback-incorrecto"
                st.markdown(f'<div class="{cls}">{st.session_state.feedback}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("✨ Selecciona un área arriba para comenzar el quiz.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- TAB 2: CHAT INTELIGENTE --------------------
with tabs[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 💬 Asistente IA de Redes")
    st.markdown("Pregunta sobre redes, protocolos, dispositivos y más. El asistente usa IA avanzada.")
    col_clear, col_mute = st.columns(2)
    with col_clear:
        if st.button("🧹 Limpiar conversación", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
    with col_mute:
        label_mute = "🔇 Silenciar IA" if not st.session_state.mute_audio else "🔊 Activar IA"
        if st.button(label_mute, use_container_width=True):
            st.session_state.mute_audio = not st.session_state.mute_audio
            st.rerun()
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    # --- Entrada de micrófono nativa ---
    st.markdown("### 🎤 Captura por voz")
    audio_value = st.audio_input("Grabar un mensaje de voz")
    if audio_value:
        with st.spinner("Transcribiendo..."):
            try:
                # Guardar temporalmente el audio (es un BytesIO con datos WAV)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                    tmpfile.write(audio_value.getvalue())
                    tmp_path = tmpfile.name
                recognizer = sr.Recognizer()
                with sr.AudioFile(tmp_path) as source:
                    audio_data = recognizer.record(source)
                transcribed_text = recognizer.recognize_google(audio_data, language="es-ES")
                st.session_state.input_text = transcribed_text
                st.success(f"Texto transcrito: {transcribed_text}")
                os.unlink(tmp_path)
            except sr.UnknownValueError:
                st.error("No se pudo entender el audio. Inténtalo de nuevo.")
            except sr.RequestError as e:
                st.error(f"Error con el servicio de reconocimiento: {e}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")
    # Entrada de texto
    user_text = st.text_area(
        "Escribe tu consulta:",
        value=st.session_state.input_text,
        height=80,
        placeholder="Ejemplo: ¿Qué es una dirección IP?"
    )
    if st.button("🚀 Enviar mensaje", type="primary", use_container_width=True):
        if user_text.strip():
            st.session_state.messages.append({"role": "user", "content": user_text.strip()})
            st.session_state.input_text = ""
            st.rerun()
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("✨ Pensando..."):
            try:
                system_prompt = {
                    "role": "system",
                    "content": "Eres un asistente experto en redes de computadoras. Responde SIEMPRE de forma muy breve y concisa (máximo 2-3 oraciones). Ve directo al punto. Usa un tono natural y humano."
                }
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[system_prompt] + st.session_state.messages,
                    temperature=0.7,
                    max_tokens=150
                )
                respuesta = completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                if not st.session_state.mute_audio:
                    speak(respuesta)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
                respuesta = "Lo siento, hubo un error temporal. Por favor, intenta de nuevo."
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- TAB 3: LABORATORIO --------------------
with tabs[2]:
    st.markdown("## 🔧 Laboratorio de Redes")
    st.markdown("Herramientas interactivas para aprender y simular conceptos de redes")
    st.markdown('<div class="section-title">📡 Topologías de Red Interactivas</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.markdown('<div style="text-align:center; padding:15px; background:rgba(59,130,246,0.1); border-radius:16px;">⭐ Estrella</div>', unsafe_allow_html=True)
        if st.button("Visualizar Estrella", key="top_estrella", use_container_width=True):
            st.session_state.topologia_actual = "Estrella"
            speak("Mostrando topología en estrella")
    with col_t2:
        st.markdown('<div style="text-align:center; padding:15px; background:rgba(139,92,246,0.1); border-radius:16px;">🔄 Anillo</div>', unsafe_allow_html=True)
        if st.button("Visualizar Anillo", key="top_anillo", use_container_width=True):
            st.session_state.topologia_actual = "Anillo"
            speak("Mostrando topología en anillo")
    with col_t3:
        st.markdown('<div style="text-align:center; padding:15px; background:rgba(16,185,129,0.1); border-radius:16px;">📏 Bus</div>', unsafe_allow_html=True)
        if st.button("Visualizar Bus", key="top_bus", use_container_width=True):
            st.session_state.topologia_actual = "Bus"
            speak("Mostrando topología en bus")
    with col_t4:
        st.markdown('<div style="text-align:center; padding:15px; background:rgba(245,158,11,0.1); border-radius:16px;">🔗 Malla</div>', unsafe_allow_html=True)
        if st.button("Visualizar Malla", key="top_malla", use_container_width=True):
            st.session_state.topologia_actual = "Malla"
            speak("Mostrando topología en malla")
    if st.session_state.topologia_actual:
        st.markdown("---")
        fig = iniciar_topologia(st.session_state.topologia_actual)
        if fig:
            st.pyplot(fig)
        detalles = {
            "Estrella": {"desc":"Todos los dispositivos se conectan a un switch central.","ventajas":"✅ Fácil de instalar, centralizado.","desventajas":"❌ Fallo del switch afecta toda la red."},
            "Anillo": {"desc":"Cada dispositivo conectado a otros dos formando un círculo.","ventajas":"✅ Organizada, no requiere central.","desventajas":"❌ Un fallo puede interrumpir la red."},
            "Bus": {"desc":"Un único cable compartido.","ventajas":"✅ Poco cable, económica.","desventajas":"❌ Fallo del bus colapsa la red, muchas colisiones."},
            "Malla": {"desc":"Cada dispositivo se conecta a muchos otros.","ventajas":"✅ Alta redundancia y confiabilidad.","desventajas":"❌ Muy costosa y compleja."}
        }
        d = detalles.get(st.session_state.topologia_actual, {})
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f'<div style="background:rgba(59,130,246,0.1); border-radius:16px; padding:15px;"><b>📖 Descripción</b><br>{d.get("desc","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:rgba(16,185,129,0.1); border-radius:16px; padding:15px; margin-top:10px;"><b>✅ Ventajas</b><br>{d.get("ventajas","")}</div>', unsafe_allow_html=True)
        with col_d2:
            st.markdown(f'<div style="background:rgba(239,68,68,0.1); border-radius:16px; padding:15px;"><b>❌ Desventajas</b><br>{d.get("desventajas","")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🛠️ Herramientas de Diagnóstico</div>', unsafe_allow_html=True)
    col_her1, col_her2 = st.columns(2)
    with col_her1:
        simulador_ping("8.8.8.8")
    with col_her2:
        calculadora_subredes()
    
    st.markdown('<div class="section-title">🗺️ Análisis de Ruta (Traceroute)</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_tr1, col_tr2 = st.columns([3,1])
    with col_tr1:
        dom = st.text_input("🌐 Dominio o IP para rastrear", "google.com", key="trace_domain")
    with col_tr2:
        if st.button("🚀 Iniciar Traceroute", use_container_width=True):
            simulador_traceroute(dom)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🖧 Componentes de Red</div>', unsafe_allow_html=True)
    componentes_red()

# -------------------- TAB 4: IA CON CLAUDE --------------------
with tabs[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🤖 Inteligencia Artificial: Claude AI")
    st.markdown("Conoce a Claude, el asistente de IA desarrollado por **Anthropic** con un enfoque en ser **útil, honesto y inofensivo**.")
    col_inf1, col_inf2 = st.columns([2,1])
    with col_inf1:
        st.markdown("""
        <div style="background: rgba(59,130,246,0.1); border-radius: 20px; padding: 1.5rem;">
            <h3>✨ ¿Qué es Claude?</h3>
            <p>Claude es un modelo de lenguaje grande (LLM) creado por Anthropic. Fue entrenado usando <strong>IA Constitucional</strong>, un método que le permite seguir principios éticos claros.</p>
            <h3>🎯 Características destacadas</h3>
            <ul>
                <li>Ventana de contexto de hasta 200,000 tokens.</li>
                <li>Razonamiento avanzado en matemáticas, programación y análisis.</li>
                <li>Capacidad multilingüe (incluye español perfecto).</li>
                <li>Generación de código en Python, JavaScript, Java, etc.</li>
                <li>Análisis de documentos (PDF, TXT, CSV).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_inf2:
        st.image("https://www.anthropic.com/_next/static/media/claude-icon.2e8e6c8c.svg", width=180)
        st.markdown("""
        <div style="background: rgba(139,92,246,0.1); border-radius: 20px; padding: 1rem; text-align: center; margin-top: 1rem;">
            <span style="font-size: 3rem;">🧠</span><br>
            <b>IA Constitucional</b><br>
            <small>Entrenada con principios éticos.</small>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📈 Evolución de Claude")
    st.markdown("""
    | Versión | Lanzamiento | Contexto | Características |
    |---------|-------------|----------|------------------|
    | Claude 1 | 2021 (beta) | 9k tokens | Primer asistente |
    | Claude 2 | Julio 2023 | 100k tokens | Mejora en razonamiento |
    | Claude 2.1 | Nov 2023 | 200k tokens | Reducción de alucinaciones |
    | Claude 3 | Mar 2024 | 200k tokens | Velocidad extrema, visión |
    """)
    st.markdown("---")
    st.markdown("### 🚀 Aplicaciones prácticas")
    col_apl1, col_apl2, col_apl3 = st.columns(3)
    with col_apl1:
        st.markdown("""<div style="background:rgba(16,185,129,0.1); border-radius:16px; padding:1rem;"><h4>👩‍🎓 Estudiantes</h4><ul><li>Explicaciones personalizadas</li><li>Resúmenes de textos</li><li>Ayuda con ejercicios</li></ul></div>""", unsafe_allow_html=True)
    with col_apl2:
        st.markdown("""<div style="background:rgba(245,158,11,0.1); border-radius:16px; padding:1rem;"><h4>👩‍🏫 Docentes</h4><ul><li>Creación de planes de clase</li><li>Material didáctico</li><li>Rúbricas de evaluación</li></ul></div>""", unsafe_allow_html=True)
    with col_apl3:
        st.markdown("""<div style="background:rgba(59,130,246,0.1); border-radius:16px; padding:1rem;"><h4>💻 Programadores</h4><ul><li>Depuración de código</li><li>Documentación automática</li><li>Refactorización</li></ul></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2)); border-radius: 20px; padding: 1.5rem; text-align: center;">
        <i>"La inteligencia artificial debe ser útil, honesta e inofensiva. Ese es el núcleo del enfoque de Anthropic con Claude."</i><br>
        — Equipo de Anthropic
    </div>
    """, unsafe_allow_html=True)
    st.info("🔗 **Más información:** [anthropic.com/claude](https://www.anthropic.com/claude)")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); padding: 20px; border-radius: 16px; text-align: center; margin-top: 20px;">
    <p style="color: #94a3b8;">🌐 Proyecto de enseñanza y aprendizaje - Fundamentos de redes de computadoras</p>
    <p style="color: #64748b; font-size: 0.75rem;">Desarrollado con Claude.AI - Quiz interactivo + Chat con IA Groq + Laboratorio de redes</p>
</div>
""", unsafe_allow_html=True)
