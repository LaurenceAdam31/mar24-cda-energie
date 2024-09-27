import streamlit as st

# Configuration de la page
st.set_page_config(page_title="home", layout="wide")

# Bloc unique pour les styles CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 50px !important;
        font-family: system-ui;
        color: #2d3a64; /* Couleur personnalisée pour le titre */
    }
    .medium-font {
        font-size: 30px !important;
        font-family: system-ui;
        color: #2d3a64;
    }
    .small-font {
        font-size: 24px !important; /* Ajuste la taille selon tes besoins */
        font-family: system-ui;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">🌟 Projet Energie eco2Mix</p>', unsafe_allow_html=True)

# Sous-titres avec taille moyenne de police
st.markdown("<p class='medium-font'><strong>Etude sur la production et la consommation d'électricité</strong></p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'>en France métropolitaine de janvier 2013 à juin 2024</p>", unsafe_allow_html=True)

# Image d'accueil
st.image('images/accueil.jpg')

# Texte avec lien cliquable uniquement sur "Datascientest.com"
st.markdown("""
    <p class='small-font'>
    Réalisé dans le cadre de la formation <strong>Data Analyst</strong> de 
    <a href='https://formation.datascientest.com/nos-formations?utm_term=datascientest&utm_campaign=%5Bsearch%5D+data+analyst&utm_source=adwords&utm_medium=ppc&hsa_acc=9618047041&hsa_cam=14490023985&hsa_grp=126147897829&hsa_ad=542987827577&hsa_src=g&hsa_tgt=kwd-810260702289&hsa_kw=datascientest&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=Cj0KCQjwlvW2BhDyARIsADnIe-LSEVxQbp35WkjN2LqsmmWg43ixLtmnuXw8sRpCmSfHq1jIo9LJufEaAviZEALw_wcB' target='_blank'>Datascientest.com</a>.
    </p>
    """, unsafe_allow_html=True)

# Autres textes avec taille moyenne
st.markdown("<p class='small-font'>Promotion Mars 2024 - Format continu</p>", unsafe_allow_html=True)
#st.markdown("<p class='small-font'>Auteurs :</p>", unsafe_allow_html=True)

# Saut de ligne
st.markdown("")

# Liens des auteurs
st.markdown("<p class='small-font'><strong>Virginie Fernandes</strong> - <a href='https://www.linkedin.com/in/virginie-fernandes-47144b76/' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'><strong>Jessica Picard</strong> - <a href='https://www.linkedin.com/in/jessica-picard-97641788/' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'><strong>Bernard Lavole</strong> - <a href='https://www.linkedin.com/in/bernard-lavole-878b9878/' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'><strong>Laurence Adam</strong> - <a href='https://www.linkedin.com/in/laurence-adam/' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
