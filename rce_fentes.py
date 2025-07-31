import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(context):
    G = nx.DiGraph()
    G.add_node("Source")

    if context == "Fente gauche ouverte":
        G.add_node("Fente gauche ouverte")
        G.add_node("Impact sur l'écran (gauche)")
        G.add_edge("Source", "Fente gauche ouverte")
        G.add_edge("Fente gauche ouverte", "Impact sur l'écran (gauche)")
    elif context == "Fente droite ouverte":
        G.add_node("Fente droite ouverte")
        G.add_node("Impact sur l'écran (droite)")
        G.add_edge("Source", "Fente droite ouverte")
        G.add_edge("Fente droite ouverte", "Impact sur l'écran (droite)")
    elif context == "Les deux fentes ouvertes":
        G.add_node("Les deux fentes ouvertes")
        G.add_node("Interférence")
        G.add_edge("Source", "Les deux fentes ouvertes")
        G.add_edge("Les deux fentes ouvertes", "Interférence")
    
    return G

st.set_page_config(page_title="RCE – Simulation des fentes", layout="centered")
st.title("🧪 Simulation RCE – Expérience des fentes")

st.markdown("**Choisissez quelles fentes sont ouvertes :**")

context_choice = st.radio("Configuration :", 
                          ["Fente gauche ouverte", "Fente droite ouverte", "Les deux fentes ouvertes"])

G = build_graph(context_choice)

# Affichage du graphe
st.subheader("🔗 Graphe de cohérence contextuelle")
fig, ax = plt.subplots(figsize=(8, 5))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, arrows=True, ax=ax)
st.pyplot(fig)

# Explication textuelle
st.subheader("🧠 Résultat relationnel")
if context_choice == "Fente gauche ouverte":
    st.success("Une seule fente ouverte → trajectoire unique vers **impact gauche**.\n\nComportement classique.")
elif context_choice == "Fente droite ouverte":
    st.success("Une seule fente ouverte → trajectoire unique vers **impact droite**.\n\nComportement classique.")
elif context_choice == "Les deux fentes ouvertes":
    st.info("Deux fentes ouvertes → pas de trajectoire unique, mais **structure d’interférence**.\n\nRésultat **relationnel**, non réductible à un état préalable.")

st.markdown("---")
st.markdown("🔍 *Cette simulation illustre le fonctionnement du moteur relationnel RCE : la réalité ne préexiste pas, elle s’actualise par cohérence contextuelle.*")
