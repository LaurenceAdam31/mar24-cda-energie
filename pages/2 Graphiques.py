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

df_energie = imda.import_df("df_energie.zip")

# CONVERSTION EN DATETIME
df_energie, df_conso_prod = imda.modif_df(df_energie)

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Graphiques")
pages = ["Visualisation Nationale", "Visualisation Régionale"]
page = st.sidebar.radio("Aller vers", pages)

 

# SWITCH SUR LA PAGE DATAVIZUALIZATION
if page == "Visualisation Nationale":
    st.header("Visualisation Nationale")
    imda.data_2021(df_energie)

    imda.data_nationale(df_energie)

elif page == "Visualisation Régionale":
    st.header("Visualisation Régionale")
    st.write("Section de modélisation :")
  
