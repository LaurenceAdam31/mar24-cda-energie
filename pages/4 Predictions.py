from joblib import load
import pandas as pd
import streamlit as st
import datetime
from utils import import_data as imda
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt

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


def creer_modele(data, modele_info):
    type_modele, order, seasonal_order = modele_info
    if type_modele == 'SARIMAX':
        model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
    elif type_modele == 'ARIMA':
        model = ARIMA(data, order=order, seasonal_order=seasonal_order)
    results = model.fit()
    return results

# Chargement des DataFrames
df_energie = imda.get_df_energie()  # Charge df_energie depuis CSV
df_group = imda.get_df_group(df_energie.copy())  # Charge df_group depuis CSV


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

# Chargement du modèle
model_national = load('model_national.pkl')

# SIDEBAR A GAUCHE CLASSIQUE
st.sidebar.title("Predictions")
pages = ["Prediction Nationale", "Prediction Régionale"]
page = st.sidebar.radio("Aller vers", pages)


# Chargement des DataFrames
conso = imda.get_conso(df_energie)  # Charge conso depuis CSV


# SWITCH SUR LA PAGE DE PREDICTION
if page == "Prediction Nationale":
    st.title('Prédictions de la consommation électrique nationale')   
    
    # Création de colonnes pour les entrées de dates
    col1, col2 = st.columns(2)
 
    # Saisie des dates de début et de fin
    d = col1.date_input('Date début', datetime.date.today())
    f = col2.date_input('Date fin', datetime.date(datetime.datetime.now().year + 1, 9, 1))

    # Faire la prédiction en fonction des dates saisies
    if d >= datetime.date(2021, 1, 1):
        prediction = model_national.get_prediction(start=d, end=f)
    else:
        prediction = model_national.get_prediction(start=pd.to_datetime('2024-09-01'), end=f)

    predicted_consumption = prediction.predicted_mean
    pred_ci = prediction.conf_int()

    # Création du DataFrame pour les prédictions
    pred = pd.DataFrame({
        'PERIODE': predicted_consumption.index,
        'Consommation (MW)': predicted_consumption.values
    })

    start_date = '2024-09-01'

    # Visualisation
    plt.figure(figsize=(15, 8))
    if d < datetime.date(2024, 9, 1):
        filtered_conso = conso[(conso.index > pd.to_datetime(d))]
        plt.plot(filtered_conso, label='Données réelles')
    plt.plot(predicted_consumption, color="orange", label='Prédictions')
    plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='grey', alpha=0.2, label='Intervalle de confiance')
    if d <= datetime.date(2024, 9, 1):
        plt.axvline(x=pd.to_datetime(start_date), color='red', linestyle='--', label='Date de début des prédictions')
    plt.legend()
    plt.grid(True)
    plt.title(f'Prédictions de la consommation électrique (MW) nationale')
    st.pyplot(plt)

    predicted_consumption = predicted_consumption.to_frame()
    predicted_consumption = predicted_consumption.rename(columns = {'predicted_mean' : 'Consommation (MW)'})
    
    if d < datetime.date(2024, 9, 1):
        res = pd.concat([filtered_conso, predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]])
    else:
        res = predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]
         
    res = pd.concat([res, pred_ci], axis = 1)

    st.dataframe(res)

    
elif page == "Prediction Régionale":
    # Interface Streamlit
    st.title('Prédictions de la consommation électrique par région')
    
    # Création de colonnes pour les entrées de dates
    col1, col2 = st.columns(2)

    # Saisie des dates de début et de fin
    d = col1.date_input('Date début', datetime.date.today())
    f = col2.date_input('Date fin', datetime.date(datetime.datetime.now().year + 1, 9, 1))

    # Sélection de la région
    region_selection = st.selectbox('Sélectionnez une région', regions_concatenees)

    # Afficher les prédictions pour la région sélectionnée
    if region_selection:
        region_code = region_selection.split(' - ')[0]
        df_region = df_par_region[int(region_code)].drop(columns=['Code INSEE région'])
        modele_info = meilleurs_modeles.get(region_selection)
        
        if modele_info:
            best_model = creer_modele(df_region, modele_info)
            start_date = '2024-09-01'
            end_date = '2024-12-01'
            # Faire la prédiction en fonction des dates saisies
            if d >= datetime.date(2024, 9, 1):
                pred = best_model.get_prediction(start=d, end=f)
            else:
                pred = best_model.get_prediction(start=pd.to_datetime(start_date), end=f)
            pred_mean = pred.predicted_mean
            pred_ci = pred.conf_int()

            # Visualisation
            plt.figure(figsize=(15, 8))
            if d < datetime.date(2024, 9, 1):
                filtered_conso = df_region[(df_region.index > pd.to_datetime(d))]
                plt.plot(filtered_conso, label='Données réelles')
            plt.plot(pred_mean, color="orange", label='Prédictions')
            plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='grey', alpha=0.2, label='Intervalle de confiance')
            if d <= datetime.date(2021, 1, 1):
                plt.axvline(x=pd.to_datetime(start_date), color='red', linestyle='--', label='Date de début des prédictions')
            plt.legend()
            plt.grid(True)
            plt.title(f'Prédictions de la consommation électrique (MW) pour la région {region_selection}')
            st.pyplot(plt)
            
            predicted_consumption = pred_mean.to_frame()
            predicted_consumption = predicted_consumption.rename(columns = {'predicted_mean' : 'Consommation (MW)'})
            
            if d < datetime.date(2024, 9, 1):
                res = pd.concat([filtered_conso, predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]])

            else:
                res = predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]
            res = pd.concat([res, pred_ci], axis = 1)
            
            st.dataframe(res)


        else:
            st.write("Aucun modèle trouvé pour cette région.")