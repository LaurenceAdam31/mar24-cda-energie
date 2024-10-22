import streamlit as st
import base64
from utils import import_data as imda


# CONFIG DE LA PAGE --> AVEC FAVICON
st.set_page_config(page_title="Projet Energie", page_icon="🌟", layout="wide")

# Bloc unique pour les styles CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 36px !important;
        font-family: system-ui;
        color: #2d3a64; /* Couleur personnalisée pour le titre */
    }
    .medium-font {
        font-size: 25px !important;
        font-family: system-ui;
        color: #2d3a64;
    }
    .small-font {
        font-size: 18px !important; /* Ajuste la taille selon tes besoins */
        font-family: system-ui;
        line-height: 0.9; /* Ajuste la hauteur de ligne pour réduire l'espacement */
    }
    .linkedin-icon {
        display: inline-block;
        width: 25px; /* Augmente la largeur de l'icône */
        height: 25px; /* Augmente la hauteur de l'icône */
        margin-left: 5px;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre principal avec grande taille de police, aligné à gauche
st.markdown('<p class="big-font">🌟 Projet Energie eco2Mix</p>', unsafe_allow_html=True)

# Sous-titres avec taille moyenne de police
st.markdown("<p class='medium-font'><strong>Etude sur la production et la consommation d'électricité</strong></p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'>en France métropolitaine de janvier 2013 à septembre 2024</p>", unsafe_allow_html=True)

# Image d'accueil
st.image('images/accueil.jpg')

# Ajouter le logo de Datascientest en bas de la page
#st.markdown("<br><br>", unsafe_allow_html=True)  # Saut de ligne pour espacer
st.image('images/datascientest.png', width=300)  # Ajustez la largeur ici


# Texte avec lien cliquable sur "Datascientest.com"
st.markdown("""
    <p class='small-font'>
    Réalisé dans le cadre de la formation <strong>Data Analyst</strong> de 
    <a href='https://formation.datascientest.com/nos-formations?utm_term=datascientest&utm_campaign=%5Bsearch%5D+data+analyst&utm_source=adwords&utm_medium=ppc&hsa_acc=9618047041&hsa_cam=14490023985&hsa_grp=126147897829&hsa_ad=542987827577&hsa_src=g&hsa_tgt=kwd-810260702289&hsa_kw=datascientest&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=Cj0KCQjwlvW2BhDyARIsADnIe-LSEVxQbp35WkjN2LqsmmWg43ixLtmnuXw8sRpCmSfHq1jIo9LJufEaAviZEALw_wcB' target='_blank'>Datascientest.com</a>.
    </p>
    """, unsafe_allow_html=True)
st.markdown("<p class='small-font'>Promotion Mars 2024 - Format continu</p>", unsafe_allow_html=True)

# Saut de ligne
st.markdown("")

# Chemin relatif vers l'image LinkedIn
linkedin_icon_path = "images/linkedin.svg"

# Fonction pour lire et convertir l'image en Base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Fonction pour insérer l'image LinkedIn et le texte en HTML
def render_linkedin(author, linkedin_url, image_base64):
    st.markdown(f"""
    <p class='small-font'>
        <strong>{author}</strong> 
        <a href='{linkedin_url}' target='_blank'>
            <img class='linkedin-icon' src='data:image/svg+xml;base64,{image_base64}'/>
        </a>
    </p>
    """, unsafe_allow_html=True)
    
# Titre "Membres du Projet :" en taille moyenne
st.markdown("<p class='medium-font'><strong>Membres du Projet :</strong></p>", unsafe_allow_html=True)

# Convertir l'icône LinkedIn SVG en base64
linkedin_icon_base64 = get_image_as_base64(linkedin_icon_path)

# Utiliser la fonction pour afficher les auteurs avec l'icône LinkedIn
render_linkedin("Virginie Fernandes", "https://www.linkedin.com/in/virginie-fernandes-47144b76/", linkedin_icon_base64)
render_linkedin("Jessica Picard", "https://www.linkedin.com/in/jessica-picard-97641788/", linkedin_icon_base64)
render_linkedin("Bernard Lavole", "https://www.linkedin.com/in/bernard-lavole-878b9878/", linkedin_icon_base64)
render_linkedin("Laurence Adam", "https://www.linkedin.com/in/laurence-adam/", linkedin_icon_base64)

# Titre "Mentor :" en taille moyenne
st.markdown("<p class='medium-font'><strong>Mentor :</strong></p>", unsafe_allow_html=True)

# Utiliser la fonction pour afficher les auteurs avec l'icône LinkedIn
render_linkedin("Alain Ferlac", "https://www.linkedin.com/in/alain-ferlac-8240171a1//", linkedin_icon_base64)

