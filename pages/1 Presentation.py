import streamlit as st
import pandas as pd
from utils import import_data as imda

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

# Présentation du Jeu de données
st.markdown("""
<p class='medium-font'><b>Jeux de données utilisés :</b></p>
<ul>
     <li style="font-size: 24px; font-family: system-ui;">
         Dataset "<a href='https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/information/?disjunctive.libelle_region&disjunctive.nature' target='_blank'>Eco2mix Régional</a>" de janvier 2013 à janvier 2023
     </li>
    <li style="font-size: 24px; font-family: system-ui;">
        Données régionales "<a href='https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-tr/export/?disjunctive.libelle_region&disjunctive.nature' target='_blank'>Temps réel</a>" de février 2023 à juin 2024
    </li>
</ul>
""", unsafe_allow_html=True)

# IMPORTATION DU DATASET df_energie
df_energie = imda.get_df_energie()  

# TODO FAIRE EN PLUS DES PETITS BOUTONS INTERACTIFS 
if st.button("Afficher les premières lignes du dataset d'énergie"):
    st.dataframe(df_energie.head())

if st.button("Afficher les dernières lignes du dataset d'énergie"):
    st.dataframe(df_energie.tail())

if st.button("Afficher les colonnes du dataset d'énergie"):
    st.write(df_energie.columns)

if st.button("Afficher les colonnes et types du dataset d'énergie"):
    st.write(df_energie.dtypes)