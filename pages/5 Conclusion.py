import streamlit as st
import pandas as pd
from utils import import_data as imda

# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Appel de la fonction pour appliquer les styles
imda.apply_styles()

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">🏁 Conclusion</p>', unsafe_allow_html=True)

# Texte d'introduction
st.markdown('<p class="small-font">L\'exploration du jeu de données Eco2mix nous a permis de visualiser des éléments de tendance et d\'observer de très fortes disparités de consommation d’électricité entre les régions ainsi que l\'importance des variations saisonnières dans la modélisation de la consommation d’électricité.</p>', unsafe_allow_html=True)

# liste à puces
st.markdown("""
<p class='medium-font'><b>Pour aller plus loin, nous aurions pu :</b></p>
<ul>
    <li class="small-font">intégrer les variables exogènes au modèle(température, nombre de jours fériés dans la période)</li>
    <li class="small-font">Etudier les similitudes (températures, populations, habitat…) entre les régions prédites par le même modèle</li>
    <li class="small-font">Evaluer les stockages de batteries en France en lien avec le développement des besoins des véhicules électriques</li>
</ul>

""", unsafe_allow_html=True)

# liste à puces
st.markdown("""
<p class='medium-font'><b>Ce Projet nous a permis de :</b></p>
<ul>
    <li class="small-font">Nous confronter à la difficulté a été de se coordonner pour le travail en équipe à distance et de mener de front les sprints pour la formation.</li>
    <li class="small-font">Mettre en pratique nos nouvelles compétences en matière de nettoyage des données, de visualisation et de modélisation avec différentes bibliothèques Python. </li>
    <li class="small-font">Communiquer dans un climat serein et constructif, ce qui nous a permis d’obtenir des résultats beaucoup plus intéressants qu’en étant seul.</li>
</ul>

""", unsafe_allow_html=True)

st.markdown('<p class="small-font">Nous remercions toute l\'équipe de Datascientest et plus particulièrement Alain Ferlac pour son soutien, son accompagnement et son suivi. </p>', unsafe_allow_html=True)
