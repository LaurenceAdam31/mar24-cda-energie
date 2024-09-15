import streamlit as st
st.title('PRESENTATION DU SUJET')


st.markdown("""
<style>
.medium-font {
    font-size:20px !important;
    font-family: system-ui;
}
.center{
            text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='medium-font'> Objectifs</p>", unsafe_allow_html=True)

st.markdown("""
<style>
.small-font {
    font-size:16px !important;
    font-family: system-ui;
}
.left{
         text-align: left;}
</style>
""", unsafe_allow_html=True)


st.markdown("<p class='small-font'> <b>L’objectif</b> de ce projet est d’observer la synchronisation entre la consommation et la production d'énergie, tant au niveau national que régional, pour déduire une prévision de consommation. <br> Pour cela, nous allons faire : <br><b>Analyse au niveau national</b> - Analyse de la consommation et de la production à différentes échelles de temps pour visualiser l’évolution de la consommation et de la production. Nous étudierons également le phasage entre la production et la consommation afin d’identifier les périodes avec risques de black out. <br><b>Analyse niveau régional </b> - Analyse de la répartition par région de la production et de la consommation, comparaison des données de consommation et de production entre les différentes et identifier les régions les plus à risques de black-out  <br><b>Analyse par filière de production </b> - voir l’évolution des énergies renouvelables par rapport à l'énergie nucléaire dans le temps. Identifier quelles régions présentent le plus de production d'énergie renouvelable et étudier la répartition par type de production.<br><b>Analyse températures / consommation </b> - Nous procéderons à une étude des corrélations entre la consommation d'énergie et les températures extérieures.  </p>", unsafe_allow_html=True)