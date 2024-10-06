import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import altair as alt
import os

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

# Liste des noms de mois en français
month_name_fr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
                 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

# Fonction pour exclure les périodes spécifiques
def exclude_period(dataframe, period_to_exclude='2024-10-01'):
    # Supprime la période spécifiée si elle est présente
    return dataframe.drop(pd.Timestamp(period_to_exclude), errors='ignore')

# Fonction pour charger le DataFrame df_energie à partir d'un fichier CSV compressé
@st.cache_data
def get_df_energie():
    df_energie = pd.read_csv("df_energie.zip", compression='zip')
    return df_energie

@st.cache_data
def get_df_group(df_energie):
    df_group = df_energie.groupby(['PERIODE', 'Code INSEE région']).agg({'Consommation (MW)': 'sum'}).reset_index()
    df_group['Code INSEE région'] = df_group['Code INSEE région'].astype(int)
    df_group['PERIODE'] = pd.to_datetime(df_group['PERIODE'])
    df_group.set_index('PERIODE', inplace=True)
    return exclude_period(df_group)

# Fonction pour obtenir conso
def get_conso(df_energie):
    conso = df_energie.groupby('PERIODE').agg({'Consommation (MW)': 'sum'}).reset_index()
    conso['PERIODE'] = pd.to_datetime(conso['PERIODE'])
    conso.set_index('PERIODE', inplace=True)
    return exclude_period(conso)

# Fonction pour obtenir df_conso_prod
def get_df_conso_prod(df_energie):
    df_conso_prod = df_energie.groupby('Annee').agg({
        'Consommation (MW)': 'sum',
        'Production_totale (MW)': 'sum',
        'Total_NonRenouvelable (MW)': 'sum',
        'Total_Renouvelable (MW)': 'sum'
    }).reset_index()
    df_conso_prod = df_conso_prod[df_conso_prod['Annee'] != 2024]
    return df_conso_prod



@st.cache_data
def create_fig_1(df):
    # Créer le camembert avec Plotly Express
    fig = px.pie(df, values='Pourcentage (%)', names='Type d\'énergie',
                title="Production d'énergie par type en France en 2021 en pourcentage")

    # Personnaliser les couleurs du camembert
    colors = ['#EF553B', '#636EFA', '#B6E880', '#FECB52', '#19D3F3', '#AB63FA', '#FFA15A', 'gray']
    fig.update_traces(marker=dict(colors=colors))


    # Ajouter un titre au centre
    fig.update_layout(title={
        'text': "Sources de production d'énergie en France en 2021",
        'y': 0.9,  # Ajuster la position verticale du titre
        'x': 0.5,   # Ajuster la position horizontale du titre
        'xanchor': 'center',  # Centrer le titre horizontalement
        'yanchor': 'top'      # Aligner le titre en haut
    })

    # Ajouter la légende en dessous du camembert
    fig.update_layout(
        legend=dict(
            orientation='h',  # Orientation horizontale de la légende
            font=dict(size=12, color='black')  # Police et couleur du texte de la légende
        )
    )

    # Définir la taille de la figure
    fig.update_layout(
        width=600,   # Largeur de la figure en pixels
        height=600   # Hauteur de la figure en pixels
    )

    fig.update_traces(
        textinfo='percent+label',  # Afficher les pourcentages et les labels
        textposition='inside',  # Positionner les textes à l'intérieur des segments
        marker=dict(line=dict(color='white', width=2))  # Ajouter une bordure blanche entre les segments pour plus de clarté
    )
    
    st.plotly_chart(fig)
    
@st.cache_data
def create_fig_2(df):
    # Création d'un camembert représentant en % la consommation d'énergie par Région
    fig = px.pie(df, values='Consommation (MW)', names='Région',
                    title=f"Consommation d'énergie par région en France pour l'année 2021")

    fig.update_layout(
        width=600,  # largeur en pixels
        height=600,  # hauteur en pixels
        legend=dict(
            orientation="h",  # 'h' horizontal
            # yanchor="bottom",  # ancrer en haut
            # y=1,  # place la légende à la hauteur du graphique
            # xanchor="left",  # ancrer à gauche
            # x=-0.3  # déplacer légèrement la légende vers la gauche
            font=dict(size=12, color='black')  # Police et couleur du texte de la légend
        )
    )

    # Afficher le camembert
    st.plotly_chart(fig)
    

# @st.cache_data
# def create_fig_3(df):
    # # Affichage cartes consommation par Région en 2021
    # #Position [latitude, longitude] sur laquelle est centrée la carte
    # location = [47, 1]

    # #Niveau de zoom initial :
    # #3-4 pour un continent, 5-6 pour un pays, 11-12 pour une ville
    # zoom = 6

    # #Style de la carte
    # tiles = 'cartodbpositron'

    # Carte = folium.Map(location = location,
    #                 zoom_start = zoom,
    #                 tiles = tiles)

    # json = pd.read_json('regions.geojson')

    # folium.Choropleth(
    #     geo_data='regions.geojson',
    #     name="choropleth",
    #     data=df,
    #     columns=['Région', "Consommation (MW)"],
    #     key_on="feature.properties.nom",
    #     fill_color="Blues",
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name="Consommation (MW)",
    # ).add_to(Carte)
    # st_folium(Carte)



def data_2021(data):
    df_energie = data

    col1, col2 = st.columns(2)

    #Création d'un dataframe qui somme la consommation et la production par région et par année
    df_source = df_energie.groupby(['Annee', 'Région'])[['Consommation (MW)','Thermique (MW)',	'Nucléaire (MW)',	'Eolien (MW)',	'Solaire (MW)',	'Hydraulique (MW)',	'Pompage (MW)',	'Bioénergies (MW)',	'Ech. physiques (MW)','Production_totale (MW)', 'Total_NonRenouvelable (MW)', 'Total_Renouvelable (MW)']].sum().reset_index()

    #Création d'un dataframe pour l'année de référence 2021
    df_2021 = df_source.loc[df_source["Annee"] == 2021]


    # Création du DataFrame avec vos données
    df_2021_france = pd.DataFrame({
        'Consommation (MW)': [468556569.0],
        'Thermique (MW)': [37535944.0],
        'Nucléaire (MW)': [360425725.0],
        'Eolien (MW)': [36867678.0],
        'Solaire (MW)': [13973688.0],
        'Hydraulique (MW)': [61306018.0],
        'Pompage (MW)': [-6035039.0],
        'Bioénergies (MW)': [10033910.0],
        'Ech. physiques (MW)': [-45483890.0],
        'Production_totale (MW)': [514107924.0],
        'Total_NonRenouvelable (MW)': [397961669.0],
        'Total_Renouvelable (MW)': [116146255.0]
    })

    # Extraire la production totale
    production_totale = df_2021_france["Production_totale (MW)"].iloc[0]

    # Sélectionner les colonnes spécifiques pour calculer les pourcentages
    pourcentages = df_2021_france[[
        "Thermique (MW)", "Nucléaire (MW)", "Eolien (MW)",
        "Solaire (MW)", "Hydraulique (MW)", "Pompage (MW)",
        "Bioénergies (MW)"
    ]].iloc[0] / production_totale * 100

    # Créer un DataFrame avec les pourcentages
    df_pourcentages = pd.DataFrame(pourcentages).reset_index()
    df_pourcentages.columns = ["Type d'énergie", "Pourcentage (%)"]

    with col1:
        create_fig_1(df_pourcentages)
        # Afficher le camembert
        

    with col2:
        create_fig_2(df_2021)

    st.divider()

    col3, col4 = st.columns(2)

    
    with col3:
        st.write('CARTE DE LA CONSOMMATION PAR REGION EN 2021')
        
        # Affichage cartes consommation par Région en 2021
        #Position [latitude, longitude] sur laquelle est centrée la carte
        location = [47, 1]

        #Niveau de zoom initial :
        #3-4 pour un continent, 5-6 pour un pays, 11-12 pour une ville
        zoom = 6

        #Style de la carte
        tiles = 'cartodbpositron'

        Carte = folium.Map(location = location,
                        zoom_start = zoom,
                        tiles = tiles)

        json = pd.read_json('regions.geojson')

        folium.Choropleth(
            geo_data='regions.geojson',
            name="choropleth",
            data=df_2021,
            columns=['Région', "Consommation (MW)"],
            key_on="feature.properties.nom",
            fill_color="Blues",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Consommation (MW)",
        ).add_to(Carte)
        st_folium(Carte)
        

    with col4:

        # Carte France Production par Région en 2021
        Carte2 = folium.Map(location = location,
                        zoom_start = zoom,
                        tiles = tiles)
        st.write('CARTE DE LA PRODUCTION PAR REGION EN 2021')
        folium.Choropleth(
            geo_data='regions.geojson',
            name="choropleth",
            data=df_2021,
            columns=['Région', "Production_totale (MW)"],
            key_on="feature.properties.nom",
            fill_color="Reds",
            fill_opacity=0.3,
            line_opacity=0.2,
            legend_name="Production_totale (MW)",
        ).add_to(Carte2)
        st_folium(Carte2)


def data_nationale(data):
    df_energie = data

    # Agréger les données par année pour obtenir la consommation et la production totales
    df_conso_prod = df_energie.groupby('Annee').agg({
        'Consommation (MW)': 'sum',
        'Production_totale (MW)': 'sum',
        'Total_NonRenouvelable (MW)': 'sum',
        'Total_Renouvelable (MW)': 'sum'
    }).reset_index()

    # Exclure les lignes où l'année est 2024
    df_conso_prod = df_conso_prod[df_conso_prod['Annee'] != 2024]

    # Création de l'histogramme avec Plotly Express
    fig = px.bar(
        df_conso_prod,
        x='Annee',
        y=['Consommation (MW)', 'Production_totale (MW)'],  # Ajouter la production totale
        title="Consommation et production d'électricité par année",
        labels={'value': 'MW', 'variable': 'Type d\'énergie'},  # Labels personnalisés pour l'axe Y et les légendes
        opacity=0.8,  # Opacité des barres
        color_discrete_sequence=['#636EFA', '#EF553B'],  # Couleurs distinctes pour consommation et production
        barmode='group',  # Barres côte à côte
        category_orders={'Annee': df_conso_prod['Annee']}  # Ordre des catégories pour 'Annee'
    )

    # Mise à jour de la mise en page pour ajuster la taille et centrer le titre
    fig.update_layout(
        width=900,  # Largeur de la figure
        height=400,  # Hauteur de la figure
        xaxis_title="Année",  # Titre de l'axe X
        yaxis_title="MW",  # Titre de l'axe Y
        legend_title="Type d'énergie",  # Titre de la légende
        title_x=0.5,  # Centrer le titre
        margin=dict(l=50, r=50, t=50, b=50),  # Marges pour une meilleure disposition
        xaxis=dict(
            tickmode='array',  # Utilisation du mode de tick 'array'
            tickvals=df_conso_prod['Annee'],  # Valeurs des ticks (les années)
            ticktext=df_conso_prod['Annee'].astype(str),  # Texte des ticks (converti en chaîne pour éviter les problèmes)
            tickangle=-45,  # Rotation des labels pour éviter le chevauchement
            tickfont=dict(size=10),  # Taille de la police des labels
        ),
        legend=dict(
            orientation='h',  # Orientation horizontale de la légende
            traceorder='normal',  # Ordre normal des traces (consommation avant production)
            x=0.5,  # Position horizontale au centre
            y=-0.2,  # Position verticale en dessous de la figure
            bgcolor='rgba(0,0,0,0)',  # Couleur de fond transparente pour la légende
            bordercolor='rgba(0,0,0,0)',  # Couleur de bordure transparente pour la légende
            xanchor='center',  # Ancrage horizontal au centre
            yanchor='top'  # Ancrage vertical en haut
        )
    )

    # Afficher l'histogramme
    st.plotly_chart(fig)

    df_conso_globale = df_energie[['Annee', 'Mois', 'Consommation (MW)']].groupby(['Annee', 'Mois']).sum()
    df_conso_globale.reset_index(inplace=True)
    cats = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    df_conso_globale['Mois'] = pd.Categorical(df_conso_globale['Mois'], categories=cats, ordered = True)
    df_conso_globale = df_conso_globale.sort_values(by=['Annee', 'Mois'])

    df_conso_globale_altair = df_conso_globale.copy()
    df_conso_globale_altair['Annee'] = df_conso_globale_altair['Annee'].astype('category')

    alt.renderers.enable('html')
    chart = alt.Chart(df_conso_globale_altair, title = 'Consommation électrique mensuelle par année').mark_line(point=True).encode(
        x = alt.X("Mois", sort = cats, axis = alt.Axis(title="Mois", labelAngle=45)),
        y = alt.Y('Consommation (MW)', axis = alt.Axis(title="Consommation (MW)")),
        color = alt.Color('Annee', title='Annee')
    ).properties(width=800, height = 500).interactive()
    chart


