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

# Appliquer les styles
imda.apply_styles()

# Titre principal 
st.markdown('<p class="big-font">🧹 Préparation et nettoyage des données</p>', unsafe_allow_html=True)


# Chargement des Données

st.markdown('<p class="medium-font"><b>Données initiales:</b></p>', unsafe_allow_html=True)

#st.subheader("Données initiales")

st.markdown("""
    <p class='small-font'>
    Le fichier principal Eco2Mix Régional contient les données consolidées et définitives de la consommation d'énergie par Région de janvier 2013 à janvier 2023 au pas de 30 minutes
    Nous avons chargé ce dataset et il a été appelé df
    </p>
    """, unsafe_allow_html=True)



# Import de df
df = imda.import_df() 

# Affiche un aperçu des données initiales
st.write("Aperçu des données initiales Eco2Mix Régional consolidées:")
#st.dataframe(df.head())  # Montre les premières lignes pour validation


#  boutons du dataset 

if st.button("Afficher les premières lignes du dataset df"):
    st.dataframe(df.head())
    
if st.button("Afficher les dernières lignes du dataset df"):
    st.dataframe(df.tail())

if st.button("Afficher les dimensions du dataset df"):
    st.write(df.shape)    
    
if st.button("Afficher les colonnes et types du dataset df"):
    st.write(df.dtypes)

st.markdown("""
    <p class='small-font'>
    Le fichier secondaire Eco2Mix temps réel contient les données de février 2023 à septembre 2024 au pas de 15 minutes
    Nous avons chargé ce dataset et il a été appelé df2
    </p>
    """, unsafe_allow_html=True)


# Import df2
df2 = imda.import_df2() 

# Affiche un aperçu des données initiales
st.write('Aperçu des données initiales Eco2Mix Régional "temps réel"')
#st.dataframe(df2.head())  # Montre les premières lignes pour validation


#  boutons du dataset 
if st.button("Afficher les premières lignes du dataset"):
    st.dataframe(df2.head())
    
if st.button("Afficher les dernières lignes du dataset"):
    st.dataframe(df2.tail())

    
if st.button("Afficher les dimensions du dataset"):
    st.write(df2.shape)    
    
if st.button("Afficher les colonnes et types du dataset"):
    st.write(df2.dtypes)

