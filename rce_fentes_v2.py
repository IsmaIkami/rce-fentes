
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

st.set_page_config(page_title="RCE – Fentes", layout="wide")
st.title("🧪 Expérience des fentes – Interprétation classique vs RCE")

st.markdown("Choisissez le **contexte expérimental** (fentes ouvertes) :")

context_choice = st.radio("Configuration des fentes :", 
                          ["Fente gauche ouverte", "Fente droite ouverte", "Les deux fentes ouvertes"])

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Physique quantique standard")
    if context_choice == "Les deux fentes ouvertes":
        st.markdown("""
        - Le système est en **superposition d'états**.
        - On parle d’**onde de probabilité** qui interfère avec elle-même.
        - Le paradoxe : pourquoi une particule interférerait-elle seule, sans interaction ?
        """)
        st.warning("Résultat : franges d’interférence observées
➡️ Mais interprétation reste floue (dualités, effondrement, ou multivers).")
    else:
        st.success("Une seule fente → trajectoire classique observée.
➡️ Comportement local interprété comme corpusculaire.")

with col2:
    st.subheader("🧠 Théorie relationnelle (RCE)")
    if context_choice == "Les deux fentes ouvertes":
        st.markdown("""
        - Aucune trajectoire définie n’est activée.
        - Le graphe de cohérence contient **plusieurs issues liées**, indissociables.
        - L’interférence est une **actualisation relationnelle**, non une dualité onde/particule.
        """)
        st.success("Résultat : la structure logique impose une configuration globale cohérente.
➡️ Pas besoin d’onde ni de superposition ontologique.")
    else:
        st.markdown("""
        - Le contexte (fente unique) impose une **branche logique unique**.
        - Pas de potentiel d’interférence, donc issue directe actualisée.
        """)
        st.success("Résultat : issue actualisée par la cohérence du contexte seul.
➡️ Comportement classique réinterprété logiquement.")

st.markdown("---")
st.subheader("🔗 Graphe de cohérence contextuelle (selon RCE)")

G = build_graph(context_choice)
fig, ax = plt.subplots(figsize=(8, 5))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, arrows=True, ax=ax)
st.pyplot(fig)

st.info("💡 Dans le paradigme relationnel, la réalité ne préexiste pas : elle s'actualise en fonction des contraintes de cohérence logique imposées par le contexte.")
