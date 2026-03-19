# Copyright: (c) 2026 - Guillermo Roger Hernandez Chandia.
# Status: All Rights Reserved (Todos os Direitos Reservados).
# Contexto: Projeto acadêmico de Análise e Desenvolvimento de Sistemas (ADS).

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import random
import time
from collections import deque

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CYBER PLANET v15.0", layout="wide")

# --- ESTADOS DO SISTEMA (Session State) ---
if 'logs' not in st.session_state:
    st.session_state.logs = deque(["[NÚCLEO FINAL OPERACIONAL]..."], maxlen=20)
if 'contador' not in st.session_state:
    st.session_state.contador = 0
if 'alerta' not in st.session_state:
    st.session_state.alerta = False
if 'alerta_timer' not in st.session_state:
    st.session_state.alerta_timer = 0
if 'angulo_giro' not in st.session_state:
    st.session_state.angulo_giro = 0

# --- DESIGN NEON AVANÇADO ---
st.markdown("""
    <style>
    .main { background-color: #050a12; color: #00d4ff; font-family: 'Courier New', monospace; }
    .stMetric { border: 1px solid #00d4ff; background: rgba(0,212,255,0.1); border-radius: 10px; }
    .log-container {
        height: 450px; overflow-y: auto; border-left: 2px solid rgba(0,212,255,0.3); 
        padding-left: 20px; scrollbar-width: thin; scrollbar-color: #00d4ff #050a12;
    }
    h1 { text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR DE CONTROLE (Painel de Filtros) ---
st.sidebar.title("🛡️ CYBER CONTROL")
filtro_log = st.sidebar.selectbox(
    "Nível de Monitoramento:",
    ["Todos os Eventos", "Apenas Críticos (ALERTA)", "Apenas Tráfego (INFO)"]
)

if st.sidebar.button("Limpar Cache de Logs"):
    st.session_state.logs = deque(["[LOG REINICIADO]..."], maxlen=20)
    st.rerun()

st.title("⚡ NEURAL SENTINEL - SUPREME COMMAND")
placeholder = st.empty()

# Banco de Dados de Nós (Nodes)
map_nodes = {
    'Cidade': ['Tóquio', 'Londres', 'Nova York', 'São Paulo', 'Sydney', 'Paris', 'Moscou', 'Dubai'],
    'lat': [35.68, 51.50, 40.71, -23.55, -33.86, 48.85, 55.75, 25.20],
    'lon': [139.69, -0.12, -74.00, -46.63, 151.20, 2.35, 37.61, 55.27]
}

# --- LOOP DE EXECUÇÃO (Runtime) ---
while True:
    st.session_state.contador += 1
    st.session_state.angulo_giro = (st.session_state.angulo_giro + 3) % 360

    # Lógica de Backend: Geração de Dados
    idx_a, idx_o = random.sample(range(len(map_nodes['Cidade'])), 2)
    orig, alvo = map_nodes['Cidade'][idx_o], map_nodes['Cidade'][idx_a]

    # Probabilidade de Ataque (Pegadinha de Lógica: if/else encadeado)
    if random.random() > 0.88:
        st.session_state.alerta = True
        st.session_state.alerta_timer = 4
        st.session_state.ataque_coords = {
            'lat': [map_nodes['lat'][idx_o], map_nodes['lat'][idx_a]], 
            'lon': [map_nodes['lon'][idx_o], map_nodes['lon'][idx_a]]
        }
        st.session_state.logs.appendleft(f"[ALERTA] Invasão detectada: {orig} >> {alvo}")
    else:
        st.session_state.logs.appendleft(f"[INFO] Tráfego normal: {orig} >> {alvo}")

    if st.session_state.alerta_timer > 0: 
        st.session_state.alerta_timer -= 1
    else: 
        st.session_state.alerta = False

    color_sys = "#FF1744" if st.session_state.alerta else "#00d4ff"

    with placeholder.container():
        col_globe, col_txt = st.columns([2.5, 1]) 
        
        with col_globe:
            # Renderização do Globo 3D
            fig_map = px.scatter_geo(map_nodes, lat='lat', lon='lon', hover_name='Cidade', size=[70]*8, color_discrete_sequence=[color_sys])
            
            if st.session_state.alerta:
                fig_map.add_trace(go.Scattergeo(
                    lat=st.session_state.ataque_coords['lat'], 
                    lon=st.session_state.ataque_coords['lon'], 
                    mode='lines', 
                    line=dict(width=4, color='#FF1744')
                ))
            
            fig_map.update_geos(
                projection_type="orthographic", 
                projection_rotation=dict(lon=st.session_state.angulo_giro, lat=0, roll=0),
                showland=True, landcolor="#0b1424", showocean=True, oceancolor="#02050a",
                showcoastlines=True, coastlinecolor="#00d4ff"
            )
            fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin={"r":0,"t":0,"l":0,"b":0}, height=550, showlegend=False)
            st.plotly_chart(fig_map, use_container_width=True, key=f"map_{st.session_state.contador}")

        with col_txt:
            st.subheader("🛡️ NETWORK EVENT LOG")
            
            # --- FILTRAGEM DINÂMICA (UI Filter) ---
            logs_para_exibir = []
            for item in st.session_state.logs:
                if filtro_log == "Todos os Eventos":
                    logs_para_exibir.append(item)
                elif filtro_log == "Apenas Críticos (ALERTA)" and "[ALERTA]" in item:
                    logs_para_exibir.append(item)
                elif filtro_log == "Apenas Tráfego (INFO)" and "[INFO]" in item:
                    logs_para_exibir.append(item)

            log_html = "".join([f"<p style='color:{'#FF1744' if '[ALERTA]' in l else '#00d4ff'}; margin:2px;'>{l}</p>" for l in logs_para_exibir])
            st.markdown(f"<div class='log-container'>{log_html}</div>", unsafe_allow_html=True)

        # --- TELEMETRIA INFERIOR ---
        st.divider()
        cargas = [random.randint(15, 99) for _ in range(8)]
        fig_bar = go.Figure(data=[go.Bar(x=map_nodes['Cidade'], y=cargas, marker_color=[color_sys if c < 85 else "#FFF" for c in cargas])])
        fig_bar.update_layout(title="TELEMETRIA GLOBAL EM TEMPO REAL", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#00d4ff", height=200, margin={"t":30,"b":0})
        st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_{st.session_state.contador}")

    time.sleep(0.5)
