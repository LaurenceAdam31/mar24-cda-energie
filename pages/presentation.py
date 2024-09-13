import streamlit as st
st.title('PRESENTATION DU SUJET')


st.markdown("""
<style>
.medium-font {
    font-size:25px !important;
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
    font-size:25px !important;
    font-family: system-ui;
}
.left{
         text-align: left;}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='small-font'> L’objectif de ce projet est d’observer la synchronisation entre la consommation et la production d'énergie, tant au niveau national que régional, pour déduire une prévision de consommation. Pour cela, nous allons faire : </p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'> Analyse au niveau national - Analyse de la consommation et de la production à différentes échelles de temps pour visualiser l’évolution de la consommation et de la production. Nous étudierons également le phasage entre la production et la consommation afin d’identifier les périodes avec risques de black out.</p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'> Analyse niveau régional : Analyse de la répartition par région de la production et de la consommation, comparaison des données de consommation et de production entre les différentes et identifier les régions les plus à risques de black-out  </p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'> Analyse par filière de production : voir l’évolution des énergies renouvelables par rapport à l'énergie nucléaire dans le temps. Identifier quelles régions présentent le plus de production d'énergie renouvelable et étudier la répartition par type de production.</p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'> Analyse températures / consommation : Nous procéderons à une étude des corrélations entre la consommation d'énergie et les températures extérieures.  </p>", unsafe_allow_html=True)