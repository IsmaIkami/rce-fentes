
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import networkx as nx

# --- Paramètres utilisateur ---
st.set_page_config(page_title="Double-Slit Simulator", layout="wide")
st.title("🧪 Double-Slit Experiment Simulator – Quantum vs RCE")

st.markdown("This professional simulator lets you explore how the double-slit behaves under standard quantum interpretation vs a relational logic engine (RCE).")

st.sidebar.header("🔧 Experimental setup")

# Fentes ouvertes
fente_gauche = st.sidebar.checkbox("Left slit open", value=True)
fente_droite = st.sidebar.checkbox("Right slit open", value=True)

# Détecteurs
detecteur_gauche = st.sidebar.checkbox("Detector at left slit")
detecteur_droite = st.sidebar.checkbox("Detector at right slit")

# Intensité du faisceau
intensite = st.sidebar.slider("Source intensity (particles)", 100, 10000, 3000, step=100)

# Présence de bruit
bruit = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.1, step=0.01)

# Mode d'interprétation
mode = st.sidebar.radio("Interpretation mode", ["Quantum Mechanics", "RCE (Relational Coherence)"])

# --- Génération des impacts (quantique) ---
def generate_interference(intensity, noise_level, both_slits, detector=False):
    x = np.linspace(-1, 1, 500)
    screen = np.zeros_like(x)

    if both_slits and not detector:
        # Interference pattern (sin^2)
        pattern = (np.sin(10 * x) ** 2)
        screen += pattern
    else:
        # Single-slit or collapsed wave
        screen += np.exp(-((x - 0.3)**2) * 20) * fente_droite
        screen += np.exp(-((x + 0.3)**2) * 20) * fente_gauche

    screen += np.random.normal(0, noise_level, size=x.shape)
    screen = np.maximum(0, screen)

    hits = np.random.choice(x, size=intensity, p=screen/screen.sum())
    return hits

# --- Visualisation 1 : Résultat sur écran (quantique) ---
def plot_distribution(hits, title):
    hist, bins = np.histogram(hits, bins=100, range=(-1, 1))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=(bins[:-1] + bins[1:]) / 2, y=hist, marker_color='blue'))
    fig.update_layout(title=title, xaxis_title="Screen position", yaxis_title="Count", height=400)
    return fig

# --- Visualisation 2 : Graphe relationnel (RCE) ---
def plot_rce_graph(left, right, detector_left, detector_right):
    G = nx.DiGraph()
    G.add_node("Source")

    if left:
        G.add_node("Left slit")
        if not detector_left:
            G.add_edge("Source", "Left slit")
            G.add_node("Hit (left)")
            G.add_edge("Left slit", "Hit (left)")

    if right:
        G.add_node("Right slit")
        if not detector_right:
            G.add_edge("Source", "Right slit")
            G.add_node("Hit (right)")
            G.add_edge("Right slit", "Hit (right)")

    if left and right and not (detector_left or detector_right):
        G.add_node("Interference")
        G.add_edge("Source", "Interference")

    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x, node_y = zip(*[pos[n] for n in G.nodes()])
    node_text = list(G.nodes())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y,
                             line=dict(width=1, color='gray'),
                             hoverinfo='none',
                             mode='lines'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y,
                             mode='markers+text',
                             marker=dict(size=40, color='skyblue'),
                             text=node_text,
                             textposition="top center"))
    fig.update_layout(title="RCE – Coherence Graph", height=400,
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

# --- Simulation ---
slits_open = fente_gauche + fente_droite
detecteurs_actifs = detecteur_gauche or detecteur_droite
both_slits = fente_gauche and fente_droite

# Quantum mode
if mode == "Quantum Mechanics":
    hits = generate_interference(intensite, bruit, both_slits, detecteurs_actifs)
    fig1 = plot_distribution(hits, "Quantum screen pattern")

# RCE mode
else:
    fig1 = plot_rce_graph(fente_gauche, fente_droite, detecteur_gauche, detecteur_droite)

# --- Affichage final ---
st.markdown("### 4. Results")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.markdown("📘 This simulation compares the standard quantum mechanical interpretation with a new logic-based relational model (RCE).")
