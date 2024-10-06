import streamlit as st
import pandas as pd
import numpy as np
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
            font-size: 35px !important;
            font-family: system-ui;
            color: #2d3a64;
        }
        .small-font {
            font-size: 20px !important; 
            font-family: system-ui;
        }
        </style>
    """, unsafe_allow_html=True)

# Appliquer les styles
apply_styles()

# Titre principal 
st.markdown('<p class="big-font">🧹 Préparation et nettoyage des données</p>', unsafe_allow_html=True)

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Jeux de données")
pages = ["Données utilisées", "Préprocessing"]
page = st.sidebar.radio("Aller vers", pages)

# Introduction générale au nettoyage des données
st.markdown("""
<p class='small-font'>
Cette section présente les différentes étapes de nettoyage des données avant de passer aux visualisations et modélisations. 
</p>
""", unsafe_allow_html=True)

# SWITCH SUR LA PAGE 1
if page == "Données utilisées":
    st.markdown('<p class="medium-font"><b>Données initiales:</b></p>', unsafe_allow_html=True)

    st.markdown("""
    <ul>
        <li class="small-font">
            <b>Dataset "<a href='https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/information/?disjunctive.libelle_region&disjunctive.nature' target='_blank'>Eco2mix Régional</a>" de janvier 2013 à janvier 2023</b>
            <br>
            Ce jeu de données contient des informations détaillées sur la consommation électrique régionale ainsi que la production par filière (nucléaire, éolien, solaire, etc.) pour chaque demi-heure. 
        </li>
    </ul>
    <br>
    <ul>
        <li class="small-font">
            <b>Données régionales "<a href='https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-tr/export/?disjunctive.libelle_region&disjunctive.nature' target='_blank'>Temps réel</a>" de février 2023 à septembre 2024</b>
            <br>
            Ce dataset en temps réel fournit les mêmes informations mais avec une granularité plus fine, toutes les 15 minutes.
        </li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="medium-font"><b>Données transformées:</b></p>', unsafe_allow_html=True)

    # IMPORTATION DU DATASET df_energie
    df_energie = imda.get_df_energie()  
        # Trier le DataFrame par la colonne 'date' dans l'ordre décroissant
    df_energie = df_energie.sort_values(by='Date', ascending=True)


    # BOUTONS INTERACTIFS 
    if st.button("dimensions du dataset df_energie"):
        st.write(df_energie.shape)
        
    if st.button("Afficher les premières lignes du dataset"):
        st.dataframe(df_energie.head())

    if st.button("Afficher les dernières lignes du dataset"):
        st.dataframe(df_energie.tail())

    if st.button("Afficher les colonnes et types du dataset"):
        st.write(df_energie.dtypes)
        
    date_min = df_energie['Date'].min()
    date_max = df_energie['Date'].max()
    
    
    st.markdown('<p class="medium-font"><b>Dataframes utilisés pour les modelisation:</b></p>', unsafe_allow_html=True)
# Chargement des DataFrames
    df_group = imda.get_df_group(df_energie.copy())  # Charge df_group depuis 
    st.markdown('<p class="small-font"><b>Au niveau régional :</b></p>', unsafe_allow_html=True)

    st.dataframe(df_group.head())
    
    st.markdown('<p class="small-font"><b>Au niveau national :</b></p>', unsafe_allow_html=True)
    conso = imda.get_conso(df_energie)  # Charge conso depuis CSV

    st.dataframe(conso.head())


# SWITCH SUR LA PAGE 2
if page == "Préprocessing":
    st.markdown('<p class="medium-font"><b>Nettoyage des données:</b></p>', unsafe_allow_html=True)

    # Sous-sections
    st.markdown('<p class="small-font"><b>Transformations sur les variables :</b></p>', unsafe_allow_html=True)
    
    st.markdown("""
        <ul>
            <li class="small-font">Convertir les colonnes de date et heure en format <code>datetime</code>.</li>
            <li class="small-font">Remplacer les valeurs non convertibles par <code>NaN</code>.</li>
            <li class="small-font">Transformer la colonne 'code INSEE Région' en type string.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    with st.expander("", expanded=False):
        st.code("""
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    df['Heure'] = pd.to_datetime(df['Heure'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
    df['Date - Heure'] = pd.to_datetime(df['Date - Heure'], utc=True, errors='coerce')
    df['Code INSEE région'] = df['Code INSEE région'].astype(str).apply(lambda x: f"{int(x)}")
        """, language='python')
        
    st.markdown('<p class="small-font"><b>Réduction de la fréquence des mesures :</b></p>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="small-font">Suppression des mesures prises toutes les 30 min (Eco2Mix Régional)
            ou toutes les 15 min (Eco2Mix temps-réel) pour éviter de multiplier par 2 ou 4 la consommation lors de l'agrégation en MWh.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    with st.expander("", expanded=False):
        st.code("""
    # Supprimer les lignes ou minutes = 30
    df.drop(df[df['Date - Heure'].dt.minute == 30].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Filtrer et supprimer les lignes où les minutes sont 30, 15 ou 45
    df2.drop(df2[(df2['Date - Heure'].dt.minute == 30) |
                  (df2['Date - Heure'].dt.minute == 15) |
                  (df2['Date - Heure'].dt.minute == 45)].index, inplace=True)
    df2.reset_index(drop=True, inplace=True)
        """, language='python')
    

    st.markdown('<p class="small-font"><b>Suppression des lignes et colonnes inutiles :</b></p>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="small-font">Supprimer lignes où la consommation n'est pas renseignée.</li>
            <li class="small-font">Supprimer les colonnes contenant plus de 79% de valeurs manquantes. 
        <ul>
        """, unsafe_allow_html=True)

    
    with st.expander("", expanded=False):
        st.code("""
    # Supprimer les 11 premières lignes où la conso n'est pas renseignée
    df.dropna(subset=['Consommation (MW)'], axis=0, inplace=True)
    
    # Suppression des colonnes non étudiées ainsi que [éolien terrestre] et [éolien offshore] vides avant 2021
    columns_to_drop = [
    'TCO Thermique (%)', 'TCH Thermique (%)',
    'TCO Nucléaire (%)', 'TCH Nucléaire (%)', 'TCO Eolien (%)', 'TCH Eolien (%)',
    'TCO Solaire (%)', 'TCH Solaire (%)', 'TCO Hydraulique (%)', 'TCH Hydraulique (%)',
    'TCO Bioénergies (%)', 'TCH Bioénergies (%)', 'Column 30',
    'Stockage batterie', 'Déstockage batterie', 'Eolien terrestre', 'Eolien offshore']
    
    df = df.drop(columns=columns_to_drop, errors='ignore')
        """, language='python')
        
        

    st.markdown('<p class="small-font"><b>Remplacement des valeurs <code>NAN</code> par zéro (absence de production) :</b></p>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="small-font"><b>Nucléaire</b> : Île-de-France, Pays de la Loire, Provence-Alpes-Côte d'Azur, Bourgogne-Franche-Comté, Bretagne</li>
            <li class="small-font"><b>Pompage</b> : Centre-Val de Loire, Île-de-France, Pays de la Loire, Normandie, Hauts-de-France, Nouvelle-Aquitaine</li>
            <li class="small-font"><b>Éolien</b> : Île-de-France, Centre-Val de Loire</li>
        </ul>
        """, unsafe_allow_html=True)
    
    with st.expander("", expanded=False):
        st.code("""
    # REMPLACEMENT DES VALEURS MANQUANTES DANS CERTAINES COLONNES PAR 0
    df['Nucléaire (MW)'] = df['Nucléaire (MW)'].fillna(0)
    df['Pompage (MW)'] = df['Pompage (MW)'].fillna(0)
    
    # TRAITEMENT DE LA COLONNE 'Eolien (MW)'
    df['Eolien (MW)'] = df['Eolien (MW)'].replace(['', 'non-disponible'], np.nan)
    df['Eolien (MW)'] = pd.to_numeric(df['Eolien (MW)'], errors='coerce')  # Remplacer les erreurs par NaN
    df['Eolien (MW)'] = df['Eolien (MW)'].fillna(0)

        """, language='python')
    
    

    # Concaténation des deux datasets et ajouts de colonnes
    st.markdown('<p class="medium-font"><b>Fusion des datasets et ajouts de colonnes:</b></p>', unsafe_allow_html=True)

    st.markdown('<p class="small-font"><b>Fusion des datasets Eco2mix consolidé et Eco2mix temps réel:</b></p>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        st.code("""
        df_energie = pd.concat([df1, df_2], ignore_index=True)
        """, language='python')

    st.markdown('<p class="small-font"><b>Ajout de colonnes année et nom du mois en français:</b></p>', unsafe_allow_html=True)
 
    with st.expander("", expanded=False):
        st.code("""
        df_energie.loc[:, "Annee"] = df_energie["Date"].dt.year
        df_energie.loc[:, "Mois"] = df_energie["Date"].dt.month.map(month_name_fr).astype('string')
        """, language='python')

    st.markdown('<p class="small-font"><b>Création de colonnes "Production NonRenouvelable", "Production Renouvelable" et "Production totale":</b></p>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        st.code("""
        df_energie["Total_NonRenouvelable (MW)"] = df_energie[['Thermique (MW)', 'Nucléaire (MW)']].sum(axis=1)
        df_energie["Total_Renouvelable (MW)"] = df_energie[['Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Eolien (MW)']].sum(axis=1)
        df_energie["Production_totale (MW)"] = df_energie[["Total_NonRenouvelable (MW)", "Total_Renouvelable (MW)"]].sum(axis=1)
        """, language='python')
    


    # aGRÉGATION PAR MOIS
    st.markdown('<p class="medium-font"><b>Agrégation par périodes mensuelles:</b></p>', unsafe_allow_html=True)
    
    st.markdown('<p class="small-font"><b>Pour les modélisations nous avons agrégé les dates par périodes de 1 mois</b></p>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li class="small-font">En conservant les régions pour le modèle régional</li>
            <li class="small-font">En supprimant les régions pour le modèle national</li>
        <ul>
        """, unsafe_allow_html=True)

    
    with st.expander("", expanded=False):
        st.code("""
        # Ajout de la colonne 'PERIODE' dans df_energie
        ['PERIODE'] = df_energie['Date'].dt.to_period('M').astype(str)
        
        # Agrégation des données par période et Code INSEE région
        df_group = df_energie.groupby(['PERIODE', 'Code INSEE région']).agg({'Consommation (MW)': 'sum'}).reset_index()
        
        # Agrégation des données par période
        conso = df_energie.groupby('PERIODE').agg({'Consommation (MW)': 'sum'}).reset_index()

        # Convertir 'PERIODE' en datetime
        df_group['PERIODE'] = pd.to_datetime(df_group['PERIODE'])
        conso['PERIODE'] = pd.to_datetime(conso['PERIODE'])
    
        # Définir 'PERIODE' comme index
        df_group.set_index('PERIODE', inplace=True)
        conso.set_index('PERIODE', inplace=True)
        
        """, language='python')
    
        