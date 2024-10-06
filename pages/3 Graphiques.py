import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
    # st.write("Section de modélisation :")
    # Titre pour "Étude au niveau Régional" avec style personnalisé
    st.markdown('<p class="medium-font"><b>Étude au niveau Régional</b></p>', unsafe_allow_html=True)

    # Analyse de la consommation d'énergie par région
    st.markdown("""
    <p class='medium-font'><b>Analyse de la consommation d'énergie par région (2015 - 2024) :</b></p>
    """, unsafe_allow_html=True)

                
    # IMPORTATION DU DATASET df_energie
    df_energie = imda.get_df_energie()  

    # Filtrer les données à partir de l'année 2015
    df_anim = df_energie[df_energie["Annee"] > 2014].sort_values(by="Annee")

    # Définir une couleur spécifique pour chaque région
    couleurs_regions = {
        'Île-de-France': '#1f77b4',   # Bleu
        'Auvergne-Rhône-Alpes': '#ff7f0e',   # Orange
        'Provence-Alpes-Côte d\'Azur': '#2ca02c',   # Vert
        'Bretagne': '#d62728',   # Rouge
        'Normandie': '#9467bd',   # Violet
        'Nouvelle-Aquitaine': '#8c564b',   # Marron
        'Occitanie': '#e377c2',   # Rose
        'Pays de la Loire': '#7f7f7f',   # Gris
        'Hauts-de-France': '#bcbd22',   # Vert clair
        'Grand Est': '#17becf',   # Bleu clair
        'Centre-Val de Loire': '#ffbb78',   # Jaune foncé
        'Bourgogne-Franche-Comté': '#f7b6d2'  # Rose clair
    }

    # Création du graphique de boîtes animées avec Plotly
    fig = px.box(df_anim,
                x="Région",
                y="Consommation (MW)",
                animation_frame="Annee",
                range_y=[0, 20000],
                color="Région",  # Utilisation de la colonne 'Région' pour la coloration
                color_discrete_map=couleurs_regions  # Application de la carte de couleur
                )

    # Mise à jour de la mise en page
    fig.update_layout(
        title="Consommation d'énergie par région de 2015 à 2024",
        xaxis_title="Région",
        yaxis_title="Consommation (MW)"
    )

    # Intégration du graphique dans Streamlit
    st.plotly_chart(fig)

# # Afficher des boutons interactifs pour explorer le dataset
# if st.button("Afficher les premières lignes du dataset d'énergie"):
#     st.dataframe(df_energie.head())

# if st.button("Afficher les dernières lignes du dataset d'énergie"):
#     st.dataframe(df_energie.tail())

# if st.button("Afficher les colonnes du dataset d'énergie"):
#     st.write(df_energie.columns)

# if st.button("Afficher les colonnes et types du dataset d'énergie"):
#     st.write(df_energie.dtypes)
