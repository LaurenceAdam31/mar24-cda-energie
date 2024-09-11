import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

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
st.sidebar.title("Sommaire")
pages = ["Exploration des données", "DataVizualization", "Modélisation"]
page = st.sidebar.radio("Aller vers", pages)

# PRINT DES PAGES
if page == "Exploration des données":
    st.header("Exploration des données")
    st.write("Voici un aperçu des données :")
    st.dataframe(df_energie.head())
    st.write("Informations sur les types de données :")
    st.write(df_energie.info())
    st.write("Statistiques de base :")
    st.write(df_energie.describe())

# SWITCH SUR LA PAGE DATAVIZUALIZATION
elif page == "DataVizualization":
    st.header("DataVizualization")
    st.write("Visualisation des données :")

    # EXEMPLE HISTO
    if st.checkbox("Afficher l'histogramme de l'évolution de la consommation d'énergie"):
        fig = px.histogram(df_energie, x='Consommation (MW)', nbins=30, title='Distribution de la consommation d\'énergie')
        st.plotly_chart(fig)


    # EXEMPLE GRAPH LINE
    if st.checkbox("Afficher l'évolution de la consommation d'énergie au fil du temps"):
        fig = px.line(df_energie, x='Date - Heure', y='Consommation (MW)', title='Évolution de la consommation d\'énergie au fil du temps')
        st.plotly_chart(fig)

    # EXEMPLE PIE
    if st.checkbox("Afficher la répartition des sources d'énergie"):
        energy_sources = df_energie[['Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Bioénergies (MW)']].sum()
        fig = px.pie(values=energy_sources.values, names=energy_sources.index, title='Répartition des sources d\'énergie')
        st.plotly_chart(fig)

elif page == "Modélisation":
    st.header("Modélisation")
    st.write("Section de modélisation :")
    # VOIR AVEC JESSICA LAURENCE ET VIRGINIE POUR DEFINIR LES BESOINS DE LA PAGE MODELISATION

# # TODO FAIRE EN PLUS DES PETITS BOUTONS INTERACTIFS 
# if st.button("Afficher les premières lignes du dataset"):
#     st.dataframe(df_energie.head())

# if st.button("Afficher les dernières lignes du dataset"):
#     st.dataframe(df_energie.tail())

# if st.button("Afficher les colonnes du dataset"):
#     st.write(df_energie.columns)