import streamlit as st
import pandas as pd
import numpy as np
from utils import import_data as imda

# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Appliquer les styles
imda.apply_styles()

# IMPORTATION DU DATASET df_energie
df_energie = imda.get_df_energie()  

# MODIFICATION DES DONNÉES
df_conso_prod = imda.get_df_conso_prod()  # Récupérer les données agrégées

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Graphiques")
pages = ["Visualisation Nationale", "Visualisation Régionale"]
page = st.sidebar.radio("Aller vers", pages)

# SWITCH SUR LA PAGE DE VISUALISATION
if page == "Visualisation Nationale":
    st.markdown('<h2 class="custom-title">Visualisation Nationale</h2>', unsafe_allow_html=True)
    # Appeler les fonctions de visualisation pour la page nationale
    imda.data_2021(df_energie)  # Visualisation des données de 2021
    imda.data_nationale(df_energie)  # Visualisation nationale

elif page == "Visualisation Régionale":
    st.markdown('<h2 class="custom-title">Visualisation Régionale</h2>', unsafe_allow_html=True)
    st.write("Section de modélisation :")

# Afficher des boutons interactifs pour explorer le dataset
if st.button("Afficher les premières lignes du dataset d'énergie"):
    st.dataframe(df_energie.head())

if st.button("Afficher les dernières lignes du dataset d'énergie"):
    st.dataframe(df_energie.tail())

if st.button("Afficher les colonnes du dataset d'énergie"):
    st.write(df_energie.columns)

if st.button("Afficher les colonnes et types du dataset d'énergie"):
    st.write(df_energie.dtypes)
