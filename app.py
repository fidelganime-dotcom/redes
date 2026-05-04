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

# ---------- CONFIGURACIÓN STREAMLIT ----------
st.set_page_config(
    page_title="REDES BÁSICAS - TECNO KIDS", 
    page_icon="🌐", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CLIENTE GROQ ----------
# Usar secrets en producción, o la clave directa localmente
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
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

.medalla {
    font-size: 1.3rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.2));
    padding: 12px;
    border-radius: 60px;
    margin: 10px 0;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

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

@keyframes fadeInOut {
    0%, 100% { opacity: 0; transform: scale(0.9); }
    10%, 90% { opacity: 1; transform: scale(1); }
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

@media (max-width: 768px) {
    .premium-title { font-size: 1.8rem; }
    .section-title { font-size: 1.2rem; }
    .question-text { font-size: 1rem; }
}
</style>

<div class="watermark">🌐 REDES BÁSICAS</div>
"""

st.markdown(STYLES, unsafe_allow_html=True)

# ==================== BASE DE CONOCIMIENTO ====================
knowledge = {
    "¿qué es una red?": "Una red de computadoras es un conjunto de dispositivos conectados que comparten recursos e información.",
    "¿para qué sirve una red?": "Sirve para compartir datos, impresoras, internet, comunicarse entre dispositivos.",
    "diferencias entre lan y wan": "LAN es red local (corto alcance). WAN es red amplia (Internet).",
    "¿qué es el modelo osi?": "Modelo de 7 capas que estandariza la comunicación.",
    "capas del modelo osi": "1️⃣ Física, 2️⃣ Enlace, 3️⃣ Red, 4️⃣ Transporte, 5️⃣ Sesión, 6️⃣ Presentación, 7️⃣ Aplicación.",
    "¿qué es una dirección ipv4?": "Número único de 32 bits que identifica cada dispositivo.",
    "¿qué es un router?": "Dispositivo de capa 3 que conecta redes diferentes.",
    "¿qué es un switch?": "Dispositivo de capa 2 que conecta dispositivos en una misma red.",
    "¿qué es dhcp?": "Protocolo que asigna automáticamente direcciones IP.",
    "¿qué es vlan?": "Red virtual que separa el tráfico en capa 2.",
    "¿qué es nat?": "Traduce IPs privadas a públicas para acceder a Internet.",
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
    "Protocolos (ARP, ICMP, TCP)": [],
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
        ("¿Cuál es la red más grande del mundo?", ["Internet", "Intranet", "Extranet", "LAN"], "Internet"),
        ("¿Qué significa NIC?", ["Network Interface Card", "Network Internet Card", "New Interface Card", "Null Interface Card"], "Network Interface Card"),
    ]
    osi = [
        ("¿Cuántas capas tiene el modelo OSI?", ["7", "5", "4", "6"], "7"),
        ("¿Cuál es la capa 3 del modelo OSI?", ["Red", "Transporte", "Enlace", "Física"], "Red"),
        ("¿Qué capa se encarga del direccionamiento IP?", ["Red", "Transporte", "Aplicación", "Sesión"], "Red"),
        ("¿Qué capa usa direcciones MAC?", ["Enlace de Datos", "Red", "Física", "Transporte"], "Enlace de Datos"),
        ("¿Qué capa transmite bits?", ["Física", "Enlace", "Red", "Transporte"], "Física"),
    ]
    ipv4 = [
        ("¿Cuántos bits tiene IPv4?", ["32", "64", "128", "16"], "32"),
        ("¿Cuántos octetos tiene IPv4?", ["4", "3", "5", "6"], "4"),
        ("¿Rango de clase A?", ["1-126", "128-191", "192-223", "224-239"], "1-126"),
        ("¿Dirección de loopback?", ["127.0.0.1", "0.0.0.0", "255.255.255.255", "192.168.1.1"], "127.0.0.1"),
        ("¿Qué es IP privada?", ["No accesible desde Internet", "Accesible mundialmente", "Solo servidores", "IP de broadcast"], "No accesible desde Internet"),
    ]
    subnet = [
        ("¿Máscara /24?", ["255.255.255.0", "255.255.0.0", "255.0.0.0", "255.255.255.128"], "255.255.255.0"),
        ("¿Bits de host en /26?", ["6", "8", "2", "4"], "6"),
        ("¿Hosts por subred en /28?", ["14", "16", "30", "62"], "14"),
        ("¿Para qué subnetear?", ["Optimizar direcciones", "Aumentar velocidad", "Reducir colisiones", "Conectar redes"], "Optimizar direcciones"),
    ]
    dispositivos = [
        ("¿Qué conecta redes diferentes?", ["Router", "Switch", "Hub", "Bridge"], "Router"),
        ("¿Qué usa direcciones MAC?", ["Switch", "Router", "Gateway", "Repetidor"], "Switch"),
        ("¿Comando modo privilegiado Cisco?", ["enable", "config t", "interface", "show"], "enable"),
        ("¿Qué hace 'no shutdown'?", ["Activar interfaz", "Desactivar", "Borrar", "Reiniciar"], "Activar interfaz"),
    ]
    cables = [
        ("¿Conector UTP común?", ["RJ45", "BNC", "LC", "USB"], "RJ45"),
        ("¿Distancia máxima UTP?", ["100 m", "50 m", "200 m", "500 m"], "100 m"),
        ("¿Cable para dos PCs directo?", ["Crossover", "Directo", "Rollover", "Fibra"], "Crossover"),
        ("¿Cable PC a switch?", ["Directo", "Crossover", "Rollover", "Fibra"], "Directo"),
    ]
    protocolos = [
        ("¿Protocolo de ping?", ["ICMP", "TCP", "UDP", "ARP"], "ICMP"),
        ("¿Qué hace ARP?", ["Resuelve IP a MAC", "MAC a IP", "Asigna IP", "Enruta"], "Resuelve IP a MAC"),
        ("¿Qué significa TCP?", ["Transmission Control Protocol", "Transfer CP", "Transport CP", "Trunk CP"], "Transmission Control Protocol"),
        ("¿Qué significa UDP?", ["User Datagram Protocol", "Universal DP", "Unreliable DP", "Uniform DP"], "User Datagram Protocol"),
    ]
    seg_nat = [
        ("¿Qué hace DHCP?", ["Asigna IP automática", "Resuelve nombres", "Enruta", "Cifra"], "Asigna IP automática"),
        ("¿Qué significa NAT?", ["Network Address Translation", "Network Access Translation", "Network Address Table", "Network Automatic Translation"], "Network Address Translation"),
        ("¿Para qué sirve NAT?", ["IPs privadas a Internet", "Aumentar velocidad", "Cifrar", "Filtrar"], "IPs privadas a Internet"),
        ("¿Qué es VLAN?", ["Red virtual capa 2", "Red de área local", "VPN", "Red inalámbrica"], "Red virtual capa 2"),
    ]
    return cb, osi, ipv4, subnet, dispositivos, cables, protocolos, seg_nat

preguntas_quiz = []
areas_nombres = list(areas_quiz.keys())
bases = generar_preguntas()
for idx, base in enumerate(bases):
    for p in base:
        opciones_mezcladas = p[1].copy()
        respuesta_correcta = p[2]
        random.shuffle(opciones_mezcladas)
        preguntas_quiz.append({"area": areas_nombres[idx], "tipo": "multiple", "pregunta": p[0], "opciones": opciones_mezcladas, "respuesta": respuesta_correcta})

# ==================== FUNCIONES DE VOZ ====================
def speak(text, voice_type, speed="Normal"):
    # Función simplificada - no reproduce audio en la nube
    pass

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
        "🖥️ NIC": "Permite conectar un dispositivo a la red.",
        "🔌 RJ45": "Conector estándar para cables UTP.",
        "🔄 Switch": "Conecta dispositivos en una misma red.",
        "🌐 Router": "Conecta redes diferentes y enruta.",
        "📡 Access Point": "Proporciona conectividad WiFi.",
        "💡 Fibra óptica": "Larga distancia, inmunidad a interferencias.",
        "🛡️ Firewall": "Filtra tráfico según reglas de seguridad.",
        "🚪 Gateway": "Puerta de enlace a otras redes."
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
    st.session_state.mute_audio = True
    st.session_state.input_text = ""

mensajes_mascota = [
    "🌟 ¡Excelente! Sigue así, eres un genio de las redes.",
    "💡 Recuerda: cada gran experto fue una vez principiante.",
    "🎯 ¡Acertaste! La práctica hace al maestro.",
    "📚 ¿Sabías que las redes son el internet que usas a diario?",
    "🚀 ¡Vamos por más! El conocimiento es poder."
]

def hablar_mascota():
    mensaje = random.choice(mensajes_mascota)
    st.session_state.mensaje_mascota = mensaje

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
    else:
        st.session_state.feedback = f"❌ Incorrecto. Respuesta: {pregunta['respuesta']}"
        st.session_state.correcta = False
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
    sel = st.selectbox("🎤 Voz", voice_opts, index=0)
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
    st.caption("Proyecto educativo de Redes de Computadoras (Redes II) integra IA con Groq. Developed by Joswii")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TABS PRINCIPALES ====================
st.markdown('<h1 class="premium-title">🌐 REDES II Y TELECOMUNICACIONES</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8; margin-bottom:30px;">✨ INGENIERIA DE SISTEMAS UAP ✨</p>', unsafe_allow_html=True)

tabs = st.tabs(["📝 Quiz de Redes", "💬 Chat Inteligente", "🔧 Laboratorio de Redes"])

# -------------------- TAB 1: QUIZ --------------------
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col_inicio1, col_inicio2, col_inicio3 = st.columns([1,2,1])
    with col_inicio2:
        if st.button("🎉 Mensaje de Bienvenida", use_container_width=True):
            st.balloons()
    
    st.markdown("### 📡 Elige tu área de conocimiento")
    
    areas_con_iconos = {
        "Conceptos básicos de redes": "🌐",
        "Modelo OSI": "🥧",
        "Direccionamiento IPv4": "🔢",
        "Subneteo y máscaras": "✂️",
        "Dispositivos y comandos": "🖥️",
        "Cables y conexiones": "🔌",
        "Protocolos (ARP, ICMP, TCP)": "📡",
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
    
    col_clear, _ = st.columns(2)
    with col_clear:
        if st.button("🧹 Limpiar conversación", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
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
    
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("✨ Pensando..."):
            try:
                system_prompt = {
                    "role": "system",
                    "content": "Eres un asistente experto en redes de computadoras. Responde SIEMPRE de forma muy breve y concisa (máximo 2-3 oraciones). Ve directo al punto."
                }
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[system_prompt] + st.session_state.messages,
                    temperature=0.7,
                    max_tokens=150
                )
                respuesta = completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
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
    
    col_top1, col_top2, col_top3, col_top4 = st.columns(4)
    with col_top1:
        st.markdown("""<div style="text-align:center; padding:15px; background:rgba(59,130,246,0.1); border-radius:16px;"><div style="font-size:2.5rem;">⭐</div><div style="font-weight:600;">Estrella</div></div>""", unsafe_allow_html=True)
        if st.button("Visualizar Estrella", key="top_estrella", use_container_width=True):
            st.session_state.topologia_actual = "Estrella"
    with col_top2:
        st.markdown("""<div style="text-align:center; padding:15px; background:rgba(139,92,246,0.1); border-radius:16px;"><div style="font-size:2.5rem;">🔄</div><div style="font-weight:600;">Anillo</div></div>""", unsafe_allow_html=True)
        if st.button("Visualizar Anillo", key="top_anillo", use_container_width=True):
            st.session_state.topologia_actual = "Anillo"
    with col_top3:
        st.markdown("""<div style="text-align:center; padding:15px; background:rgba(16,185,129,0.1); border-radius:16px;"><div style="font-size:2.5rem;">📏</div><div style="font-weight:600;">Bus</div></div>""", unsafe_allow_html=True)
        if st.button("Visualizar Bus", key="top_bus", use_container_width=True):
            st.session_state.topologia_actual = "Bus"
    with col_top4:
        st.markdown("""<div style="text-align:center; padding:15px; background:rgba(245,158,11,0.1); border-radius:16px;"><div style="font-size:2.5rem;">🔗</div><div style="font-weight:600;">Malla</div></div>""", unsafe_allow_html=True)
        if st.button("Visualizar Malla", key="top_malla", use_container_width=True):
            st.session_state.topologia_actual = "Malla"
    
    if st.session_state.topologia_actual:
        st.markdown("---")
        fig = iniciar_topologia(st.session_state.topologia_actual)
        if fig:
            st.pyplot(fig)
        
        detalles = {
            "Estrella": "Todos los dispositivos se conectan a un switch central. Ventaja: si un cable falla, solo ese dispositivo se desconecta.",
            "Anillo": "Los dispositivos se conectan en círculo. Los datos viajan en una dirección.",
            "Bus": "Todos los dispositivos comparten un único cable. Es simple pero si el cable falla, toda la red falla.",
            "Malla": "Cada dispositivo se conecta a muchos otros. Alta confiabilidad pero mayor costo."
        }
        st.info(detalles.get(st.session_state.topologia_actual, ""))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🛠️ Herramientas de Diagnóstico</div>', unsafe_allow_html=True)
    
    col_herramienta1, col_herramienta2 = st.columns(2)
    with col_herramienta1:
        simulador_ping("8.8.8.8")
    with col_herramienta2:
        calculadora_subredes()
    
    st.markdown('<div class="section-title">🗺️ Análisis de Ruta</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_trace1, col_trace2 = st.columns([3,1])
    with col_trace1:
        dom = st.text_input("🌐 Dominio o IP para rastrear", "google.com", key="trace_domain")
    with col_trace2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Iniciar Traceroute", use_container_width=True):
            simulador_traceroute(dom)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🖧 Componentes de Red</div>', unsafe_allow_html=True)
    componentes_red()

st.markdown("---")
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); padding: 20px; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05); margin-top: 20px;">
    <p style="color: #94a3b8; font-size: 0.85rem;">🌐 Proyecto de enseñanza y aprendizaje - Fundamentos de redes de computadoras</p>
    <p style="color: #64748b; font-size: 0.75rem;">Desarrollado con IA - Quiz interactivo + Chat con IA Groq + Laboratorio de redes</p>
</div>
""", unsafe_allow_html=True)
