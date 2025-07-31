
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Double Slit Simulation – RCE Theory", layout="wide")

# Intro section
st.title("Double Slit Experiment – Classical vs Relational Coherence Interpretation")
st.markdown("""
This interactive simulation illustrates the iconic double slit experiment under different interpretative frameworks:

- **Classical (Instrumentalist)**: Treats the quantum wavefunction as a computational tool without deep ontological commitment.
- **Relational Coherence Engine (RCE)**: A novel interpretation based on **contextual actualization** of relations between nodes (states), where outcomes emerge via coherent paths.

This app was created to demonstrate the theory presented in the scientific paper: *Actualization of Reality through Contextual Coherence: Foundations of a Relational Physics without Fixed Ontology*.
""")

# Sidebar configuration
st.sidebar.header("Experiment Parameters")
num_particles = st.sidebar.slider("Number of particles", 100, 10000, 3000, step=100)
noise_level = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.1)
slit_left_open = st.sidebar.checkbox("Left slit open", value=True)
slit_right_open = st.sidebar.checkbox("Right slit open", value=True)
interpretation = st.sidebar.radio("Interpretation model", ["Classical (Instrumentalist)", "RCE (Relational Coherence)"])

# Double slit simulation
def simulate_double_slit(n, noise, left_open=True, right_open=True, mode="classical"):
    screen = np.zeros(1000)
    positions = np.linspace(-1, 1, 1000)

    for _ in range(n):
        if not (left_open or right_open):
            continue

        if left_open and right_open:
            phase = np.pi * np.random.rand()
            if mode == "rce":
                p = np.cos(5 * positions + phase)**2 + noise * np.random.rand(len(positions))
            else:
                p = np.sin(10 * positions + phase)**2 + noise * np.random.rand(len(positions))
        elif left_open:
            p = np.exp(-((positions + 0.3)**2) / 0.01)
        elif right_open:
            p = np.exp(-((positions - 0.3)**2) / 0.01)

        p = p / np.sum(p)
        index = np.random.choice(range(1000), p=p)
        screen[index] += 1

    return positions, screen

positions, screen = simulate_double_slit(num_particles, noise_level, slit_left_open, slit_right_open, "rce" if "RCE" in interpretation else "classical")

# Plot the result
fig, ax = plt.subplots()
ax.plot(positions, screen)
ax.set_title(f"Detection Pattern – {interpretation}")
ax.set_xlabel("Screen position")
ax.set_ylabel("Hits")
st.pyplot(fig)

# Coherence Graph (RCE only)
if "RCE" in interpretation:
    st.markdown("### RCE – Coherence Graph")
    G = nx.DiGraph()
    G.add_nodes_from(["Source", "Left slit", "Right slit", "Hit (left)", "Hit (right)", "Interference"])

    edges = [("Source", "Left slit"), ("Source", "Right slit"),
             ("Left slit", "Hit (left)"), ("Right slit", "Hit (right)"),
             ("Source", "Interference")]

    pos = {
        "Source": (0, 0), "Left slit": (-1, -1), "Right slit": (1, -1),
        "Hit (left)": (-1.5, -2), "Hit (right)": (1.5, -2), "Interference": (0, 1)
    }

    G.add_edges_from(edges)

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes],
        y=[pos[node][1] for node in G.nodes],
        text=list(G.nodes),
        mode="markers+text",
        textposition="bottom center",
        marker=dict(size=30, color="lightblue"),
        hoverinfo="text"
    )

    edge_trace = go.Scatter(
        x=sum([[pos[edge[0]][0], pos[edge[1]][0], None] for edge in edges], []),
        y=sum([[pos[edge[0]][1], pos[edge[1]][1], None] for edge in edges], []),
        mode="lines",
        line=dict(width=2, color="gray"),
        hoverinfo="none"
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Relational Coherence Graph", showlegend=False, margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

# Reference section
st.markdown("""
---  
#### 📘 References
- Relational Coherence Theory: `https://github.com/yourname/rce-fentes`
- Author: **IKAMI**, contact: `ikami.research@proton.me`
""")
