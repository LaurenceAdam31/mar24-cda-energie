from joblib import load
import pandas as pd
import streamlit as st
import datetime
from utils import import_data as imda
import plotly.express as px

# Chargement du modèle
model_national = load('model_national.pkl')


# Chargement des DataFrames
df_energie = imda.get_df_energie()  # Charge df_energie depuis CSV
conso = imda.get_conso(df_energie)  # Charge conso depuis CSV

# Création de colonnes pour les entrées de dates
col1, col2 = st.columns(2)

# Saisie des dates de début et de fin
d = col1.date_input('Date début', datetime.date.today())
f = col2.date_input('Date fin', datetime.date(datetime.datetime.now().year + 1, 9, 1))

# Faire la prédiction en fonction des dates saisies
if d >= datetime.date(2021, 1, 1):
    prediction = model_national.get_prediction(start=d, end=f)
else:
    prediction = model_national.get_prediction(start=pd.to_datetime('2021-01-01'), end=f)

predicted_consumption = prediction.predicted_mean

# Création du DataFrame pour les prédictions
pred = pd.DataFrame({
    'PERIODE': predicted_consumption.index,
    'Consommation (MW)': predicted_consumption.values
})

# Création du graphique
fig = px.line(pred, x="PERIODE", y="Consommation (MW)", color_discrete_sequence=["#4CC005"], labels={'y': 'Consommation (MW)'})

# Filtrage des données antérieures à 2021
if d < datetime.date(2021, 1, 1):
    filtered_conso = conso[(conso.index > pd.to_datetime(d)) & (conso.index < pd.to_datetime('2021-01-01'))]
    fig.add_scatter(x=filtered_conso.index, y=filtered_conso["Consommation (MW)"], mode='lines', name='Historique', line=dict(color='#0514C0'))

# Mise à jour du layout du graphique
fig.update_layout(title='Stock vs Prédiction', xaxis_title='Date', yaxis_title='Consommation (MW)')

# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)