import streamlit as st

# Fonction pour appliquer les styles CSS
def apply_styles():
    st.markdown("""
        <style>
        .big-font {
            font-size: 50px !important;
            font-family: system-ui;
            color: #2d3a64; /* Couleur personnalisée pour le titre */
        }
        .medium-font {
            font-size: 30px !important;
            font-family: system-ui;
            color: #2d3a64;
        }
        .small-font {
            font-size: 24px !important; 
            font-family: system-ui;
        }
        </style>
    """, unsafe_allow_html=True)

# Appel de la fonction pour appliquer les styles
apply_styles()

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">🎯 Présentation du Projet</p>', unsafe_allow_html=True)

# Objectifs avec liste à puces
st.markdown("""
<p class='medium-font'><b>Objectifs :</b></p>
<ul>
    <li style="font-size: 24px; font-family: system-ui;">Observer la consommation et la production d'énergie</li>
    <li style="font-size: 24px; font-family: system-ui;">En déduire une prévision de consommation</li>
</ul>
""", unsafe_allow_html=True)

# Etapes du Projet
st.markdown("""
<p class='medium-font'><b>Méthodologie :</b></p>
<ul>
     <li style="font-size: 24px; font-family: system-ui;">Explorer, nettoyer et enrichir le jeu de données</li>
    <li style="font-size: 24px; font-family: system-ui;">Analyser l'évolution de la consommation et la production d'énergie au niveau national</li>
    <li style="font-size: 24px; font-family: system-ui;">Etudier les spécificités régionales</li>
    <li style="font-size: 24px; font-family: system-ui;">Expérimenter des modèles de machine learning pour réaliser des prévisions de consommation</li>
</ul>
""", unsafe_allow_html=True)

