import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from utils import import_data as imda
from utils.import_data import couleurs_regions
from utils.import_data import data_2021
from utils.import_data import data_nationale
from utils.import_data import prepare_data_by_region


# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Appliquer les styles
imda.apply_styles()

# IMPORTATION DU DATASET df_energie
df_energie = imda.get_df_energie()  
df_pourcentages = imda.get_pourcentages_france()

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
    
    with st.expander("Phasage entre consommation et production en 2021"):
        # Appel de la fonction pour obtenir le graphique de consommation et production
        fig_nationale = data_nationale(df_energie)  # Obtenir le graphique
        st.plotly_chart(fig_nationale)  # Afficher le graphique de consommation et production
    

    
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
    with st.expander("Cartes de consommation et production par région en 2021"):
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
    df_2021 = imda.data_2021(df_energie)  # Obtenir df_2021
    df_pourcentages = imda.get_pourcentages_france()
    df_source = prepare_data_by_region(df_2021)

    fig1 = imda.create_fig_1(df_pourcentages)
    st.plotly_chart(fig1)

    #  expander pour la deuxième ligne de graphiques
    with st.expander("Type de source d'energie par région en 2021"):
    
        fig5 = imda.create_fig5(df_2021)  # Créer le graphique
        st.plotly_chart(fig5)  # Afficher le graphique
    
    with st.expander("Type de source d'energie renouvelables par région en 2021"):
        
        fig_histogram = imda.create_histogram(df_source)
        st.plotly_chart(fig_histogram)  # Affichez l'histogramme
        