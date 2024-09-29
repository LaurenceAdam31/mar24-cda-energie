import streamlit as st
import plotly.express as px
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

# Titre pour "Étude au niveau Régional" avec style personnalisé
st.markdown('<p class="medium-font"><b>Étude au niveau Régional</b></p>', unsafe_allow_html=True)

# Analyse de la consommation d'énergie par région
st.markdown("""
<p class='medium-font'><b>Analyse de la consommation d'énergie par région (2015 - 2024) :</b></p>
""", unsafe_allow_html=True)

            
# Chargement dataframe
df_energie = imda.import_df("df_energie.zip")

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
