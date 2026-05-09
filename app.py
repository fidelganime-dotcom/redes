import streamlit as st
import random
import time
import os
import tempfile
import re
import base64
import ipaddress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
from groq import Groq
from streamlit_mic_recorder import speech_to_text
# ---------- VERIFICAR DEPENDENCIAS DE VOZ ----------
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except:
    PYTTSX3_AVAILABLE = False
try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
    pygame.mixer.init()
except:
    GTTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except:
    SR_AVAILABLE = False

# ---------- CONFIGURACIÓN STREAMLIT ----------
st.set_page_config(
    page_title="REDES BÁSICAS - TECNO KIDS", 
    page_icon="🌐", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CLIENTE GROQ ----------
#client = Groq(api_key="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")
client = Groq(api_key="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")

# ==================== CSS PREMIUM ====================
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

/* Main app styling */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}

/* Elegant glass cards */
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

/* Premium headers */
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

/* Buttons refined */
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

/* Sidebar elegant */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] .stMarkdown {
    color: var(--white);
}

/* Input fields refined */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    color: var(--white) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    outline: none !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 10px !important;
}

/* Tabs styling */
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

/* Metric display */
.metric-value {
    transition: all 0.3s ease;
}

.metric-value:hover {
    transform: scale(1.1);
    text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

/* Info box */
.info-box {
    background: rgba(59, 130, 246, 0.08);
    border-radius: 20px;
    padding: 20px;
    margin: 16px 0;
    border: 1px solid rgba(59, 130, 246, 0.2);
    transition: all 0.3s ease;
}

.info-box:hover {
    background: rgba(59, 130, 246, 0.12);
    transform: translateX(4px);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

/* Scrollbar */
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

::-webkit-scrollbar-thumb:hover {
    background: rgba(59, 130, 246, 0.6);
}

/* Chat bubbles */
.chat-bubble-user {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 20px 20px 5px 20px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 80%;
    align-self: flex-end;
}

.chat-bubble-bot {
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 20px 20px 20px 5px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 80%;
    align-self: flex-start;
    border-left: 3px solid #3b82f6;
}

/* Area cards */
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

.area-icon {
    font-size: 2.5rem;
}

.area-name {
    font-weight: 600;
    color: #f1f5f9;
    margin-top: 8px;
    font-size: 0.9rem;
}

/* Component card */
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

/* Latency container */
.latency-container {
    background: rgba(0,0,0,0.3);
    border-radius: 16px;
    padding: 15px;
    margin: 10px 0;
}

/* Question box */
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

/* Feedback */
.feedback-correcto {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80;
    padding: 1rem;
    border-radius: 16px;
    border-left: 4px solid #22c55e;
    backdrop-filter: blur(8px);
}

.feedback-incorrecto {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    padding: 1rem;
    border-radius: 16px;
    border-left: 4px solid #ef4444;
    backdrop-filter: blur(8px);
}

/* Medal display */
.medalla {
    font-size: 1.3rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.2));
    padding: 12px;
    border-radius: 60px;
    margin: 10px 0;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Score display */
.puntaje {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    padding: 8px 20px;
    border-radius: 60px;
    font-weight: bold;
    font-size: 1.5rem;
    color: white;
    display: inline-block;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
}

/* Mascota container */
.mascota-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: bounce 2s infinite;
}

.mascota-container:hover {
    transform: scale(1.1);
}

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
    0%, 100% { opacity: 0; transform: scale(0.9); }
    10%, 90% { opacity: 1; transform: scale(1); }
}

/* Watermark */
.watermark {
    position: fixed;
    bottom: 15px;
    left: 15px;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(10px);
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 500;
    z-index: 999;
}

/* Responsive */
@media (max-width: 768px) {
    .premium-title {
        font-size: 1.8rem;
    }
    .section-title {
        font-size: 1.2rem;
    }
    .question-text {
        font-size: 1rem;
    }
}
</style>

<div class="watermark">🌐 REDES BÁSICAS</div>
"""

st.markdown(STYLES, unsafe_allow_html=True)

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
    "Inteligencia Artificial Claude AI": [],  # ← reemplazo solicitado
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
    # ==================== NUEVAS PREGUNTAS SOBRE CLAUDE AI ====================
    claude_preguntas = [
        ("¿Qué es Claude y cuál es el principal objetivo de esta inteligencia artificial desarrollada por Anthropic?",
         ["Asistente conversacional útil, honesto e inofensivo", "Un motor de búsqueda web", "Un sistema operativo", "Un antivirus"],
         "Asistente conversacional útil, honesto e inofensivo"),
        ("¿Por qué Claude es considerado un asistente confiable?",
         ["Porque fue entrenado con principios éticos y de IA constitucional", "Porque tiene acceso a todo internet sin restricciones", "Porque es el único modelo disponible", "Porque reemplaza a los humanos"],
         "Porque fue entrenado con principios éticos y de IA constitucional"),
        ("¿Qué tipo de tareas puede realizar Claude para estudiantes y docentes?",
         ["Explicar temas complejos, generar resúmenes y ayudar con código", "Solo jugar videojuegos", "Conducir autos", "Hacer tareas físicas"],
         "Explicar temas complejos, generar resúmenes y ayudar con código"),
        ("¿Cuál fue la razón principal por la que ex investigadores de OpenAI crearon Anthropic?",
         ["Enfocarse en IA segura y ética", "Ganar más dinero", "Copiar modelos existentes", "Vender datos personales"],
         "Enfocarse en IA segura y ética"),
        ("¿En qué año fue creada Anthropic?",
         ["2021", "2018", "2020", "2022"], "2021"),
        ("La seguridad y la ética son aspectos importantes en el desarrollo de modelos como Claude.",
         ["Verdadero", "Falso"], "Verdadero"),
        ("¿Cómo ha evolucionado Claude desde su lanzamiento inicial?",
         ["Ha mejorado en comprensión, capacidad de contexto y razonamiento", "Sigue siendo igual", "Ha empeorado", "Solo cambió su nombre"],
         "Ha mejorado en comprensión, capacidad de contexto y razonamiento"),
        ("¿Qué mejora importante tuvo Claude en programación?",
         ["Generar y depurar código en múltiples lenguajes", "Reemplazar completamente a los programadores", "Solo escribir Java", "No entiende código"],
         "Generar y depurar código en múltiples lenguajes"),
        ("¿Cuál es la diferencia general entre Claude 2, 2.1 y Claude 3?",
         ["Cada versión es más rápida, precisa y con mayor capacidad", "Solo cambió el nombre", "La versión 3 es más lenta", "No hay diferencias"],
         "Cada versión es más rápida, precisa y con mayor capacidad"),
        ("Cada nueva versión de Claude es más rápida, precisa e inteligente que la anterior.",
         ["Verdadero", "Falso"], "Verdadero"),
        ("¿Qué beneficio ofrece Claude a los estudiantes?",
         ["Ayuda a entender temas, resolver dudas y practicar ejercicios", "Hace los exámenes por ellos", "Solo da respuestas literales", "No es útil para estudiantes"],
         "Ayuda a entender temas, resolver dudas y practicar ejercicios"),
        ("¿De qué manera los docentes pueden usar Claude?",
         ["Como apoyo para explicar conceptos y generar material didáctico", "Para que enseñe en su lugar", "Solo para calificar exámenes", "No puede ayudar a docentes"],
         "Como apoyo para explicar conceptos y generar material didáctico"),
        ("¿Cómo puede ayudar Claude a los programadores?",
         ["Escribir código, encontrar errores y sugerir optimizaciones", "Hackear sistemas", "Diseñar hardware", "Solo responder correos"],
         "Escribir código, encontrar errores y sugerir optimizaciones"),
        ("¿Por qué muchas empresas usan asistentes como Claude?",
         ["Automatizar tareas, mejorar atención al cliente y análisis de datos", "Para espiar a los empleados", "Porque es gratuito", "Para eliminar puestos de trabajo"],
         "Automatizar tareas, mejorar atención al cliente y análisis de datos"),
        ("¿Cuáles son las principales funciones de Claude en análisis de información?",
         ["Resumir documentos, extraer datos clave y responder preguntas", "Modificar archivos sin permiso", "Borrar información", "Crear virus"],
         "Resumir documentos, extraer datos clave y responder preguntas"),
        ("¿Cómo influye Claude en la transformación digital educativa?",
         ["Facilitando el acceso a conocimiento personalizado y tutoría inteligente", "Reemplazando las escuelas", "Limitando el aprendizaje", "Solo para entretenimiento"],
         "Facilitando el acceso a conocimiento personalizado y tutoría inteligente"),
        ("Claude es considerado una herramienta importante en el desarrollo actual de IA porque:",
         ["Demuestra que se puede tener IA potente, útil y alineada con valores humanos", "Es el único modelo existente", "No tiene competencia", "Es de código abierto"],
         "Demuestra que se puede tener IA potente, útil y alineada con valores humanos"),
        ("¿Qué importancia tiene el Procesamiento de Lenguaje Natural (NLP) en Claude?",
         ["Es el núcleo que le permite entender y generar lenguaje humano", "No usa NLP", "Solo para traducir idiomas", "Para reconocer imágenes"],
         "Es el núcleo que le permite entender y generar lenguaje humano"),
        ("¿Cómo contribuye Claude al aprendizaje conversacional?",
         ["Manteniendo diálogos fluidos y adaptándose al nivel del usuario", "Dando respuestas fijas sin interacción", "Interrumpiendo constantemente", "Solo leyendo textos"],
         "Manteniendo diálogos fluidos y adaptándose al nivel del usuario"),
        ("¿Por qué es importante usar herramientas de IA como Claude de manera ética?",
         ["Para evitar sesgos, desinformación y asegurar un impacto positivo", "Porque es obligatorio", "No es importante", "Solo para cumplir leyes"],
         "Para evitar sesgos, desinformación y asegurar un impacto positivo"),
    ]
    seg_nat = [
        ("¿Qué hace DHCP?", ["Asigna IP automática", "Resuelve nombres", "Enruta", "Cifra"], "Asigna IP automática"),
        ("¿Qué significa NAT?", ["Network Address Translation", "Network Access Translation", "Network Address Table", "Network Automatic Translation"], "Network Address Translation"),
        ("¿Para qué sirve NAT?", ["IPs privadas a Internet", "Aumentar velocidad", "Cifrar", "Filtrar"], "IPs privadas a Internet"),
        ("¿Qué significa PAT?", ["Port Address Translation", "Packet Address Translation", "Protocol Address Translation", "Private Address Translation"], "Port Address Translation"),
        ("¿Qué es VLAN?", ["Red virtual capa 2", "Red de área local", "VPN", "Red inalámbrica"], "Red virtual capa 2"),
        ("¿IPs privadas clase C?", ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12", "169.254.0.0/16"], "192.168.0.0/16"),
    ]
    # Retornamos ahora 8 listas (la sexta es claude_preguntas)
    return cb, osi, ipv4, subnet, dispositivos, cables, claude_preguntas, seg_nat

preguntas_quiz = []
areas_nombres = list(areas_quiz.keys())
bases = generar_preguntas()
for idx, base in enumerate(bases):
    for p in base:
        if isinstance(p[1], list):  # opciones múltiples
            opciones_mezcladas = p[1].copy()
            respuesta_correcta = p[2]
            random.shuffle(opciones_mezcladas)
            preguntas_quiz.append({"area": areas_nombres[idx], "tipo": "multiple", "pregunta": p[0], "opciones": opciones_mezcladas, "respuesta": respuesta_correcta})
        else:  # verdadero/falso
            preguntas_quiz.append({"area": areas_nombres[idx], "tipo": "vf", "pregunta": p[0], "opciones": ["Verdadero", "Falso"], "respuesta": p[2]})

# ==================== FUNCIONES DE VOZ ====================
def speak_human(text, voice_gender, speed="Normal"):
    if not PYTTSX3_AVAILABLE:
        speak_gtts(text, speed)
        return
    clean = re.sub(r'[^\w\sáéíóúñ]', '', text)
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150 if speed=="Normal" else 120)
        voices = engine.getProperty('voices')
        keywords = {"Hombre": ["male","raul","diego"], "Mujer":["female","sabina","helena"], "Niño":["boy","child"], "Niña":["girl","child"]}
        selected_id = None
        for v in voices:
            v_name = v.name.lower()
            if any(k in v_name for k in keywords.get(voice_gender, [])):
                selected_id = v.id
                break
        if selected_id:
            engine.setProperty('voice', selected_id)
        engine.say(clean)
        engine.runAndWait()
        engine.stop()
    except:
        speak_gtts(text, speed)

def speak_gtts(text, speed="Normal"):
    if not GTTS_AVAILABLE:
        return
    clean = re.sub(r'[^\w\sáéíóúñ]', '', text)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp = f.name
        tts = gTTS(clean, lang="es", slow=(speed=="Lenta"))
        tts.save(tmp)
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.unlink(tmp)
    except:
        pass

def speak(text, voice_type, speed="Normal"):
    speak_human(text, voice_type, speed)

# ==================== SIMULACIONES ====================
if "latency_data" not in st.session_state:
    st.session_state.latency_data = deque(maxlen=20)
    for _ in range(5):
        st.session_state.latency_data.append(random.uniform(20, 80))
    st.session_state.latency_activo = False

def actualizar_latencia():
    nueva_latencia = random.uniform(20, 150)
    st.session_state.latency_data.append(nueva_latencia)
    return nueva_latencia

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
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.set_facecolor('#1e1e2e')
            fig.patch.set_facecolor('#1e1e2e')
            
            tiempos = list(range(len(st.session_state.latency_data)))
            latencias = list(st.session_state.latency_data)
            
            ax.plot(tiempos, latencias, linewidth=2, color='#3b82f6')
            ax.fill_between(tiempos, latencias, alpha=0.3, color='#3b82f6')
            ax.axhline(y=100, color='#ef4444', linestyle='--', linewidth=1, label='Alerta (>100ms)')
            ax.set_xlabel('Paquete #', color='white')
            ax.set_ylabel('Latencia (ms)', color='white')
            ax.set_title(f'Latencia hacia {ip_destino} - Actual: {nueva:.1f} ms', color='white', fontweight='bold')
            ax.tick_params(colors='white')
            ax.legend(facecolor='#1e1e2e', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.2)
            
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(1.5)
            st.rerun()
    else:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_facecolor('#1e1e2e')
        fig.patch.set_facecolor('#1e1e2e')
        tiempos = list(range(len(st.session_state.latency_data)))
        latencias = list(st.session_state.latency_data)
        ax.plot(tiempos, latencias, linewidth=2, color='#3b82f6')
        ax.fill_between(tiempos, latencias, alpha=0.3, color='#3b82f6')
        ax.set_xlabel('Paquete #', color='white')
        ax.set_ylabel('Latencia (ms)', color='white')
        ax.set_title(f'Historial de latencia hacia {ip_destino}', color='white', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)
        plt.close(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📤 Enviar ping", key="send_ping", use_container_width=True):
        perdida = random.randint(0, 20)
        rtt = random.uniform(1, 200)
        with st.spinner("Enviando paquetes ICMP..."):
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
        "CIDR": ["/24", "/25", "/26", "/27", "/28", "/29", "/30"],
        "Máscara": ["255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252"],
        "Hosts útiles": [254, 126, 62, 30, 14, 6, 2],
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
    saltos = random.randint(5, 12)
    progress_bar = st.progress(0)
    for i in range(1, saltos+1):
        ip_salto = f"10.0.{i}.1"
        rtt = random.uniform(5, 50)
        st.write(f"`{i:2}   {ip_salto}   {rtt:.1f} ms`")
        progress_bar.progress(i/saltos)
        time.sleep(0.2)
    st.success("✅ Rastreo completado exitosamente")
    st.markdown('</div>', unsafe_allow_html=True)

def componentes_red():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🖧 Componentes de Red")
    comps = {
        "🖥️ NIC (Tarjeta de red)": "Permite conectar un dispositivo a la red (cableada o inalámbrica).",
        "🔌 RJ45": "Conector estándar para cables UTP.",
        "🔄 Switch": "Conecta dispositivos en una misma red usando direcciones MAC.",
        "🌐 Router": "Conecta redes diferentes y enruta paquetes IP.",
        "📡 Access Point": "Proporciona conectividad WiFi.",
        "🔌 Cable UTP": "Par trenzado sin blindaje, usado en redes Ethernet.",
        "💡 Fibra óptica": "Utiliza luz para transmitir datos, larga distancia e inmunidad a interferencias.",
        "🛡️ Firewall": "Filtra tráfico según reglas de seguridad.",
        "🗄️ Servidor": "Ofrece servicios (DHCP, DNS, web, etc.) a los clientes.",
        "🚪 Gateway": "Puerta de enlace que permite salir de la red local a Internet."
    }
    cols = st.columns(2)
    for i, (nombre, desc) in enumerate(comps.items()):
        with cols[i % 2]:
            st.markdown(f'<div class="component-card"><b>{nombre}</b><br><span style="color:#94a3b8; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOPOLOGÍAS ====================
def dibujar_topologia_estrella():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#1e1e2e')
    fig.patch.set_facecolor('#1e1e2e')
    
    centro = (5, 4)
    circle_center = plt.Circle(centro, 0.6, color='#3b82f6', ec='white', linewidth=2, zorder=3)
    ax.add_patch(circle_center)
    ax.text(centro[0], centro[1], "Switch", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    
    dispositivos = [(2, 6, "PC1"), (8, 6, "PC2"), (2, 2, "PC3"), (8, 2, "PC4")]
    for x, y, name in dispositivos:
        circle = plt.Circle((x, y), 0.4, color='#10b981', ec='white', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        ax.plot([x, centro[0]], [y, centro[1]], 'w-', linewidth=2, alpha=0.7, zorder=1)
    
    ax.set_title("Topología en Estrella", color='white', fontsize=14, fontweight='bold')
    return fig

def dibujar_topologia_anillo():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#1e1e2e')
    fig.patch.set_facecolor('#1e1e2e')
    
    angulos = [45, 135, 225, 315]
    radios = 2.5
    centro = (5, 4)
    puntos = []
    for ang in angulos:
        rad = np.radians(ang)
        x = centro[0] + radios * np.cos(rad)
        y = centro[1] + radios * np.sin(rad)
        puntos.append((x, y))
    
    nombres = ["PC1", "PC2", "PC3", "PC4"]
    for i, (x, y) in enumerate(puntos):
        circle = plt.Circle((x, y), 0.4, color='#10b981', ec='white', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, nombres[i], ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    
    for i in range(len(puntos)):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i+1) % len(puntos)]
        ax.plot([x1, x2], [y1, y2], '#f59e0b', linewidth=2.5, alpha=0.8, zorder=1)
    
    ax.set_title("Topología en Anillo", color='white', fontsize=14, fontweight='bold')
    return fig

def dibujar_topologia_bus():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#1e1e2e')
    fig.patch.set_facecolor('#1e1e2e')
    
    ax.plot([1, 9], [4, 4], '#ef4444', linewidth=3, alpha=0.9, zorder=1)
    ax.text(5, 4.5, "Cable Principal (Bus)", ha='center', color='#ef4444', fontsize=9, fontweight='bold')
    
    xs = [2, 4, 6, 8]
    for i, x in enumerate(xs):
        circle = plt.Circle((x, 3), 0.4, color='#10b981', ec='white', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, 3, f"PC{i+1}", ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        ax.plot([x, x], [3.4, 4], 'w-', linewidth=2, alpha=0.7, zorder=1)
    
    ax.set_title("Topología en Bus", color='white', fontsize=14, fontweight='bold')
    return fig

def dibujar_topologia_malla():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#1e1e2e')
    fig.patch.set_facecolor('#1e1e2e')
    
    puntos = [(2, 6, "A"), (8, 6, "B"), (2, 2, "C"), (8, 2, "D"), (5, 4, "E")]
    coords = [(x, y) for x, y, _ in puntos]
    
    for x, y, name in puntos:
        circle = plt.Circle((x, y), 0.35, color='#10b981', ec='white', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
    
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            ax.plot([coords[i][0], coords[j][0]], [coords[i][1], coords[j][1]], 
                   '#8b5cf6', linewidth=1.5, alpha=0.5, zorder=1)
    
    ax.set_title("Topología en Malla (Parcial)", color='white', fontsize=14, fontweight='bold')
    return fig

def iniciar_topologia(tipo):
    if tipo == "Estrella":
        return dibujar_topologia_estrella()
    elif tipo == "Anillo":
        return dibujar_topologia_anillo()
    elif tipo == "Bus":
        return dibujar_topologia_bus()
    elif tipo == "Malla":
        return dibujar_topologia_malla()
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
    speak(mensaje, st.session_state.voice_type, st.session_state.speed)

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
        speak("Correcto. Ganaste 10 puntos.", st.session_state.voice_type, st.session_state.speed)
    else:
        st.session_state.feedback = f"❌ Incorrecto. Respuesta: {pregunta['respuesta']}"
        st.session_state.correcta = False
        speak(f"Incorrecto. La respuesta correcta es: {pregunta['respuesta']}", st.session_state.voice_type, st.session_state.speed)
    st.session_state.indice += 1
    st.rerun()

# ==================== MASCOTA ANIMADA ====================
st.markdown(f"""
<div class="mascota-container" id="mascota">
    <div style="font-size: 55px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 50%; padding: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
        🦊
    </div>
    <div class="mascota-speech" id="mascota-speech">
        {st.session_state.mensaje_mascota}
    </div>
</div>
""", unsafe_allow_html=True)

col_mascota1, col_mascota2, col_mascota3 = st.columns([1,1,8])
with col_mascota1:
    if st.button("🦊", key="btn_mascota", help="¡Haz clic para que la mascota te hable!"):
        hablar_mascota()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div style="text-align:center; margin-bottom:20px;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942783.png", width=70)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Configuración")
    
    voice_opts = ["👨 Hombre","👩 Mujer","🧒 Niño","👧 Niña"]
    sel = st.selectbox("🎤 Voz", voice_opts, index=voice_opts.index(st.session_state.voice_type) if st.session_state.voice_type in voice_opts else 0)
    st.session_state.voice_type = sel
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
    st.caption("Proyecto educativo de Redes de Computadoras (Redes II) que integra un chat basado en Inteligencia Artificial con tecnología de Groq para apoyar el aprendizaje interactivo de los estudiantes.Developed by Joswii")
    st.markdown('</div>', unsafe_allow_html=True)
    

# ==================== TABS PRINCIPALES ====================
st.markdown('<h1 class="premium-title">🌐 REDES II Y TELECOMUNICACIONES</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; margin-bottom:30px;">✨ INGENIERIA DE SISTEMAS UAP ✨</p>', unsafe_allow_html=True)

tabs = st.tabs(["📝 Quiz de Redes", "💬 Chat Inteligente", "🔧 Laboratorio de Redes", "🤖 IA con Claude"])

# -------------------- TAB 1: QUIZ --------------------
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col_inicio1, col_inicio2, col_inicio3 = st.columns([1,2,1])
    with col_inicio2:
        if st.button("🎉 Mensaje de Bienvenida", use_container_width=True):
            st.balloons()
            speak("INGENIERIA DE SISTEMAS UNIVERSIDAD AMAZONICA DE PANDO.", st.session_state.voice_type, st.session_state.speed)
    
    st.markdown("### 📡 Elige tu área de conocimiento")
    
    areas_con_iconos = {
        "Conceptos básicos de redes": "🌐",
        "Modelo OSI": "🥧",
        "Direccionamiento IPv4": "🔢",
        "Subneteo y máscaras": "✂️",
        "Dispositivos y comandos": "🖥️",
        "Cables y conexiones": "🔌",
        "Inteligencia Artificial Claude AI": "🤖",  # nuevo ícono
        "Seguridad, DHCP, VLAN, NAT": "🛡️",
    }
    
    cols = st.columns(4)
    for i, (area, icono) in enumerate(areas_con_iconos.items()):
        with cols[i % 4]:
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
                speak(texto, st.session_state.voice_type, st.session_state.speed)
            
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
    
    # Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Entrada de voz
    st.markdown("### 🎤 Dictado por voz")
    texto_voz = speech_to_text(
        language='es',
        start_prompt="🎙️ Presiona para hablar",
        stop_prompt="⏹️ Detener",
        key='mic_recorder_chat'
    )
    if texto_voz and texto_voz != st.session_state.input_text:
        st.session_state.input_text = texto_voz
    
    # Entrada de texto
    user_text = st.text_area(
        "Escribe tu consulta:",
        value=st.session_state.input_text,
        height=80,
        label_visibility="collapsed",
        placeholder="Ejemplo: ¿Qué es una dirección IP?"
    )
    
    if st.button("🚀 Enviar mensaje", type="primary", use_container_width=True):
        if user_text.strip():
            st.session_state.messages.append({"role": "user", "content": user_text.strip()})
            st.session_state.input_text = ""
            st.rerun()
    
    # Procesar respuesta
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
                    speak(respuesta, st.session_state.voice_type, st.session_state.speed)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
                respuesta = "Lo siento, hubo un error temporal. Por favor, intenta de nuevo."
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- TAB 3: LABORATORIO MEJORADO --------------------
with tabs[2]:
    st.markdown("## 🔧 Laboratorio de Redes")
    st.markdown("Herramientas interactivas para aprender y simular conceptos de redes")
    
    # ==================== SECCIÓN 1: TOPOLOGÍAS ====================
    st.markdown('<div class="section-title">📡 Topologías de Red Interactivas</div>', unsafe_allow_html=True)
    
    # Tarjeta para topologías
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col_top1, col_top2, col_top3, col_top4 = st.columns(4)
    with col_top1:
        st.markdown("""
        <div style="text-align:center; padding:15px; background:rgba(59,130,246,0.1); border-radius:16px; margin:5px;">
            <div style="font-size:2.5rem;">⭐</div>
            <div style="font-weight:600;">Estrella</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Visualizar Estrella", key="top_estrella", use_container_width=True):
            st.session_state.topologia_actual = "Estrella"
            speak("Mostrando topología en estrella", st.session_state.voice_type, st.session_state.speed)
    
    with col_top2:
        st.markdown("""
        <div style="text-align:center; padding:15px; background:rgba(139,92,246,0.1); border-radius:16px; margin:5px;">
            <div style="font-size:2.5rem;">🔄</div>
            <div style="font-weight:600;">Anillo</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Visualizar Anillo", key="top_anillo", use_container_width=True):
            st.session_state.topologia_actual = "Anillo"
            speak("Mostrando topología en anillo", st.session_state.voice_type, st.session_state.speed)
    
    with col_top3:
        st.markdown("""
        <div style="text-align:center; padding:15px; background:rgba(16,185,129,0.1); border-radius:16px; margin:5px;">
            <div style="font-size:2.5rem;">📏</div>
            <div style="font-weight:600;">Bus</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Visualizar Bus", key="top_bus", use_container_width=True):
            st.session_state.topologia_actual = "Bus"
            speak("Mostrando topología en bus", st.session_state.voice_type, st.session_state.speed)
    
    with col_top4:
        st.markdown("""
        <div style="text-align:center; padding:15px; background:rgba(245,158,11,0.1); border-radius:16px; margin:5px;">
            <div style="font-size:2.5rem;">🔗</div>
            <div style="font-weight:600;">Malla</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Visualizar Malla", key="top_malla", use_container_width=True):
            st.session_state.topologia_actual = "Malla"
            speak("Mostrando topología en malla", st.session_state.voice_type, st.session_state.speed)
    
    if st.session_state.topologia_actual:
        st.markdown("---")
        fig = iniciar_topologia(st.session_state.topologia_actual)
        if fig:
            st.pyplot(fig)
        
        detalles_topologias = {
            "Estrella": {
                "desc": "Todos los dispositivos se conectan a un switch o hub central.",
                "ventajas": "✅ Si un cable falla, solo ese dispositivo se desconecta\n✅ Fácil de instalar y administrar\n✅ Centralización de recursos",
                "desventajas": "❌ Si el switch central falla, toda la red falla\n❌ Mayor cantidad de cable que en Bus"
            },
            "Anillo": {
                "desc": "Cada dispositivo se conecta a otros dos formando un círculo. Los datos viajan en una dirección.",
                "ventajas": "✅ Organizada y predecible\n✅ No requiere dispositivo central\n✅ Rendimiento uniforme",
                "desventajas": "❌ Si un dispositivo falla, puede interrumpir toda la red\n❌ Difícil de diagnosticar fallas"
            },
            "Bus": {
                "desc": "Todos los dispositivos comparten un único cable llamado bus.",
                "ventajas": "✅ Poco cable, económica\n✅ Fácil de instalar\n✅ Ideal para redes pequeñas",
                "desventajas": "❌ Si el cable principal falla, toda la red falla\n❌ Muchas colisiones de datos\n❌ Bajo rendimiento con muchos dispositivos"
            },
            "Malla": {
                "desc": "Cada dispositivo se conecta a muchos otros, creando redundancia.",
                "ventajas": "✅ Alta confiabilidad (rutas alternativas)\n✅ Tolerante a fallos\n✅ Privacidad y seguridad",
                "desventajas": "❌ Muy costosa (mucho cable)\n❌ Difícil de instalar y mantener\n❌ Compleja de administrar"
            }
        }
        
        detalle = detalles_topologias.get(st.session_state.topologia_actual, {})
        
        col_desc1, col_desc2 = st.columns(2)
        with col_desc1:
            st.markdown(f"""
            <div style="background: rgba(59,130,246,0.1); border-radius:16px; padding:15px;">
                <b>📖 Descripción</b><br>{detalle.get('desc', '')}
            </div>
            """, unsafe_allow_html=True)
        with col_desc2:
            st.markdown(f"""
            <div style="background: rgba(16,185,129,0.1); border-radius:16px; padding:15px;">
                <b>✅ Ventajas</b><br>{detalle.get('ventajas', '').replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(239,68,68,0.1); border-radius:16px; padding:15px; margin-top:10px;">
            <b>❌ Desventajas</b><br>{detalle.get('desventajas', '').replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== SECCIÓN 2: HERRAMIENTAS DE RED ====================
    st.markdown('<div class="section-title">🛠️ Herramientas de Diagnóstico</div>', unsafe_allow_html=True)
    
    col_herramienta1, col_herramienta2 = st.columns(2)
    
    with col_herramienta1:
        # Ping mejorado
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        simulador_ping("8.8.8.8")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_herramienta2:
        # Calculadora de subredes mejorada (sin tabla)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧮 Calculadora de Subredes Avanzada")
        st.markdown("Calcula información detallada de una dirección IP con CIDR")
        
        ip_input = st.text_input("📝 Dirección IP con CIDR", placeholder="Ejemplo: 192.168.1.0/24", key="ip_calc")
        
        if ip_input:
            try:
                red = ipaddress.ip_network(ip_input, strict=False)
                
                # Mostrar resultados en tarjetas
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.markdown(f"""
                    <div style="background:rgba(59,130,246,0.15); border-radius:12px; padding:12px; margin:5px 0;">
                        <span style="color:#60a5fa;">🌐 Red</span><br>
                        <b style="font-size:1.1rem;">{red.network_address}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background:rgba(139,92,246,0.15); border-radius:12px; padding:12px; margin:5px 0;">
                        <span style="color:#a78bfa;">🎭 Broadcast</span><br>
                        <b style="font-size:1.1rem;">{red.broadcast_address}</b>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown(f"""
                    <div style="background:rgba(16,185,129,0.15); border-radius:12px; padding:12px; margin:5px 0;">
                        <span style="color:#34d399;">🔢 Máscara</span><br>
                        <b style="font-size:1.1rem;">{red.netmask}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background:rgba(245,158,11,0.15); border-radius:12px; padding:12px; margin:5px 0;">
                        <span style="color:#fbbf24;">💻 Hosts útiles</span><br>
                        <b style="font-size:1.1rem;">{red.num_addresses - 2}</b>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); border-radius:12px; padding:12px; margin-top:10px;">
                    <span style="color:#94a3b8;">📌 Rango de direcciones utilizables</span><br>
                    <b>{red[1]} → {red[-2]}</b>
                </div>
                """, unsafe_allow_html=True)
                
                # Información de clase
                primera_ip = int(str(red.network_address).split('.')[0])
                if 1 <= primera_ip <= 126:
                    clase = "A (Redes grandes)"
                    mascara_defecto = "255.0.0.0"
                elif 128 <= primera_ip <= 191:
                    clase = "B (Redes medianas)"
                    mascara_defecto = "255.255.0.0"
                elif 192 <= primera_ip <= 223:
                    clase = "C (Redes pequeñas)"
                    mascara_defecto = "255.255.255.0"
                else:
                    clase = "Especial (Multicast/Reservada)"
                    mascara_defecto = "N/A"
                
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); border-radius:12px; padding:10px; margin-top:10px; font-size:0.85rem;">
                    <b>📊 Información adicional:</b><br>
                    • Clase IP: {clase}<br>
                    • Máscara por defecto: {mascara_defecto}<br>
                    • CIDR: /{red.prefixlen}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("❌ Formato inválido. Usa formato como: 192.168.1.0/24")
        
        st.markdown("---")
        
        # Tabla de referencia rápida de CIDR
        with st.expander("📚 Tabla de referencia CIDR rápida"):
            st.markdown("""
            | CIDR | Máscara | Hosts útiles | Uso típico |
            |------|---------|--------------|------------|
            | /24 | 255.255.255.0 | 254 | Redes pequeñas (LAN típica) |
            | /25 | 255.255.255.128 | 126 | Media red clase C |
            | /26 | 255.255.255.192 | 62 | Subred pequeña |
            | /27 | 255.255.255.224 | 30 | Red muy pequeña |
            | /28 | 255.255.255.240 | 14 | Segmento pequeño |
            | /29 | 255.255.255.248 | 6 | Enlaces punto a punto |
            | /30 | 255.255.255.252 | 2 | Enlaces router-router |
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== SECCIÓN 3: TRACEROUTE ====================
    st.markdown('<div class="section-title">🗺️ Análisis de Ruta (Traceroute)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_trace1, col_trace2 = st.columns([3,1])
    with col_trace1:
        dom = st.text_input("🌐 Dominio o IP para rastrear", "google.com", key="trace_domain")
    with col_trace2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Iniciar Traceroute", use_container_width=True):
            simulador_traceroute(dom)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== SECCIÓN 4: COMPONENTES DE RED ====================
    st.markdown('<div class="section-title">🖧 Componentes de Red</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    componentes_data = {
        "🖥️ Tarjeta de Red (NIC)": "Permite conectar un dispositivo a la red. Cada NIC tiene una dirección MAC única.",
        "🔌 Conector RJ45": "Conector estándar para cables UTP/Cat. Tiene 8 pines para transmisión de datos.",
        "🔄 Switch": "Conecta dispositivos en una misma red. Usa direcciones MAC para enviar datos al destino correcto.",
        "🌐 Router": "Conecta redes diferentes y enruta paquetes IP. Permite el acceso a Internet.",
        "📡 Access Point": "Proporciona conectividad WiFi a dispositivos inalámbricos en la red.",
        "🔌 Cable UTP/FTP": "Par trenzado sin/blindaje. Categorías: Cat5e (1Gbps), Cat6 (10Gbps).",
        "💡 Fibra Óptica": "Utiliza pulsos de luz para transmitir datos. Larga distancia e inmunidad a interferencias.",
        "🛡️ Firewall": "Filtra el tráfico según reglas de seguridad. Protege la red de accesos no autorizados.",
        "🗄️ Servidor": "Ofrece servicios a los clientes: DHCP, DNS, web, correo, archivos.",
        "🚪 Gateway": "Puerta de enlace que permite salir de la red local hacia otras redes o Internet.",
        "⚡ PoE": "Power over Ethernet - Alimentación eléctrica a través del cable de red.",
        "📊 Módem": "Convierte señales digitales a analógicas para conexión al ISP."
    }
    
    # Mostrar componentes en 3 columnas
    componentes_items = list(componentes_data.items())
    for i in range(0, len(componentes_items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(componentes_items):
                nombre, desc = componentes_items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="component-card" style="height: 100%;">
                        <b style="font-size:1rem;">{nombre}</b>
                        <p style="color:#94a3b8; font-size:0.8rem; margin-top:8px;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 4: IA CON CLAUDE (infografía elegante) ====================
with tabs[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🤖 Inteligencia Artificial: Claude AI")
    st.markdown("Conoce a Claude, el asistente de IA desarrollado por **Anthropic** con un enfoque en ser **útil, honesto y inofensivo**.")
    
    # Infografía con columnas
    col_info1, col_info2 = st.columns([2, 1])
    with col_info1:
        st.markdown("""
        <div style="background: rgba(59,130,246,0.1); border-radius: 20px; padding: 1.5rem;">
            <h3 style="margin-top:0;">✨ ¿Qué es Claude?</h3>
            <p>Claude es un modelo de lenguaje grande (LLM) creado por Anthropic. Su objetivo principal es ser un asistente conversacional <strong>seguro, confiable y alineado con los valores humanos</strong>. A diferencia de otros modelos, Claude fue entrenado usando <strong>IA Constitucional</strong>, un método que le permite seguir principios éticos claros.</p>
            <h3>🎯 Características destacadas</h3>
            <ul>
                <li><strong>Ventana de contexto</strong> de hasta 200,000 tokens (puede procesar libros enteros).</li>
                <li><strong>Razonamiento avanzado</strong> en matemáticas, programación y análisis.</li>
                <li><strong>Capacidad multilingüe</strong> (incluye español perfecto).</li>
                <li><strong>Generación de código</strong> en Python, JavaScript, Java, C++, etc.</li>
                <li><strong>Análisis de documentos</strong> (PDF, TXT, CSV) y resúmenes.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_info2:
        st.image("https://www.anthropic.com/_next/static/media/claude-icon.2e8e6c8c.svg", width=180)
        st.markdown("""
        <div style="background: rgba(139,92,246,0.1); border-radius: 20px; padding: 1rem; text-align: center; margin-top: 1rem;">
            <span style="font-size: 3rem;">🧠</span><br>
            <b>IA Constitucional</b><br>
            <small>Entrenada con principios éticos para reducir sesgos y comportamientos dañinos.</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla de versiones
    st.markdown("### 📈 Evolución de Claude")
    st.markdown("""
    | Versión | Lanzamiento | Capacidad de contexto | Características principales |
    |---------|-------------|----------------------|-----------------------------|
    | Claude 1 | 2021 (beta) | 9k tokens | Primer asistente conversacional de Anthropic |
    | Claude 2 | Julio 2023 | 100k tokens | Mejora en razonamiento, programación y matemáticas |
    | Claude 2.1 | Nov 2023 | 200k tokens | Reducción de alucinaciones, llamadas a funciones |
    | Claude 3 (Haiku/Sonnet/Opus) | Mar 2024 | 200k tokens | Velocidad extrema, respuestas casi instantáneas, visión (imágenes) |
    """)
    
    st.markdown("---")
    
    # Beneficios por profesión
    st.markdown("### 🚀 Aplicaciones prácticas de Claude")
    col_ben1, col_ben2, col_ben3 = st.columns(3)
    with col_ben1:
        st.markdown("""
        <div style="background: rgba(16,185,129,0.1); border-radius: 16px; padding: 1rem; height: 100%;">
            <h4>👩‍🎓 Estudiantes</h4>
            <ul>
                <li>Explicaciones personalizadas</li>
                <li>Resúmenes de textos largos</li>
                <li>Ayuda con ejercicios</li>
                <li>Preparación para exámenes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_ben2:
        st.markdown("""
        <div style="background: rgba(245,158,11,0.1); border-radius: 16px; padding: 1rem; height: 100%;">
            <h4>👩‍🏫 Docentes</h4>
            <ul>
                <li>Creación de planes de clase</li>
                <li>Generación de material didáctico</li>
                <li>Evaluaciones y rúbricas</li>
                <li>Ideas para proyectos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_ben3:
        st.markdown("""
        <div style="background: rgba(59,130,246,0.1); border-radius: 16px; padding: 1rem; height: 100%;">
            <h4>💻 Programadores</h4>
            <ul>
                <li>Depuración de código</li>
                <li>Documentación automática</li>
                <li>Refactorización</li>
                <li>Explicación de algoritmos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cita y enlace
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2)); border-radius: 20px; padding: 1.5rem; text-align: center;">
        <i>"La inteligencia artificial debe ser útil, honesta e inofensiva. Ese es el núcleo del enfoque de Anthropic con Claude."</i><br>
        — Equipo de Anthropic
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🔗 **Más información:** [anthropic.com/claude](https://www.anthropic.com/claude)")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); padding: 20px; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05); margin-top: 20px;">
    <p style="color: #94a3b8; font-size: 0.85rem;">🌐 Proyecto de enseñanza y aprendizaje - Fundamentos de redes de computadoras</p>
    <p style="color: #64748b; font-size: 0.75rem;">Desarrollado con Claude.AI - Quiz interactivo + Chat con IA Groq + Laboratorio de redes</p>
</div>
""", unsafe_allow_html=True)
