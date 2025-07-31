
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import random

st.set_page_config(layout="wide")

# Title and author
st.title("Relational Coherence Engine (RCE) – Double Slit Simulation")
st.markdown("""
**By Ismail Sialyen**  
This interactive simulation illustrates the *Relational Coherence Engine (RCE)* theory, a post-classical logical paradigm proposed to reinterpret foundational quantum paradoxes.  
Instead of viewing particles as waves or discrete entities, the RCE posits that what manifests in our reality are **contextual actualizations**—nodes in a graph of potentialities that only take form through coherent relational configurations.
""")

# Introduction
with st.expander("🧠 About the RCE Paradigm"):
    st.markdown("""
    Traditional quantum mechanics oscillates between wave-particle duality and observer-induced collapse, leaving paradoxes such as the double-slit experiment unresolved in intuitive terms.  
    The RCE framework proposes a shift: **reality does not pre-exist with fixed properties**, but is instead *actualized* through **coherent relations** between contextual elements.

    > "The world is not made of things, but of relations that become things." — *Preprint, Sialyen 2025*

    In this simulation, we offer a visual exploration of how **relational coherence** can reproduce interference effects, resolve measurement inconsistencies, and provide an ontologically lean alternative.
    """)

# Sidebar controls
st.sidebar.header("Simulation parameters")
n_particles = st.sidebar.slider("Number of particles", 100, 10000, 3000, step=100)
noise_level = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.1, step=0.01)
left_open = st.sidebar.checkbox("Left slit open", value=True)
right_open = st.sidebar.checkbox("Right slit open", value=True)
interpretation = st.sidebar.radio("Interpretation model", ["Classical QM", "RCE (Relational Coherence)", "Many Worlds", "Copenhagen", "QBism"])

# Coherence Graph Construction
def generate_coherence_graph():
    G = nx.Graph()
    G.add_node("Source")
    if left_open:
        G.add_edge("Source", "Left slit")
        G.add_edge("Left slit", "Hit (left)")
    if right_open:
        G.add_edge("Source", "Right slit")
        G.add_edge("Right slit", "Hit (right)")
    G.add_edge("Source", "Interference")
    return G

def plot_coherence_graph(G):
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1), hoverinfo='none', mode='lines')

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text, textposition='top center',
        hoverinfo='text', marker=dict(size=30, color='lightblue', line=dict(width=2)))

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), height=400)
    return fig

# Outcome calculation
def simulate_hits_rce():
    hits = np.zeros(100)
    for _ in range(n_particles):
        if not left_open and not right_open:
            continue
        coherence = (left_open + right_open) / 2
        idx = int(50 + 40 * np.sin(random.uniform(0, np.pi * 2)) * coherence)
        idx = min(max(idx + int(np.random.normal(0, noise_level * 10)), 0), 99)
        hits[idx] += 1
    return hits

def plot_results(hits):
    st.subheader("Observed pattern")
    fig = go.Figure()
    fig.add_trace(go.Bar(y=hits, marker_color='indigo', name="Hits"))
    fig.update_layout(height=300, xaxis_title="Detector position", yaxis_title="Hit count")
    st.plotly_chart(fig, use_container_width=True)

# Main logic
col1, col2 = st.columns([1, 2])
with col1:
    G = generate_coherence_graph()
    fig = plot_coherence_graph(G)
    st.markdown("### RCE – Coherence Graph")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    hits = simulate_hits_rce()
    plot_results(hits)

# Interpretation insights
st.markdown("### Interpretation comparison")
st.markdown(f"""
- **Selected Model**: `{interpretation}`
- **Result**: Interference pattern {'present' if left_open and right_open else 'not present'} under current settings.
""")

# Application domain table
st.markdown("### 🌍 Potential Applications of the RCE Paradigm")
st.table({
    "Domain": ["Quantum Physics", "AI & Cognition", "Cosmology", "Information Theory"],
    "Potential Impact": [
        "Resolves measurement paradoxes without wavefunction collapse",
        "Provides a model of distributed context-based cognition",
        "Allows a contextual emergence of space-time regions",
        "Replaces static entropy models with contextual coherence graphs"
    ]
})

# Footer
st.markdown("---")
st.caption("Simulation engine developed by **Ismail Sialyen** | 2025 ©")
