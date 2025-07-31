
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import networkx as nx
import random

st.set_page_config(layout="wide")

# ---- Title and Attribution ----
st.title("Double-Slit Experiment Simulation")
st.subheader("A Comparative Framework: Classical View vs Relational Coherence Engine (RCE)")
st.markdown("""
This interactive simulation demonstrates different interpretations of the double-slit experiment.

**Developed by Ismail Sialyen**  
Based on the Relational Coherence Engine (RCE) theory — a post-classical paradigm proposing that quantum phenomena are not wave-particle dualities but **contextual actualizations**.

📄 Learn more: [Full Theory Link – Coming Soon]

---

### 🧠 Theoretical Overview

- **Standard View (Classical/Quantum)**: Events are governed by deterministic particles or probabilistic wave functions.
- **Relational Coherence View**: Events (detections, interference) emerge when a **threshold of contextual compatibility** between relations is met.

---

### 🔬 Potential Impacts of the RCE Framework

| Domain                        | Potential Contribution                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------|
| **Quantum Paradoxes**        | Resolves double-slit, EPR, and Schrödinger’s cat via contextual coherence              |
| **Artificial Intelligence**  | Enables contextual decision engines not based on fixed ontologies                     |
| **Quantum Computing**        | Offers new non-unitary logic basis for qubit coherence                                |
| **Cognitive Science**        | Models perception as actualization of compatible context patterns                      |
| **Cosmology**                | Explains structure emergence without assuming fixed particle states                    |

---    
""")

# ---- Sidebar Parameters ----
st.sidebar.title("Simulation Controls")
num_particles = st.sidebar.slider("Number of particles", 100, 10000, 3000)
noise_level = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.10)

model_choice = st.sidebar.radio("Interpretation mode", [
    "Classical / Quantum Mechanics",
    "Relational Coherence Engine (RCE)"
])

# ---- Simulation Core ----
def simulate_hits(model, noise):
    if model == "Classical / Quantum Mechanics":
        # interference pattern: central max + noise
        x = np.linspace(-1, 1, 1000)
        intensity = np.cos(5 * np.pi * x)**2
        intensity += np.random.normal(0, noise, size=1000)
    else:
        # coherence zones only where context aligns
        x = np.linspace(-1, 1, 1000)
        coherence = np.exp(-((x-0.3)**2)/0.02) + np.exp(-((x+0.3)**2)/0.02)
        intensity = coherence + np.random.normal(0, noise, size=1000)
    intensity = np.maximum(intensity, 0)
    return x, intensity

x, y = simulate_hits(model_choice, noise_level)

# ---- Display Plot ----
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Detection intensity'))
fig.update_layout(title="Observed pattern on detection screen",
                  xaxis_title="Position on screen",
                  yaxis_title="Detection intensity",
                  height=400)
st.plotly_chart(fig, use_container_width=True)

# ---- Optional Graph View of Coherence ----
if model_choice == "Relational Coherence Engine (RCE)":
    st.markdown("### RCE – Coherence Graph")
    G = nx.DiGraph()

    # Nodes with potential coherence
    G.add_node("Source")
    G.add_node("Left slit")
    G.add_node("Right slit")
    G.add_node("Hit (left)")
    G.add_node("Hit (right)")
    G.add_node("Interference")

    G.add_edges_from([
        ("Source", "Left slit"),
        ("Source", "Right slit"),
        ("Left slit", "Hit (left)"),
        ("Right slit", "Hit (right)"),
        ("Source", "Interference")
    ])

    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(G.nodes),
        textposition="bottom center",
        marker=dict(size=30, color='skyblue'),
        hoverinfo='text')

    coherence_fig = go.Figure(data=[edge_trace, node_trace],
                              layout=go.Layout(
                                  showlegend=False,
                                  hovermode='closest',
                                  margin=dict(b=20,l=5,r=5,t=40),
                                  xaxis=dict(showgrid=False, zeroline=False),
                                  yaxis=dict(showgrid=False, zeroline=False)))
    st.plotly_chart(coherence_fig, use_container_width=True)
