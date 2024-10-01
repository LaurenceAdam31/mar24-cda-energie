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
    "75- Nouvelle-Aquitaine": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "76 - Occitanie": ('ARIMA', (1, 0, 1), (2, 0, 0, 12)),
    "84 - Auvergne-Rhône-Alpes": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
    "93 - Provence-Alpes-Côte d Azur": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
   
}

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA

def creer_modele(data, modele_info):
    type_modele, order, seasonal_order = modele_info
    if type_modele == 'SARIMAX':
        model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
    elif type_modele == 'ARIMA':
        model = ARIMA(data, order=order, seasonal_order=seasonal_order)
    results = model.fit()
    return results

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import import_data as imda

# IMPORTATION DES DATAFRAMES
df = imda.import_df()   
df2 = imda.import_df2()  # 

#IMPORT DU DATAFRAME df_group
df_energie = imda.modif_df(df, df2)
df_group = imda.get_df_group(df_energie)

# # Créer un dictionnaire pour stocker les DataFrames par région
df_par_region = {}
for region, df_region in df_group.groupby("Code INSEE région"):
    if df_region.index.duplicated().any():
        df_region = df_region[~df_region.index.duplicated(keep='first')]
    df_region = df_region.asfreq('MS')
    df_par_region[region] = df_region

# Listes des codes INSEE et des noms de régions
codes_insee = ['11', '24','27','28','32','44','52','53','75', '76','84','93']
noms_regions = ['Ile de France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté','Normandie','Hauts-de-France','Grand Est','Pays de la Loire','Bretagne','Nouvelle-Aquitaine','Occitanie','Auvergne-Rhône-Alpes','Provence-Alpes-Côte d Azur']

# Concaténer le code INSEE et le nom de la région
regions_concatenees = [f"{code} - {nom}" for code, nom in zip(codes_insee, noms_regions)]



# Interface Streamlit
st.title('Prédictions de la consommation électrique par région')

# Sélection de la région
region_selection = st.selectbox('Sélectionnez une région', regions_concatenees)

# Afficher les prédictions pour la région sélectionnée
if region_selection:
    region_code = region_selection.split(' - ')[0]
    df_region = df_par_region[int(region_code)].drop(columns=['Code INSEE région'])
    modele_info = meilleurs_modeles.get(region_selection)
    if modele_info:
        best_model = creer_modele(df_region["Consommation (MW)"], modele_info)
        start_date = '2021-01-01'
        end_date = '2024-12-01'
        pred = best_model.get_prediction(start=start_date, end=end_date)
        pred_mean = pred.predicted_mean
        pred_ci = pred.conf_int()

        # Visualisation
        plt.figure(figsize=(15, 8))
        plt.plot(df_region, label='Données réelles')
        plt.plot(pred_mean, color="orange", label='Prédictions')
        plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='grey', alpha=0.2, label='Intervalle de confiance')
        plt.axvline(x=pd.to_datetime(start_date), color='red', linestyle='--', label='Date de début des prédictions')
        plt.legend()
        plt.grid(True)
        plt.title(f'Prédictions de la consommation électrique (MW) pour la région {region_selection}')
        st.pyplot(plt)

    else:
        st.write("Aucun modèle trouvé pour cette région.")
