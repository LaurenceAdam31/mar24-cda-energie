import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from utils import import_data as imda
from utils.import_data import couleurs_regions
from utils.import_data import data_2021


# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Appliquer les styles
imda.apply_styles()

# IMPORTATION DU DATASET df_energie
df_energie = imda.get_df_energie()  



# MODIFICATION DES DONNÉES
df_conso_prod = imda.get_df_conso_prod(df_energie)  # Récupérer les données agrégées

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">📊 Visualisations</p>', unsafe_allow_html=True)

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Graphiques")
pages = ["Visualisation Nationale", "Visualisation Régionale", "Sources d'énergie"]
page = st.sidebar.radio("Aller vers", pages)

# SWITCH SUR LA PAGE DE VISUALISATION
if page == "Visualisation Nationale":
    st.markdown('<p class="medium-font"><b>Au niveau National</b></p>', unsafe_allow_html=True)
    # Appeler les fonctions de visualisation pour la page nationale
    imda.test_bernard(df_energie)
    imda.data_2021(df_energie)  # Visualisation des données de 2021

elif page == "Visualisation Régionale":
    st.markdown('<p class="medium-font"><b>Au niveau Régional</b></p>', unsafe_allow_html=True)

    # IMPORTATION DU DATASET df_energie
    df_energie = imda.get_df_energie() 
    
    # Filtrer les données à partir de l'année 2015 pour le graphique Plotly
    df_anim = df_energie[df_energie["Annee"] > 2014].sort_values(by="Annee")
    
    # Affichage du graphique Plotly
    fig = imda.create_box_plot(df_anim)  # Appel de la fonction via imda
    st.plotly_chart(fig) 

    # Filtrer les données à partir de l'année 2021
    df_2021 = df_energie[df_energie["Annee"] == 2021]

    # Premier expander pour la première ligne de graphiques
    with st.expander("Afficher les cartes de consommation et production par région en 2021"):
        # Créer deux colonnes pour la première ligne
        col1, col2 = st.columns(2)

        # Carte de consommation par région dans la première colonne
        with col1:
            st.write('**CARTE DE LA CONSOMMATION PAR RÉGION EN 2021**')
            carte_conso = imda.create_map(df_2021, "Consommation (MW)", "Consommation (MW)", "Blues", "Consommation (MW)")
            st_folium(carte_conso)

        # Carte de production par région dans la deuxième colonne
        with col2:
            st.write('**CARTE DE LA PRODUCTION PAR RÉGION EN 2021**')
            carte_prod = imda.create_map(df_2021, "Production_totale (MW)", "Production_totale (MW)", "Reds", "Production Totale (MW)")
            st_folium(carte_prod)

    # Deuxième expander pour la deuxième ligne de graphiques
    with st.expander("Afficher les graphiques de phasage et de production en 2021"):

        fig4 = imda.create_fig4(df_2021)  # Créer le graphique
        st.plotly_chart(fig4)  # Afficher le graphique
            

            
elif page == "Sources d'énergie":
    st.markdown('<p class="medium-font"><b>Production 2021 par type de source d\'énergie</b></p>', unsafe_allow_html=True)
    
    # IMPORTATION DU DATASET df_energie
    df_energie = imda.get_df_energie()
    df_2021 = df_energie[df_energie["Annee"] == 2021]

    fig5 = imda.create_fig5(df_2021)  # Créer le graphique
    st.plotly_chart(fig5)  # Afficher le graphique
