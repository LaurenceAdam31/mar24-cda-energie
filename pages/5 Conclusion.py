import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import import_data as imda
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from joblib import dump, load
import os

# Listes des codes INSEE et des noms de régions
codes_insee = ['11', '24', '27', '28', '32', '44', '52', '53', '75', '76', '84', '93']
noms_regions = ['Ile de France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté', 'Normandie', 
                'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 'Bretagne', 'Nouvelle-Aquitaine', 
                'Occitanie', 'Auvergne-Rhône-Alpes', 'Provence-Alpes-Côte d Azur']

# Concaténer le code INSEE et le nom de la région
regions_concatenees = [f"{code} - {nom}" for code, nom in zip(codes_insee, noms_regions)]

# Dictionnaire des meilleurs modèles par région
meilleurs_modeles = {
    "11 - Ile de France": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "24 - Centre-Val de Loire": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "27 - Bourgogne-Franche-Comté": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "28 - Normandie": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "32 - Hauts-de-France": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "44 - Grand Est": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "52 - Pays de la Loire": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "53 - Bretagne": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "75 - Nouvelle-Aquitaine": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "76 - Occitanie": ('ARIMA', (1, 0, 1), (2, 0, 0, 12)),
    "84 - Auvergne-Rhône-Alpes": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "93 - Provence-Alpes-Côte d Azur": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
}

# Chargement des DataFrames
df_energie = imda.get_df_energie()  # Charge df_energie depuis CSV
df_group = imda.get_df_group(df_energie)  # Charge df_group depuis CSV


# Créer un dictionnaire pour stocker les DataFrames par région
df_par_region = {}
for region, df_region in df_group.groupby("Code INSEE région"):
    if df_region.index.duplicated().any():
        df_region = df_region[~df_region.index.duplicated(keep='first')]
    df_region = df_region.asfreq('MS')
    df_par_region[region] = df_region

# Entraîner, prédire et sauvegarder les modèles pour chaque région
for region, modele_info in meilleurs_modeles.items():
    region_code = int(region.split(' - ')[0].strip())
    df_region = df_par_region[region_code].drop(columns=['Code INSEE région'])
    data = df_region['Consommation (MW)']
    type_modele, order, seasonal_order = modele_info
    if type_modele == 'SARIMAX':
        model = SARIMAX(data, order=order, seasonal_order=seasonal_order).fit()
    elif type_modele == 'ARIMA':
        model = ARIMA(data, order=order).fit()
    
    # Sauvegarder le modèle
    dump(model, f'modele_{region_code}.joblib')
    
    # Prédiction
    start_date = '2021-01-01'
    end_date = '2024-12-01'
    pred = model.get_prediction(start=start_date, end=end_date)
    pred_mean = pred.predicted_mean
    pred_ci = pred.conf_int()
    
    # Sauvegarder les prédictions
    pred_mean.to_csv(f'predictions_{region_code}.csv')
    pred_ci.to_csv(f'predictions_ci_{region_code}.csv')

 

# Streamlit app
st.title("Prédictions de la consommation d'électricité par région")

# Sélection de la région
region_selection = st.selectbox("Sélectionnez une région", regions_concatenees)

if region_selection:
    region_code = int(region_selection.split(' - ')[0].strip())
    try:
        # Charger les prédictions
        pred_mean = pd.read_csv(f'predictions_{region_code}.csv', index_col=0)
        pred_ci = pd.read_csv(f'predictions_ci_{region_code}.csv', index_col=0)
        pred_mean.index = pd.to_datetime(pred_mean.index)
        pred_ci.index = pd.to_datetime(pred_ci.index)
        
        # Charger les données réelles
        df_region = df_par_region[region_code]
        
        # Visualisation
        plt.figure(figsize=(15, 8))
        plt.plot(df_region['Consommation (MW)'], label='Données réelles')
        plt.plot(pred_mean, color="orange", label='Prédictions')
        plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='grey', alpha=0.2, label='Intervalle de confiance')
        plt.axvline(x=pd.to_datetime(start_date), color='red', linestyle='--', label='Date de début des prédictions')
        plt.legend()
        plt.grid(True)
        plt.title(f'Prédictions de la consommation d\'électricité (MW) pour la région {region_selection}')
        st.pyplot(plt)
    except Exception as e:
        st.write("Erreur lors de la génération des prédictions:", str(e))
else:
    st.write("Veuillez sélectionner une région.")


