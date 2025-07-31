import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- Graph builder for relational structure ---
def build_graph(context):
    G = nx.DiGraph()
    G.add_node("Source")

    if context == "Left slit open":
        G.add_node("Left slit")
        G.add_node("Impact on screen (left)")
        G.add_edge("Source", "Left slit")
        G.add_edge("Left slit", "Impact on screen (left)")
    elif context == "Right slit open":
        G.add_node("Right slit")
        G.add_node("Impact on screen (right)")
        G.add_edge("Source", "Right slit")
        G.add_edge("Right slit", "Impact on screen (right)")
    elif context == "Both slits open":
        G.add_node("Both slits")
        G.add_node("Interference pattern")
        G.add_edge("Source", "Both slits")
        G.add_edge("Both slits", "Interference pattern")
    
    return G

# --- App setup ---
st.set_page_config(page_title="Double-slit: RCE vs Quantum", layout="wide")
st.title("🧪 Double-slit Experiment — Standard Quantum vs RCE Interpretation")

st.markdown("""
This interactive simulation compares the **standard quantum interpretation** of the double-slit experiment  
with a new approach based on **Relational Coherence** (RCE), as proposed in a novel theoretical framework.  

🔗 *[A link to the full paper will be provided here later]*  
""")

# --- Step 1: Choose experimental context ---
st.markdown("### 1. Choose experimental setup (context):")

context_choice = st.radio("Which slit(s) are open?",
                          ["Left slit open", "Right slit open", "Both slits open"])

st.divider()

# --- Step 2: Compare interpretations ---
st.markdown("### 2. Compare interpretations of the outcome:")

col1, col2 = st.columns(2)

# Left: Standard Quantum Mechanics
with col1:
    st.subheader("🎓 Standard Quantum Mechanics")
    if context_choice == "Both slits open":
        st.markdown("""
        - The particle is considered in a **superposition of paths**.
        - It behaves like a **probability wave** interfering with itself.
        - The result is an **interference pattern**.
        """)
        st.warning("But this raises the paradox: how does a particle interfere with itself?")
    else:
        st.success("Only one slit open → particle travels a clear path.\n\nOutcome is localized.")

# Right: RCE – Relational Interpretation
with col2:
    st.subheader("🧠 RCE – Relational Coherence Engine")
    if context_choice == "Both slits open":
        st.markdown("""
        - No individual path is actualized.
        - The context activates a **relational structure** where multiple outcomes are linked.
        - The interference pattern arises from **logical coherence**, not physical duality.
        """)
        st.success("No hidden wave or collapse is required — coherence replaces superposition.")
    else:
        st.markdown("""
        - The context selects **one coherent branch**.
        - The outcome emerges logically, without assuming any underlying state.
        """)
        st.success("Classical behavior reinterpreted as a relationally actualized path.")

st.divider()

# --- Step 3: Visualize the RCE graph ---
st.markdown("### 3. Visualize the relational coherence graph:")

G = build_graph(context_choice)
fig, ax = plt.subplots(figsize=(8, 5))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, arrows=True, ax=ax)
st.pyplot(fig)

# --- Final explanation ---
st.info("""
🧩 In this framework, **reality doesn't pre-exist** the context — it **emerges** through the selection of a logically coherent branch  
within a potential structure (the graph). This avoids paradoxes like self-interference, superpositions, or collapse.

👉 This is a simplified simulation. The full mathematical formulation is available in the upcoming paper.
""")
