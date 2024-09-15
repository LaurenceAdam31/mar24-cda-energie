import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from utils import import_data as imda

# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie ", page_icon="🌟", layout="wide")

df_energie = pd.read_csv(r"df_energie.zip")

# CONVERSTION EN DATETIME
df_energie['Date'] = pd.to_datetime(df_energie['Date'], format='%Y-%m-%d')
df_energie['Heure'] = pd.to_datetime(df_energie['Heure'], format='%H:%M').dt.strftime('%H:%M')
df_energie['Date - Heure'] = pd.to_datetime(df_energie['Date - Heure'], utc=True)

# REMPLACEMENT DES VALEURS QUI NE SONT PAS CONVERTIBLES EN NaN
df_energie['Eolien (MW)'] = df_energie['Eolien (MW)'].replace(['', 'non-disponible'], np.nan)

# CONVERSION DE LA COLONNE EN FLOAT, SI PAS POSSSIBLE ALORS CONVERSION EN NaN
df_energie['Eolien (MW)'] = pd.to_numeric(df_energie['Eolien (MW)'], errors='coerce')

# SUPPRIMER LE RESTE
df_energie.dropna(subset=['Consommation (MW)'], axis=0, inplace=True)

# Agréger les données par année pour obtenir la consommation et la production totales
df_conso_prod = df_energie.groupby('Annee').agg({
    'Consommation (MW)': 'sum',
    'Production_totale (MW)': 'sum',
    'Total_NonRenouvelable (MW)': 'sum',
    'Total_Renouvelable (MW)': 'sum'
}).reset_index()

# Exclure les lignes où l'année est 2024
df_conso_prod = df_conso_prod[df_conso_prod['Annee'] != 2024]

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Graphiques")
pages = ["Visualisations 2021", "Visualisation Nationale", "Visualisation Régionale"]
page = st.sidebar.radio("Aller vers", pages)

# PRINT DES PAGES
if page == "Visualisations 2021":
    st.header("Visualisations 2021")
    imda.data_2021(df_energie)


# SWITCH SUR LA PAGE DATAVIZUALIZATION
elif page == "Visualisation Nationale":
    st.header("Visualisation Nationale")
    
    imda.data_nationale(df_energie)

elif page == "Visualisation Régionale":
    st.header("Visualisation Régionale")
    st.write("Section de modélisation :")
    # VOIR AVEC JESSICA LAURENCE ET VIRGINIE POUR DEFINIR LES BESOINS DE LA PAGE MODELISATION

# TODO FAIRE EN PLUS DES PETITS BOUTONS INTERACTIFS 
if st.button("Afficher les premières lignes du dataset"):
    st.dataframe(df_energie.head())

if st.button("Afficher les dernières lignes du dataset"):
    st.dataframe(df_energie.tail())

if st.button("Afficher les colonnes du dataset"):
    st.write(df_energie.columns)