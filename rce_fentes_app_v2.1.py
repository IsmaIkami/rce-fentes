
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(page_title="Double-slit Experiment – RCE vs Classical Interpretation", layout="wide")

# -- Introduction --
st.title("Double-slit Experiment Simulator")
st.markdown(
    """
    This interactive simulator allows you to visualize and compare the outcomes of the double-slit experiment
    under different interpretive frameworks:
    - **Classical Interpretation**: Events are determined independently and follow linear causality.
    - **Relational Coherence Engine (RCE)**: A new logical paradigm where coherence across contexts determines actualization.

    This project is part of the scientific initiative to promote **relational paradigms** as proposed by IKAMI (2025).
    """
)

# -- Sidebar parameters --
st.sidebar.header("Simulation Parameters")
particles = st.sidebar.slider("Number of particles emitted", 100, 10000, 3000, step=100)
noise = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.1, step=0.01)

st.sidebar.markdown("### Interpretation model")
model = st.sidebar.radio(
    "Choose interpretation",
    ("Classical Mechanics", "Relational Coherence (RCE)", "Many-Worlds", "Copenhagen", "QBism"),
    index=1
)

st.sidebar.markdown("---")
left_open = st.sidebar.checkbox("Left slit open", value=True)
right_open = st.sidebar.checkbox("Right slit open", value=True)
detector_on = st.sidebar.checkbox("Detector near slits (collapses wave?)", value=False)

# -- Generate particle hits --
x = np.linspace(-1, 1, 500)
if left_open and right_open:
    if model == "Classical Mechanics":
        y = 0.5 * (np.exp(-((x - 0.4) ** 2) * 100) + np.exp(-((x + 0.4) ** 2) * 100))
    elif model == "Relational Coherence (RCE)":
        y = np.cos(20 * x) ** 2 * np.exp(-x**2 * 5)
    else:  # other interpretations - simulate as wave collapse if detector on
        if detector_on:
            y = 0.5 * (np.exp(-((x - 0.4) ** 2) * 100) + np.exp(-((x + 0.4) ** 2) * 100))
        else:
            y = np.cos(20 * x) ** 2 * np.exp(-x**2 * 5)
elif left_open:
    y = np.exp(-((x + 0.4) ** 2) * 100)
elif right_open:
    y = np.exp(-((x - 0.4) ** 2) * 100)
else:
    y = np.zeros_like(x)

# Add noise
rng = np.random.default_rng()
y += noise * rng.normal(0, 0.05, size=y.shape)
y = np.clip(y, 0, None)

# -- Display Results --
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Particle Detection Pattern")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Hits'))
    fig.update_layout(
        xaxis_title="Screen position",
        yaxis_title="Detection count",
        height=400,
        margin=dict(l=10, r=10, t=30, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("RCE – Coherence Graph")
    G = nx.Graph()
    G.add_node("Source")
    if left_open:
        G.add_edge("Source", "Left slit")
        G.add_edge("Left slit", "Hit (left)")
    if right_open:
        G.add_edge("Source", "Right slit")
        G.add_edge("Right slit", "Hit (right)")
    if left_open and right_open and not detector_on and model == "Relational Coherence (RCE)":
        G.add_edge("Source", "Interference")
        G.add_edge("Interference", "Hit (left)")
        G.add_edge("Interference", "Hit (right)")

    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1), hoverinfo='none', mode='lines'))
    fig2.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                              marker=dict(size=30, color='lightblue'),
                              text=list(G.nodes()), textposition="bottom center"))
    fig2.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=10, r=10, t=30, b=30),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    st.plotly_chart(fig2, use_container_width=True)

# -- Result messages --
if y.max() < 0.01:
    st.warning("Résultat : aucun impact détecté. Les deux fentes sont fermées.")
elif "cos" in str(y):
    st.success("Résultat : motif d'interférence visible — cohérence relationnelle (RCE) en action.")
else:
    st.info("Résultat : pas de motif d'interférence — interprétation classique ou effondrement d'onde.")
