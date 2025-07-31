import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="Relational Coherence Engine – Double Slit Simulation")

# --- Intro page ---
st.title("🌌 Double Slit Experiment – Classical vs Relational Coherence")
st.markdown("""
Welcome to the interactive simulation of the **Double Slit Experiment** using a new paradigm called the **Relational Coherence Engine (RCE)**.

> This prototype illustrates how the **RCE model** offers an alternative **logical foundation** to understand quantum paradoxes – not by replacing quantum mechanics, but by reinterpreting it **without ontological collapse**.

---

### 🔑 Core Concepts of RCE

| Concept                      | Description |
|-----------------------------|-------------|
| **Relational Actualization** | Events become actual only when they are coherent with their relational context |
| **Coherence Graph**          | A dynamic graph links nodes (events, observations) via **coherence weights** μ ∈ [0,1] |
| **No Ontology, Only Relations** | Reality is not made of "particles", but **contextual actualizations** |
| **Measurement**             | Changes the coherence structure, but does not collapse reality – just reroutes activation |
| **μ value**                 | Represents contextual probability without assuming an underlying state |

---

### 🧮 Core Mathematical Notion

The coherence graph is defined as a directed weighted graph:

```math
G = (V, E, μ)\quad \text{with}\quad μ: E → [0,1]
```

And the **actualization path** A is defined as:

```math
A = \text{argmax}_{P \in \mathcal{P}} \left( \prod_{e \in P} μ(e) \right)
```

Where \( \mathcal{P} \) is the set of all coherent paths from Source to Detection.

--- 
""")

# --- Parameters ---
st.sidebar.header("🧪 Experiment Parameters")

num_particles = st.sidebar.slider("Number of particles", 100, 10000, 1000, step=100)
noise_level = st.sidebar.slider("Experimental noise level", 0.0, 1.0, 0.1, step=0.05)
left_slit_open = st.sidebar.checkbox("Left slit open", value=True)
right_slit_open = st.sidebar.checkbox("Right slit open", value=True)

model_choice = st.sidebar.radio("Interpretation mode", [
    "Classical (with collapse)",
    "RCE (Relational Coherence)",
    "Many Worlds (Everett)",
    "QBism (subjective Bayesian)"
], index=1)

# --- Core Simulation Logic ---
def simulate_hits(model, n, noise, left_open, right_open):
    x_hits = []

    for _ in range(n):
        if model == "Classical (with collapse)":
            if not (left_open or right_open):
                continue
            slit = np.random.choice(["L", "R"])
            if slit == "L" and left_open:
                x = np.random.normal(loc=-0.5, scale=0.3)
            elif slit == "R" and right_open:
                x = np.random.normal(loc=0.5, scale=0.3)
            else:
                continue
        elif model == "RCE (Relational Coherence)":
            if left_open and right_open:
                phase = np.random.uniform(0, 2*np.pi)
                x = np.sin(20 * phase) + np.random.normal(0, noise)
            elif left_open:
                x = np.random.normal(loc=-0.5, scale=0.3)
            elif right_open:
                x = np.random.normal(loc=0.5, scale=0.3)
            else:
                continue
        elif model == "Many Worlds (Everett)":
            x = np.random.uniform(-1, 1)
        elif model == "QBism (subjective Bayesian)":
            bias = np.random.beta(2, 5)
            x = np.random.normal(loc=bias - 0.5, scale=0.5)
        x_hits.append(x)
    return np.array(x_hits)

# --- Simulation ---
hits = simulate_hits(model_choice, num_particles, noise_level, left_slit_open, right_slit_open)
hist_vals, bins = np.histogram(hits, bins=50)

# --- Plotting ---
fig = go.Figure()
fig.add_trace(go.Bar(x=bins[:-1], y=hist_vals, marker_color='lightblue'))
fig.update_layout(title=f"Detection Screen – {model_choice}", xaxis_title="Position", yaxis_title="Count", height=400)

st.plotly_chart(fig, use_container_width=True)

# --- Coherence Graph for RCE ---
if model_choice == "RCE (Relational Coherence)":
    import networkx as nx
    import plotly.graph_objects as go

    G = nx.DiGraph()
    G.add_edges_from([
        ("Source", "Left slit", {"mu": 0.9}),
        ("Source", "Right slit", {"mu": 0.9}),
        ("Left slit", "Hit (left)", {"mu": 0.7}),
        ("Right slit", "Hit (right)", {"mu": 0.7}),
        ("Source", "Interference", {"mu": 0.3}),
        ("Interference", "Hit (left)", {"mu": 0.2}),
        ("Interference", "Hit (right)", {"mu": 0.2}),
    ])

    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x, node_y = zip(*[pos[node] for node in G.nodes()])
    node_labels = list(G.nodes())

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', marker=dict(size=20, color='lightblue'),
                            text=node_labels, textposition="bottom center")

    fig_graph = go.Figure(data=[edge_trace, node_trace])
    fig_graph.update_layout(title="RCE – Coherence Graph", showlegend=False, height=500)

    st.plotly_chart(fig_graph, use_container_width=True)