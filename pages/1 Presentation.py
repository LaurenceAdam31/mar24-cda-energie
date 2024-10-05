import streamlit as st
import pandas as pd
from utils import import_data as imda

# Fonction pour appliquer les styles CSS
def apply_styles():
    st.markdown("""
        <style>
        .big-font {
            font-size: 48px !important;
            font-family: system-ui;
            color: #2d3a64; /* Couleur personnalisée pour le titre */
        }
        .medium-font {
            font-size: 28px !important;
            font-family: system-ui;
            color: #2d3a64;
        }
        .small-font {
            font-size: 22px !important; 
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
<p class='medium-font'><b>Etapes du projet :</b></p>
<ul>
     <li style="font-size: 24px; font-family: system-ui;">Explorer, nettoyer et enrichir le jeu de données</li>
    <li style="font-size: 24px; font-family: system-ui;">Analyser l'évolution de la consommation et la production d'énergie au niveau national</li>
    <li style="font-size: 24px; font-family: system-ui;">Etudier les spécificités régionales</li>
    <li style="font-size: 24px; font-family: system-ui;">Expérimenter des modèles de machine learning pour réaliser des prévisions de consommation</li>
</ul>
""", unsafe_allow_html=True)

# Méthodologie
st.markdown("""
<p class='medium-font'><b>Afin de collaborer et de travailler en équipe nous avons :</b></p>
<ul>
    <li style="font-size: 24px; font-family: system-ui;">Mis en place un espace commun sur google drive</li>
    <li style="font-size: 24px; font-family: system-ui;">Utilisé google colab pour nos codes python</li>
    <li style="font-size: 24px; font-family: system-ui;">Communiqué régulièrement via slack</li>
    <li style="font-size: 24px; font-family: system-ui;">Travaillé collectivement sur steamlit via github</li>
""", unsafe_allow_html=True)
