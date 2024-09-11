import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import plotly as plt

st.title('VISUALISATIONS NATIONALE')

df_energie = pd.read_csv(r"df_energie.zip")

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


df_anim = df_energie[df_energie["Annee"]>2014].sort_values(by="Annee")

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

# Création du graphique de boîtes animées
fig = px.box(df_anim,
             x="Région",
             y="Consommation (MW)",
             animation_frame="Annee",
             range_y=[0, 20000],
             color="Région",  # Utilisation de la colonne 'Région' pour la coloration
             color_discrete_map=couleurs_regions  # Application de la carte de couleur
            )

# Mise à jour de la mise en page
fig.update_layout(
    title="Consommation d'énergie par région de 2015 à 2024",
    xaxis_title="Région",
    yaxis_title="Consommation (MW)"
)

# Afficher le graphique
st.plotly_chart(fig)