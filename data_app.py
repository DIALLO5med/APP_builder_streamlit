import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs


st.markdown("<h1 style='text-align: center; color: black;'>GROUPE 2</h1>", unsafe_allow_html=True)

st.markdown("""
This app allows you to download scraped data on 'villas', 'terrains' and 'appartements' from coin afrique 
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Coin Afrique](https://sn.coinafrique.com/).
""")



# Recuperation du nombre de page maximum du site Coin Afrique (Dynamique)
#i=1
#while True:
    #url = "https://sn.coinafrique.com/?page={}".format(i)
    #rep = get(url)
    #bsoup = bs(rep.text, "html.parser")
    #container = bsoup.find('div', class_='col s6 m4 l3')
    #if container : 
        #i = int(bsoup.find("li", class_="pagination-number").find_all("a")[-1].text)
    #else :
        #nbPage = i
        #break

#Nombre de page (statique)
#nbPage=119

# Fonction de loading des données beautifulSoup
def load_bs(pageMax, title, key):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
        if key == '1':
            DF = pd.DataFrame()
            for p in range(1, pageMax):
                url = f"https://sn.coinafrique.com/categorie/villas?page={p}"
                rep = get(url)
                bsoup = bs(rep.text, "html.parser")
                containers = bsoup.find_all("div", class_="col s6 m4 l3")
                data = []
                for container in containers:
                    try:
                        info_gen = container.find("p", class_ = "ad__card-description").text.split(" ")
                        type_annonce = info_gen[0].strip()
                        nombre_pieces = info_gen[2].strip()
                        prix = container.find("p", class_ = "ad__card-price").text.replace(" ", "").replace("CFA", "").replace("Prixsurdemande", "").strip()
                        adresse = container.find("p", class_ = "ad__card-location").span.text.strip()
                        lien_image = container.find("img", class_ = "ad__card-img")["src"].strip()

                        dico = {
                            "Type d'annoce" : type_annonce,
                            "Nombre de pièces" : nombre_pieces,
                            "Prix (FCA)" : prix,
                            "Adresse" : adresse,
                            "Lien de l'image" : lien_image
                        }
                        data.append(dico)
                    except:
                        pass
                df = pd.DataFrame(data)
                DF = pd.concat([DF, df], axis = 0).reset_index(drop = True)
            
                
        if key == '2':
            DF = pd.DataFrame()
            for p in range(1, pageMax):
                url = f"https://sn.coinafrique.com/categorie/terrains?page={p}"
                rep = get(url)
                bsoup = bs(rep.text, "html.parser")
                containers = bsoup.find_all("div", class_="col s6 m4 l3")
                data = []
                for container in containers:
                    try:
                        info_gen = container.find("p", class_ = "ad__card-description").text.split(" ")
                        valeur = info_gen[1].replace("m²", "")
                        mesure = info_gen[2].replace("ha", "0000").replace("-", "")
                        superficie = valeur + mesure.replace("m", "")
                        prix = container.find("p", class_ = "ad__card-price").text.replace(" ", "").replace("CFA", "").replace("Prixsurdemande", "").strip()
                        adresse = container.find("p", class_ = "ad__card-location").span.text.strip()
                        lien_image = container.find("img", class_ = "ad__card-img")["src"].strip()

                        dico = {
                            "Superficie (m²)" :superficie,
                            "Prix (FCA)" : prix,
                            "Adresse" : adresse,
                            "Lien de l'image" : lien_image,
                            "info" : info_gen
                        }
                        data.append(dico)
                    except:
                        pass
                df = pd.DataFrame(data)
                DF = pd.concat([DF, df], axis = 0).reset_index(drop = True)

        if key == '3':
            DF = pd.DataFrame()
            for p in range(1, pageMax):
                url = f"https://sn.coinafrique.com/categorie/appartements?page={p}"
                res = get(url)
                bsoup = bs(res.text, "html.parser")
                containers = bsoup.find_all("div", class_ = "col s6 m4 l3")
                data = []
                for container in containers:
                    try:
                        info_gen = container.find("p", class_ = "ad__card-description").text.split(" ")
                        nbre_pieces = container.find("p", class_ = "ad__card-description").text.split(" ")[2]
                        prix = container.find("p", class_ = "ad__card-price").text.replace(" ", "").replace("CFA", "").replace("Prixsurdemande", "").strip()
                        adresse = container.find("p", class_ = "ad__card-location").span.text.strip()
                        lien_image = container.find("img", class_ = "ad__card-img")["src"].strip()

                        dico = {
                        "Nombre de pieces" : nbre_pieces,
                        "Prix (FCA)" : prix,
                        "Adresse" : adresse,
                        "Info" : info_gen,
                        "Lien de l'image" : lien_image
                        }
                        data.append(dico)
                    except:
                        pass
                df = pd.DataFrame(data)
                DF = pd.concat([DF, df], axis = 0).reset_index(drop = True)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(DF.shape[0]) + ' rows and ' + str(DF.shape[1]) + ' columns.')
        st.dataframe(DF)
    

# Fonction de loading des données webscraper
def load_(dataframe, title, key) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
      
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

# définir quelques styles liés aux box
st.markdown('''<style> .stButton>button {
    font-size: 12px;
    height: 3em;
    width: 25em;
}</style>''', unsafe_allow_html=True)


page = st.selectbox(
    "Page Indexes",
    options=[opt for opt in range(1, nbPage) ])

option = st.selectbox(
    "Options",
    ("Scrape data using beautifulSoup", "Download scraped data", "Dashboard of the data", "Fill the form"))


if option == "Scrape data using beautifulSoup":
    load_bs(int(page), 'Villas', '1')
    load_bs(int(page), 'Terrains', '2')
    load_bs(int(page), 'Appartements', '3')

if option == "Download scraped data":
    # Charger les données
    load_(pd.read_csv('data/lien-1.csv'), 'Villas', '1')
    load_(pd.read_csv('data/lien-2.csv'), 'Terrains', '2')
    load_(pd.read_csv('data/lien-3.csv'), 'Appartements', '3')


if option == "Fill the form":
    st.markdown("<iframe src=https://ee.kobotoolbox.org/i/CvCjdZwE width='800' height='600'></iframe>", unsafe_allow_html=True)

if option == "Dashboard of the data":
    st.markdown("<iframe width='800' height='600' src='https://lookerstudio.google.com/embed/reporting/64013115-e577-4ece-a3bd-d9552b7223b8/page/p_4uo6mtorhd' frameborder='0' "
                "style='border:0' allowfullscreen sandbox='allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox'></iframe>", unsafe_allow_html=True)




 


