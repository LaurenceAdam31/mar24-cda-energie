import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import st_folium
import altair as alt
import os
from statsmodels.tsa.seasonal import seasonal_decompose
import base64
pip install folium streamlit-folium

# Fonction pour appliquer les styles CSS
def apply_styles():
    st.markdown("""
        <style>
        .big-font { font-size: 36px !important; font-family: system-ui; color: #2d3a64; }
        .medium-font { font-size: 25px !important; font-family: system-ui; color: #2d3a64; }
        .small-font { font-size: 18px !important; font-family: system-ui; }
        </style>
    """, unsafe_allow_html=True)
    
    
# Définir une couleur spécifique pour chaque région
couleurs_regions = {
    'Île-de-France': '#1f77b4',   # Bleu
    'Auvergne-Rhône-Alpes': '#ff7f0e',   # Orange
    'Provence-Alpes-Côte d\'Azur': '#2ca02c',   # Vert
    'Bretagne': '#d62728',   # Rouge
    'Normandie': '#9467bd',   # Violet
    'Nouvelle-Aquitaine': '#8c564b',   # Marron
    'Occitanie': '#e377c2',   # Rose
    'Pays de la Loire': '#7f7f7f',   # Gris
    'Hauts-de-France': '#bcbd22',   # Vert clair
    'Grand Est': '#17becf',   # Bleu clair
    'Centre-Val de Loire': '#ffbb78',   # Jaune foncé
    'Bourgogne-Franche-Comté': '#f7b6d2'  # Rose clair
}


# Liste des noms de mois en français
month_name_fr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
                 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

############################################################################################################################

# Fonction pour exclure les périodes spécifiques (mois incomplet)
def exclude_period(dataframe, periods_to_exclude=['2024-10-01']):
    """ Exclut les périodes spécifiées du DataFrame. """
    for period in periods_to_exclude:
        dataframe = dataframe.drop(pd.Timestamp(period), errors='ignore')
    return dataframe

# Fonction pour charger le DataFrame initial df_energie à partir d'un fichier CSV compressé
@st.cache_data
def get_df_energie():
    df_energie = pd.read_csv("df_energie.zip", compression='zip')
    return df_energie



# Création de df_conso_prod (Total par année de la conso et Production par type)
@st.cache_data
def get_df_conso_prod(df_energie):
    df_conso_prod = df_energie.groupby('Annee').agg({
        'Consommation (MW)': 'sum',
        'Production_totale (MW)': 'sum',
        'Total_NonRenouvelable (MW)': 'sum',
        'Total_Renouvelable (MW)': 'sum'
    }).reset_index()
    df_conso_prod = df_conso_prod[df_conso_prod['Annee'] != 2024]
    return df_conso_prod


# Fonction pour filtrer les données pour l'année 2021
@st.cache_data
def data_2021(data):
    df_2021 = data[data["Annee"] == 2021]
    return df_2021

# Fonction pour préparer les données agrégées par région
@st.cache_data
def prepare_data_by_region(data):
    df_source = data.groupby(['Annee', 'Région'])[['Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)',
                                                    'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 
                                                    'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)',
                                                    'Production_totale (MW)', 'Total_NonRenouvelable (MW)', 
                                                    'Total_Renouvelable (MW)']].sum().reset_index()
    return df_source

# Créer l'histogramme reformulé
def create_histogram(df_source):
    # Filtrer les données pour l'année 2021
    df_2021 = df_source[df_source['Annee'] == 2021]
    
    # Reformuler les données pour un graphique groupé
    df_melted = df_2021.melt(id_vars=['Région'], 
                             value_vars=['Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 
                                         'Bioénergies (MW)', 'Total_NonRenouvelable (MW)'],
                             var_name='Type', 
                             value_name='Production')
    
    # Créer un graphique à barres empilées
    fig = px.bar(
        df_melted, 
        x='Région', 
        y='Production', 
        color='Type',
        #title='Production d\'électricité par type par région en 2021',
        labels={'Production': 'MW'},
        opacity=1,
        color_discrete_map={
            'Eolien (MW)': '#B6E880',        # Vert clair pour l'éolien
            'Solaire (MW)': '#FECB52',       # Jaune pour le solaire
            'Hydraulique (MW)': '#19D3F3',   # Bleu clair pour l'hydraulique
            'Bioénergies (MW)': '#FFA15A',   # Orange pour les bioénergies
            'Total_NonRenouvelable (MW)': '#723e64 '  # Violet pour les énergies non renouvelables
        }
    )
    
    # Ajuster la mise en page 
    fig.update_layout(
        xaxis_tickangle=-45,  # Rotation des labels des régions
        margin=dict(l=40, r=40, t=40, b=80),  # Ajustement des marges
        barmode='stack',  # Mode 'empilé' pour afficher les barres empilées
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5,
            yanchor="top",
            y=-0.3
        ),
        height=500,
        width=1000
    )
    
    return fig



def create_echanges(df_source):
    df_2021 = df_source[df_source['Annee'] == 2021]
    # Vérifier s'il y a des valeurs non-nulles dans 'Ech. physiques (MW)'
    
    df_echanges_physiques = df_2021[['Région', 'Ech. physiques (MW)']].dropna()
    
    if df_echanges_physiques.empty:
        st.write("Aucune donnée d'échanges physiques disponible pour 2021.")
        return None
    fig = px.bar(df_echanges_physiques, 
                 x='Région', 
                 y='Ech. physiques (MW)', 
                 title='Echanges physiques par région en 2021',
                 labels={'Ech. physiques (MW)': 'MW'},
                 opacity=0.7,
                 color_discrete_sequence=['grey'])

    fig.update_layout(width=1000, height=500)
    return fig





########################################################################################################################
# Création de conso pour le modèle SARIMAX National (Conso par période)
@st.cache_data
def get_conso(df_energie):
    conso = df_energie.groupby('PERIODE').agg({'Consommation (MW)': 'sum'}).reset_index()
    conso['PERIODE'] = pd.to_datetime(conso['PERIODE'])
    conso.set_index('PERIODE', inplace=True)
    return exclude_period(conso)

# Création de df_group pour le modèle SARIMAX Régional ((Conso par période et par Région)
@st.cache_data
def get_df_group(df_energie):
    df_group = df_energie.groupby(['PERIODE', 'Code INSEE région']).agg({'Consommation (MW)': 'sum'}).reset_index()
    df_group['Code INSEE région'] = df_group['Code INSEE région'].astype(int)
    df_group['PERIODE'] = pd.to_datetime(df_group['PERIODE'])
    df_group.set_index('PERIODE', inplace=True)
    return exclude_period(df_group)




#################################################################################################################################
# Fonction pour générer le graphique national de Bernard
@st.cache_data
def test_bernard(data):
    df_energie = data
    df_conso_prod = get_df_conso_prod(data)

    # Définition des couleurs pour chaque série
    colors = {
        'Consommation (MW)': '#636EFA',  # Bleu
        'Production_totale (MW)':  '#EF553B',  # Rouge
        'Total_NonRenouvelable (MW)': '#FF7F0E',  # Orange
        'Total_Renouvelable (MW)': '#00CC96'  # Vert
    }
    # Création de la figure
    fig = go.Figure()
    # Ajout des traces avec les couleurs définies
    fig.add_trace(go.Scatter(name="Consommation (MW)", x=df_conso_prod.Annee,
                             y=df_conso_prod['Consommation (MW)'],
                             line=dict(color=colors['Consommation (MW)'], width=2)))

    fig.add_trace(go.Scatter(name="Production_totale (MW)", x=df_conso_prod.Annee,
                             y=df_conso_prod['Production_totale (MW)'],
                             line=dict(color=colors['Production_totale (MW)'], width=2)))

    fig.add_trace(go.Scatter(name="Production énergie Non Renouvelable (MW)", x=df_conso_prod.Annee,
                             y=df_conso_prod['Total_NonRenouvelable (MW)'],
                             line=dict(color=colors['Total_NonRenouvelable (MW)'], width=2)))

    fig.add_trace(go.Scatter(name="Production énergie renouvelable (MW)", x=df_conso_prod.Annee,
                             y=df_conso_prod['Total_Renouvelable (MW)'],
                             line=dict(color=colors['Total_Renouvelable (MW)'], width=2)))

    # Trouver la valeur maximale pour définir la plage de l'axe Y
    max_y = df_conso_prod[['Consommation (MW)', 'Production_totale (MW)', 
                           'Total_NonRenouvelable (MW)', 'Total_Renouvelable (MW)']].max().max()
    # Mise à jour du layout
    fig.update_layout(
        title="Évolution de la consommation et de la production d'énergie de 2013 à 2023",
        yaxis_title="MW",
        xaxis=dict(
            tickformat="%Y",
            tickangle=0,
            dtick=1  # Afficher toutes les années
        ),
        yaxis=dict(range=[0, max_y]),  # Définir la plage de l'axe Y
        legend=dict(
            orientation="h",  # Légende horizontale
            y=-0.3,           # Position verticale, en dessous du graphique
            x=0.5,            # Centre horizontal
            xanchor="center",  # Ancre horizontale
            yanchor="top",     # Ancre verticale
            bgcolor='rgba(255, 255, 255, 0.7)',  # Fond de la légende semi-transparent
            font=dict(size=14)  # Taille de la police de la légende (plus grand)
        ),
        margin=dict(
            t=50,  # Marge supérieure pour le titre
            b=150  # Marge inférieure pour la légende
        ),
        width=1000,  # Largeur du graphique
        height=500   # Hauteur du graphique
    )
    st.plotly_chart(fig)
 
 
def get_pourcentages_france():
    # Extraire la production totale pour la France en 2021
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

    # Calcul des pourcentages pour chaque type d'énergie
    production_totale = df_2021_france["Production_totale (MW)"].iloc[0]
    pourcentages = df_2021_france[[
        "Thermique (MW)", "Nucléaire (MW)", "Eolien (MW)", "Solaire (MW)",
        "Hydraulique (MW)", "Pompage (MW)", "Bioénergies (MW)"
    ]].iloc[0] / production_totale * 100

    # Créer un DataFrame avec les pourcentages
    df_pourcentages = pd.DataFrame(pourcentages).reset_index()
    df_pourcentages.columns = ["Type d'énergie", "Pourcentage (%)"]

    return df_pourcentages


        
        
 # Créer le camembert Production d'énergie par type en France en 2021 (fig1)
@st.cache_data
def create_fig_1(df):
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
    
    fig.update_layout(
        legend=dict(
            orientation='h',  # Orientation horizontale de la légende
            font=dict(size=12, color='black')  # Police et couleur du texte de la légende
        ),
        width=550,   # Largeur de la figure en pixels
        height=550   # Hauteur de la figure en pixels
    )
    
    fig.update_traces(
        textinfo='percent+label',  # Afficher les pourcentages et les labels
        textposition='inside',  # Positionner les textes à l'intérieur des segments
        marker=dict(line=dict(color='white', width=2))  # Ajouter une bordure blanche entre les segments pour plus de clarté
    )

    return fig  # Retourner la figure sans l'afficher
    

# Création d'un camembert représentant en % la consommation d'énergie par Région
@st.cache_data
def create_fig_2(df):
    fig = px.pie(df, values='Consommation (MW)', names='Région',
                    title=f"Consommation d'énergie par région en France pour l'année 2021")
    fig.update_layout(
        width=400,  # largeur en pixels
        height=500,  # hauteur en pixels
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
    


    # Créer l'histogramme de phasage régional pour 2021 (fig4)
@st.cache_data
def create_fig4(df_2021):
    fig = px.histogram(
        data_frame=df_2021,  
        x='Région',
        y=['Consommation (MW)', 'Production_totale (MW)'],
        title="Consommation et production d'électricité par région en 2021",
        labels={'value': 'MW', 'variable': 'Type d\'énergie'},  # Labels personnalisés pour l'axe Y et les légendes
        opacity=0.8,  # Opacité des barres
        color_discrete_sequence=['#636EFA', '#EF553B'],  # Couleurs distinctes pour consommation et production
        barmode='group',  # Barres côte à côte
        category_orders={'Région': sorted(df_2021['Région'].unique())}  # Tri des régions par ordre alphabétique
    )
    fig.update_layout(
        width=1000,  # Largeur de la figure
        height=500,  # Hauteur de la figure
        yaxis_title="MW",  # Titre de l'axe Y
        legend_title="Type d'énergie",  # Titre de la légende
        title_x=0,  # Centrer le titre
        margin=dict(l=50, r=50, t=50, b=150),  # Marges pour une meilleure disposition
        legend=dict(
            orientation="h",  # Légende horizontale
            yanchor="top",  # Ancrer la légende en haut
            y=-0.3,  # Placer la légende en dessous de l'axe x
            xanchor="center",  # Ancrer la légende au centre horizontalement
            x=0.5,  # Centrer horizontalement
            font=dict(size=12)  # Taille de police de la légende
        )
    )
    return fig



#@st.cache_data
#def create_fig5(df_2021):
    # Filtrer uniquement les colonnes nécessaires pour optimiser
    #df_filtered = df_2021[['Région', 'Total_NonRenouvelable (MW)', 'Total_Renouvelable (MW)']].copy()

    # Reshape data for bar plot
    #df_melted = df_filtered.melt(id_vars=["Région"],
                                 #value_vars=["Total_NonRenouvelable (MW)", "Total_Renouvelable (MW)"],
                                 #var_name="Type", value_name="Production")
    
    # Création du graphique à barres groupées
    #fig = px.bar(df_melted, x="Région", y="Production", color="Type",
                 #title="Production d'énergie renouvelable et non renouvelable par région en 2021",
                 #labels={"Production": "Production (MW)", "Type": "Type de production"},
                 #barmode='group',
                 #color_discrete_sequence=['#FF7F0E', '#00CC96'],
                 #opacity=0.6
                 
    
    # Optimisation de l'apparence et des performances
    #fig.update_layout(
        #xaxis_tickangle=-45,  # Rotation des labels pour améliorer la lisibilité
        #autosize=False,       # Fixer la taille pour éviter le redimensionnement dynamique trop lourd
        #width=1200,  # Largeur de la figure
        #height=600,           # Taille spécifique pour ne pas utiliser la taille par défaut
        #margin=dict(l=40, r=40, t=40, b=40),  # Marges plus petites pour éviter des espaces inutiles
    #)

    #return fig



# Création du camembert de Production renouvelable et non renouvelable National en 2021 (data_nationale)
@st.cache_data
def data_nationale(data):
    df_energie = data
 # Récupérer df_conso_prod
    df_conso_prod = get_df_conso_prod(data)
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
        width=1000,  # Largeur de la figure
        height=500,  # Hauteur de la figure
        xaxis_title="Année",  # Titre de l'axe X
        yaxis_title="MW",  # Titre de l'axe Y
        legend_title="Type d'énergie",  # Titre de la légende
        title_x=0,  # Centrer le titre
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
    return fig 


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
    ).properties(width=600, height = 400).interactive()
    chart


# Création du graphique de boîtes animées avec Plotly
@st.cache_data
def create_box_plot(data):

    fig = px.box(data,
                  x="Région",
                  y="Consommation (MW)",
                  animation_frame="Annee",
                  range_y=[0, 20000],
                  color="Région",  # Utilisation de la colonne 'Région' pour la coloration
                  color_discrete_map=couleurs_regions  # Application de la carte de couleur
                 )

    # Mise à jour de la mise en page
    fig.update_layout(
        title="Consommation d'énergie par région de 2015 à 2023",
        xaxis_title="Région",
        yaxis_title="Consommation (MW)"
    )
    return fig


#CREATION DES CARTES FOLIUM
def create_map(df_2021, title, column, fill_color, legend_name):
    # Position [latitude, longitude] sur laquelle est centrée la carte
    location = [47, 1]  # Centrer la carte sur la France
    zoom = 6
    tiles = 'cartodbpositron'
    carte = folium.Map(location=location, zoom_start=zoom, tiles=tiles)
    
    folium.Choropleth(
        geo_data='regions.geojson',  # Assurez-vous que ce chemin est correct
        name="choropleth",
        data=df_2021,
        columns=['Région', column],
        key_on="feature.properties.nom",
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name,
    ).add_to(carte)
    
    return carte

@st.cache_data
def preprocess_data(conso):
    df_moislog = np.log(conso['Consommation (MW)'])
    mult = seasonal_decompose(df_moislog, model='additive', period=12)
    cvs = df_moislog - mult.seasonal
    x_cvs = np.exp(cvs)
    return x_cvs, mult