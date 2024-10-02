import streamlit as st
import pandas as pd
import numpy as np
from utils import import_data as imda

#IMPORT DU FICHIER CONSOLIDE ECO2MIX REGIONAL
@st.cache_data
def import_df():
    df = pd.read_csv("eco2mix-regional-cons-def.csv.zip", compression='zip', sep=';')
    return df

#IMPORT DU FICHIER TEMPS REEL 
@st.cache_data
def import_df2():
    df2 = pd.read_csv("eco2mix-regional-tr(2).csv.zip", compression='zip', sep=';')
    return df2


# Titre de la page
st.title("Préprocessing")

# Chargement des Données
st.subheader("Données initiales")
st.write("""
    Le fichier principal Eco2Mix Régional : données consolidées et définitives de consommation d'énergie de de janvier 2013 à janvier 2023
""")

# Import de df
df = imda.import_df() 

# Affiche un aperçu des données initiales
st.write("Aperçu des données initiales Eco2Mix Régional consolidées:")
st.dataframe(df.head())  # Montre les premières lignes pour validation


# Création de deux colonnes pour les boutons du dataset 
col1, col2 = st.columns(2)

with col1:
    if st.button("Afficher les premières lignes du dataset df"):
        st.dataframe(df.head())
    
    if st.button("Afficher les dernières lignes du dataset df"):
        st.dataframe(df.tail())

with col2:
    
    if st.button("Afficher les dimensions du dataset df"):
        st.write(df.shape)    
    
    if st.button("Afficher les colonnes et types du dataset df"):
        st.write(df.dtypes)


# Import df2
df2 = imda.import_df2() 

# Affiche un aperçu des données initiales
st.write('Aperçu des données initiales Eco2Mix Régional "temps réel"')
st.dataframe(df2.head())  # Montre les premières lignes pour validation


# Création de deux colonnes pour les boutons du dataset 
col3, col4 = st.columns(2)

with col3:
    if st.button("Afficher les premières lignes du dataset"):
        st.dataframe(df2.head())
    
    if st.button("Afficher les dernières lignes du dataset"):
        st.dataframe(df2.tail())

with col4:
    
    if st.button("Afficher les dimensions du dataset"):
        st.write(df2.shape)    
    
    if st.button("Afficher les colonnes et types du dataset"):
        st.write(df2.dtypes)

