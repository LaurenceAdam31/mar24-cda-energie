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

df_energie = imda.import_df()

# CONVERSTION EN DATETIME
df_energie, df_conso_prod = imda.modif_df(df_energie)

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