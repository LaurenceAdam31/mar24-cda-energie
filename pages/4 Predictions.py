from joblib import load
import pandas as pd
import streamlit as st
import datetime
from utils import import_data as imda
import plotly.express as px
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt



# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie - prédictions", page_icon="🌟", layout="wide")

#  # Dictionnaire des meilleurs modèles par région
# meilleurs_modeles = {
#     "11 - Ile de France": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "24 - Centre-Val de Loire": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "27 - Bourgogne-Franche-Comté": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "28 - Normandie": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "32 - Hauts-de-France": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "44 - Grand Est": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "52 - Pays de la Loire": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "53 - Bretagne": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "75 - Nouvelle-Aquitaine": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "76 - Occitanie": ('ARIMA', (1, 0, 1), (2, 0, 0, 12)),
#     "84 - Auvergne-Rhône-Alpes": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
#     "93 - Provence-Alpes-Côte d Azur": ('SARIMAX', (0, 1, 2), (1, 2, 2, 12)),
   
# }
image_paths = {
    '11': 'images/model_region_11.jpg',
    '24': 'images/model_region_24.jpg',
    '27': 'images/model_region_27.jpg',
    '28': 'images/model_region_28.jpg',
    '32': 'images/model_region_32.jpg',
    '44': 'images/model_region_44.jpg',
    '52': 'images/model_region_52.jpg',
    '53': 'images/model_region_53.jpg',
    '75': 'images/model_region_75.jpg',
    '76': 'images/model_region_76.jpg',
    '84': 'images/model_region_84.jpg',
    '93': 'images/model_region_11.jpg',
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
pages = ["Modélisation","Prediction Nationale", "Prediction Régionale"]
page = st.sidebar.radio("Aller vers", pages)


# Chargement des DataFrames
conso = imda.get_conso(df_energie)  # Charge conso depuis CSV

# Appel de la fonction pour appliquer les styles
imda.apply_styles()


# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">📈 Prédictions</p>', unsafe_allow_html=True)


# SWITCH SUR LA PAGE DE MODÉLISATION
if page == "Modélisation":
    st.markdown('<p class="medium-font"><b>Choix des modèles utilisés pour les prédictions</b></p>', unsafe_allow_html=True)

    st.markdown('<p class="small-font">Plusieurs modèles de prévision peuvent être utilisés. Nous avons tout d\'abord choisi d\'essayer des modèles simples:', unsafe_allow_html=True)

    st.markdown("""
        <ul>
            <li class="small-font">Modèle de régression linéaire : trop simple.</li>
            <li class="small-font">Modèle ARIMA/SARIMA, essai de différents paramètres au niveau national et régional:</li>
        </ul>
        """, unsafe_allow_html=True)
  
    
    with st.expander("Essais au niveau national"):
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; Boucle pour trouver les meilleurs paramètres, basés sur le BIC")
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; Modèle auto les meilleurs paramètres, basés sur le AIC")
    
    with st.expander("Essais au niveau régional"):
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; Application des meilleurs paramètres trouvés au niveau national :  order=(0,1,2), seasonal_order=(1, 2, 2, 12)")
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; Modèle auto pour trouvés les meilleurs paramètres par région, entrainé sur l'ensemble des données")
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; Modèle auto pour trouvés les meilleurs paramètres par région, entrainé sur ensemble train/test")

    st.markdown('<p class="small-font">Les modèles SARIMA se sont révélés les plus adaptés à la forte variation saisonnière de la consommation d\'énergie.</p>', unsafe_allow_html=True)

    st.markdown('<p class="small-font">Nous avons aussi procédé à une transformation logarithmique pour étudier la tendance d\'évolution de la consommation corrigée des variations saisonnières. La visualisation des résidus nous permet de visualiser les évènements ayant impacté la consommation d\'énergie, comme le confinement en 2020.</p>', unsafe_allow_html=True)

    # Appel de la fonction dans la page de modélisation
    x_cvs, mult = imda.preprocess_data(conso)

    # Graphiques
    st.markdown("### Série originale et série corrigée des variations saisonnières")
    with st.expander("Afficher/Masquer la série originale et la série corrigée"):
        fig, ax = plt.subplots(figsize=(8, 4))

        # Série originale
        ax.plot(conso.index, conso['Consommation (MW)'], label='Série originale', color='blue')

        # Série corrigée
        ax.plot(conso.index, x_cvs, label='Série corrigée', color='red', linestyle='--')

        ax.set_title('Série originale et série corrigée des variations saisonnières')
        ax.set_xlabel('Date')
        ax.set_ylabel('Consommation (MW)')

        ax.legend(loc='upper left')
        ax.grid(True)

        st.pyplot(fig)

    # Créer un expander pour la décomposition saisonnière
    st.markdown("### Décomposition de la série")
    with st.expander("Afficher/Masquer la décomposition saisonnière"):
        fig2, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 6), sharex=True)

        # Composantes de la décomposition
        ax1.plot(conso.index, np.log(conso['Consommation (MW)']), label='Log(Consommation)', color='blue')
        ax1.set_title('Série Log(Consommation)')

        ax2.plot(conso.index, mult.trend, label='Tendance', color='green')
        ax2.set_title('Tendance')

        ax3.plot(conso.index, mult.seasonal, label='Saisonnalité', color='orange')
        ax3.set_title('Saisonnalité')

        ax4.plot(conso.index, mult.resid, label='Résidus', color='purple')
        ax4.set_title('Résidus')

        for ax in [ax1, ax2, ax3, ax4]:
            ax.legend(loc='upper left')
            ax.grid(True)

        st.pyplot(fig2)

# SWITCH SUR LA PAGE DE PREDICTION
if page == "Modèles":
    st.markdown('<p class="small-font"><b>Modèles utilisés pour la prédiction</b></p>', unsafe_allow_html=True)
    st.write('Plusieurs modèles de prévisions peuvent êre utilisés : des modèles simples et rapides, et des modèles plus complexes')
    st.write('<b>Modèles simples</b>',' : Modèle de régression linéaire - Modèles ARIMA/SARIMA', unsafe_allow_html=True)
    st.write("Essais au niveau national")
    st.markdown("""
- Boucle pour trouver les meilleurs paramètres, basé sur le BIC
- Modèle automatique (auto arima), qui trouve les meilleurs paramètres basés sur l'AIC
""")
    st.write("Essais au niveau régional")
    st.markdown("""
- Modèle (boucle) avec les meilleurs paramètres trouvés pour le niveau national :  Les meilleurs paramètres identifiés par la fonction sont order=(0,1,2), seasonal_order=(1, 2, 2, 12)
- Modèle automatique pour trouver les meilleurs paramètres par région, entrainé sur l'ensemble des données
- Modèle automatique pour trouver les meilleurs paramètres par région, entrainé sur un ensemble train/test
""")
             
    
if page == "Prediction Nationale":
    st.markdown('<p class="medium-font"><b>Prédictions de la consommation électrique nationale</b></p>', unsafe_allow_html=True)

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
    pred_ci = prediction.conf_int()

   

    # Création du DataFrame pour les prédictions
    pred = pd.DataFrame({
        'PERIODE': predicted_consumption.index,
        'Consommation (MW)': predicted_consumption.values
    })

    start_date = '2021-01-01'

    # Visualisation
    plt.figure(figsize=(15, 8))
    if d < datetime.date(2024, 9, 1):
        filtered_conso = conso[(conso.index > pd.to_datetime(d))]
        plt.plot(filtered_conso, label='Données réelles')
    plt.plot(predicted_consumption, color="orange", label='Prédictions')
    plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='grey', alpha=0.2, label='Intervalle de confiance')
    if d <= datetime.date(2021, 1, 1):
        plt.axvline(x=pd.to_datetime(start_date), color='red', linestyle='--', label='Date de début des prédictions')
    plt.legend()
    plt.grid(True)
    plt.title(f'Prédictions de la consommation électrique (MW) nationale')
    st.pyplot(plt)

    predicted_consumption = predicted_consumption.to_frame()
    predicted_consumption = predicted_consumption.rename(columns = {'predicted_mean' : 'Consommation (MW)'})
    
    if d < datetime.date(2021, 1, 1):
        res = pd.concat([filtered_conso, predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]])
    else:
        res = predicted_consumption[predicted_consumption.index > pd.to_datetime('2024-09-01')]
         
    res = pd.concat([res, pred_ci], axis = 1)

    st.dataframe(res)

    
elif page == "Prediction Régionale":

    
    # Interface Streamlit
    st.markdown('<p class="medium-font"><b>Prédictions de la consommation électrique par région</b></p>', unsafe_allow_html=True)

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
        # modele_info = meilleurs_modeles.get(region_selection)
        
        model_regional = load(f'model_region_{region_code}.pkl')
        
        
        if model_regional:

            start_date = '2021-01-01'
            end_date = '2024-12-01'
            # Faire la prédiction en fonction des dates saisies
            if d >= datetime.date(2021, 1, 1):
                pred = model_regional.get_prediction(start=d, end=f)
            else:
                pred = model_regional.get_prediction(start=pd.to_datetime(start_date), end=f)
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

            image_path = image_paths.get(region_code)
            if image_path:
                st.image(image_path)
            
                
        else:
            st.write("Aucun modèle trouvé pour cette région.")


