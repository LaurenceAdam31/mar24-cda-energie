from joblib import load
import pandas as pd
import streamlit as st
import datetime
from matplotlib import pyplot as plt
from utils import import_data as imda
import plotly.express as px

model_national = load('model_national.pkl')

df_conso = imda.import_df("df_conso.csv")
df_conso.drop(df_conso.columns[0], axis=1, inplace=True)

# Convertir la colonne 'Date' en format datetime
df_conso['Date'] = pd.to_datetime(df_conso['Date'], errors='coerce')

# Extraire l'année et le mois au format 'AAAA-MM' et créer une nouvelle colonne 'PERIODE'
df_conso['PERIODE'] = df_conso['Date'].dt.strftime('%Y-%m')
conso = df_conso.groupby('PERIODE').agg({
    'Consommation (MW)': 'sum'
}).reset_index()
conso['PERIODE'] = pd.to_datetime(conso['PERIODE'], format='%Y-%m')
conso.set_index('PERIODE', inplace=True)

col1, col2 = st.columns(2)

d = col1.date_input('Date début', "today")
f = col2.date_input('Date fin', datetime.date(datetime.datetime.now().year + 1, 9, 1))

if d >= datetime.date(2021, 1, 1):
    prediction = model_national.get_prediction(start = d, end = f)
else:
    prediction = model_national.get_prediction(start = pd.to_datetime('2021-01-01'), end = f)
    
    
predicted_consumption = prediction.predicted_mean



conso.reset_index(inplace=True)


pred = pd.DataFrame({'index' : predicted_consumption.index, 'Consommation (MW)' : predicted_consumption}).reset_index(drop=True)

fig = px.line(pred, x = "index", y = "Consommation (MW)", color_discrete_sequence=["#4CC005"], labels={'y': 'Stock'})

if d < datetime.date(2021, 1, 1):
    conso = conso[(conso['PERIODE'] > pd.to_datetime(d)) & (conso['PERIODE'] < pd.to_datetime('2021-01-01'))]
    fig.add_scatter(x = conso["PERIODE"], y = conso["Consommation (MW)"], mode = 'lines', name='Prediction', line=dict(color='#0514C0'))


fig.update_layout(title='Stock vs Prediction', xaxis_title='Date', yaxis_title='Value')

st.plotly_chart(fig, use_container_width=True)