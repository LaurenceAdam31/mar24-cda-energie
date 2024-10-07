import streamlit as st
import pandas as pd
from utils import import_data as imda

# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Appel de la fonction pour appliquer les styles
imda.apply_styles()

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">🎯 Présentation du Projet</p>', unsafe_allow_html=True)

# Texte d'introduction
st.markdown('<p class="small-font">La gestion de la production et de la consommation d\'énergie est un défi majeur dans le contexte de la transition énergétique mondiale, pour répondre aux enjeux économiques et environnementaux.</p>', unsafe_allow_html=True)
# Objectifs avec liste à puces
st.markdown("""
<p class='medium-font'><b>Objectifs :</b></p>
<ul>
    <li class="small-font">Observer la consommation et la production d'énergie</li>
    <li class="small-font">En déduire une prévision de consommation</li>
</ul>
""", unsafe_allow_html=True)

# Etapes du Projet avec la classe small-font
st.markdown("""
<p class='medium-font'><b>Etapes du projet :</b></p>
<ul>
    <li class="small-font">Explorer, nettoyer et enrichir le jeu de données</li>
    <li class="small-font">Analyser l'évolution de la consommation et la production d'énergie au niveau national</li>
    <li class="small-font">Étudier les spécificités régionales</li>
    <li class="small-font">Expérimenter des modèles de machine learning pour réaliser des prévisions de consommation</li>
</ul>
""", unsafe_allow_html=True)

# Méthodologie avec la classe small-font
st.markdown("""
<p class='medium-font'><b>Collaboration et travail en équipe :</b></p>
<ul>
    <li class="small-font">Mise en place un espace commun sur google drive</li>
    <li class="small-font">Utilisation de google colab pour nos codes python</li>
    <li class="small-font">Communication régulièrement via Slack</li>
    <li class="small-font">Travail collectif sur Streamlit via GitHub</li>
</ul>
""", unsafe_allow_html=True)