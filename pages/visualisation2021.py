import pandas as pd
import plotly.express as px
import streamlit as st
import geopandas as gpd
import branca.colormap as cm
import folium 
from streamlit_folium import st_folium

st.title('VISUALISATIONS ANNEE DE REFERENCE 2021')

df_energie = pd.read_csv(r"df_energie.zip")

#Création d'un dataframe qui somme la consommation et la production par région et par année
df_source = df_energie.groupby(['Annee', 'Région'])[['Consommation (MW)','Thermique (MW)',	'Nucléaire (MW)',	'Eolien (MW)',	'Solaire (MW)',	'Hydraulique (MW)',	'Pompage (MW)',	'Bioénergies (MW)',	'Ech. physiques (MW)','Production_totale (MW)', 'Total_NonRenouvelable (MW)', 'Total_Renouvelable (MW)']].sum().reset_index()

#Création d'un dataframe pour l'année de référence 2021
df_2021 = df_source.loc[df_source["Annee"] == 2021]

# Supprimer la colonne 'Région'
df_2021_france = df_2021.drop(columns=['Région', 'Annee']).sum()

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

# Créer le camembert avec Plotly Express
fig = px.pie(df_pourcentages, values='Pourcentage (%)', names='Type d\'énergie',
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
# Afficher le camembert
st.plotly_chart(fig)


# Création d'un camembert représentant en % la consommation d'énergie par Région
fig = px.pie(df_2021, values='Consommation (MW)', names='Région',
                 title=f"Consommation d'énergie par région en France pour l'année 2021")

fig.update_layout(
      width=800,  # largeur en pixels
    height=500,  # hauteur en pixels
    legend=dict(
        orientation="v",  # 'v' pour vertical
        yanchor="top",  # ancrer en haut
        y=1,  # place la légende à la hauteur du graphique
        xanchor="left",  # ancrer à gauche
        x=-0.3  # déplacer légèrement la légende vers la gauche
    )
)

# Afficher le camembert
st.plotly_chart(fig)

df_anim = df_energie[df_energie["Annee"]>2014].sort_values(by="Annee")

# # Définir une couleur spécifique pour chaque région
# couleurs_regions = {
#      'Île-de-France': '#1f77b4',   # Bleu
#     'Auvergne-Rhône-Alpes': '#ff7f0e',   # Orange
#     'Provence-Alpes-Côte d\'Azur': '#2ca02c',   # Vert
#     'Bretagne': '#d62728',   # Rouge
#     'Normandie': '#9467bd',   # Violet
#     'Nouvelle-Aquitaine': '#8c564b',   # Marron
#     'Occitanie': '#e377c2',   # Rose
#     'Pays de la Loire': '#7f7f7f',   # Gris
#     'Hauts-de-France': '#bcbd22',   # Vert clair
#     'Grand Est': '#17becf',   # Bleu clair
#     'Centre-Val de Loire': '#ffbb78',   # Jaune foncé
#     'Bourgogne-Franche-Comté': '#f7b6d2'  # Rose clair
# }

# # Création du graphique de boîtes animées
# fig = px.box(df_anim,
#              x="Région",
#              y="Consommation (MW)",
#              animation_frame="Annee",
#              range_y=[0, 20000],
#              color="Région",  # Utilisation de la colonne 'Région' pour la coloration
#              color_discrete_map=couleurs_regions  # Application de la carte de couleur
#             )

# # Mise à jour de la mise en page
# fig.update_layout(
#     title="Consommation d'énergie par région de 2015 à 2024",
#     xaxis_title="Région",
#     yaxis_title="Consommation (MW)"
# )

# # Afficher le graphique
# st.plotly_chart(fig)


# json = pd.read_json('regions.geojson')
# json.features[5]

# #Position [latitude, longitude] sur laquelle est centrée la carte
# location = [47, 1]

# #Niveau de zoom initial :
# #3-4 pour un continent, 5-6 pour un pays, 11-12 pour une ville
# zoom = 6

# #Style de la carte
# tiles = 'cartodbpositron'

# Carte = folium.Map(location = [46.603354, 1.888334], zoom_start = 6)


# st_folium(Carte)

# # Carte de France COnsommation par région en 2021
# folium.Choropleth(
#     geo_data='regions.geojson',
#     name="choropleth",
#     data=df_2021,
#     columns=['Région', "Consommation (MW)"],
#     key_on="feature.properties.nom",
#     fill_color="Blues",
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name="Consommation (MW)",
# ).add_to(Carte)

# st_folium(Carte)