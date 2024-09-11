import streamlit as st
st.set_page_config(page_title="home", layout = "wide")

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    font-family: system-ui;
}
.center{
            text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🌟 Projet Energie</p>', unsafe_allow_html=True)

st.markdown("""
<style>
.medium-font {
    font-size:30px !important;
    font-family: system-ui;
}
.center{
            text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='medium-font'> Etude sur la production et la consommation d'électrcité en France</p>", unsafe_allow_html=True)

st.markdown("<a class='medium-font' href= 'https://formation.datascientest.com/nos-formations?utm_term=datascientest&utm_campaign=%5Bsearch%5D+data+analyst&utm_source=adwords&utm_medium=ppc&hsa_acc=9618047041&hsa_cam=14490023985&hsa_grp=126147897829&hsa_ad=542987827577&hsa_src=g&hsa_tgt=kwd-810260702289&hsa_kw=datascientest&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=Cj0KCQjwlvW2BhDyARIsADnIe-LSEVxQbp35WkjN2LqsmmWg43ixLtmnuXw8sRpCmSfHq1jIo9LJufEaAviZEALw_wcB'> Formation Continue DATA ANALYST mars 2024 </a>", unsafe_allow_html=True)

st.image('images/accueil.jpg')

st.write('Virginie Fernandes')
st.write('Jessica Picard')
st.write('Bernard Lavole')
st.write('Laurence Adam')
