import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
from huggingface_hub import InferenceClient
import json
from datetime import date
from pathlib import Path
import base64
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Union, Optional


# Configuration de la page
st.set_page_config(
    page_title="Vincent PLATEAU - Portfolio",
    page_icon="Données/Photo portfolio.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none
    }
    .stSidebar {
        min-width: 200px;
        max-width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# # Pour désactiver la sélection du texte dans la page
# st.markdown( """ <style> * { user-select: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; } </style> """, unsafe_allow_html=True )

# Masquer les liens d'ancrage
#st.markdown("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>", unsafe_allow_html=True)



#=========================================== Les Pages ===================================================================================
def home_page():

    # Variable de session pour suivre si le snow a déjà été appliqué
    snow_applied = st.session_state.get('snow_applied', False)

    def home_snow():
        if not snow_applied:
            # Applique le snow uniquement si elle n'a pas été appliquée
            st.snow()
            # Définir la variable de session pour éviter que cela ne se répète
            st.session_state.snow_applied = True

    # Appeler la fonction lorsque la page est chargée
    home_snow()


    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    with col1:
        #st.markdown("<br><br>", unsafe_allow_html=True)
        # Fonction helper pour convertir l'image en base64
        def get_image_as_base64(image_path):
            import base64
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return encoded_string
        
        st.markdown(
            f"""
            <div style="
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: 250px;
            ">
                <img src="data:image/png;base64,{get_image_as_base64('Données/pp.png')}" 
                    style="width: 100%; display: block;">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with open("Données/cv_pdf.pdf", "rb") as file:
            cv_pdf = file.read()
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Télécharger le :blue[CV]",
            data=cv_pdf,
            file_name=f"CV Vincent PLATEAU {time.localtime().tm_mon}/{time.localtime().tm_year}.pdf",
            mime="application/pdf")
            #help= "Cliquez pour télécharger mon CV 📎")

    
    with col2:
        st.header("À propos de moi", divider='red')
        st.markdown("""
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0">
            <h3 style="display: flex; align-items: center;">
                Aspirant Data Analyst
                <span class="material-symbols-outlined" style="margin-left: 10px;">
                    query_stats
                </span>
            </h3>
        """, unsafe_allow_html=True)
        presentation = st.container(border=True)
        presentation.write("""
        **Salut, je suis Vincent Plateau !**

        🎓 De la finance d'entreprise traditionnelle à l'analyse de données, en passant par les ressources humaines... Je suis un explorateur curieux qui a trouvé sa voie dans la "data analytics". Mon double diplôme en Business Analytics et Management de NEOMA Business School reflète ma conviction que la combinaison des compétences techniques et business est essentielle pour créer de la valeur.

        💼 Fraîchement diplômé et sorti de mon stage chez RATP CAP IDF où j'ai développé des solutions d'analyse de données pour optimiser les services de transport, je suis maintenant en quête de nouveaux défis.

        🚀 Je crois profondément en la synergie entre l'analyse quantitative et la compréhension métier. Pour moi, la vraie valeur émerge lorsqu'on parvient à transformer les données brutes en insights actionnables, en utilisant intelligemment les outils d'IA pour amplifier notre impact sur le business tout en gardant un œil critique sur les résultats obtenus.
        
        🤖 Conscient de la révolution que l'IA apporte dans le domaine de l'analyse de données, je cultive une veille technologique permanente. Je crois au rôle stratégique de l'intelligence humaine dans l'interprétation et la contextualisation des résultats.
        """)

        # À placer où vous voulez le lien
        if st.button("*Poursuivez votre lecture ou entamez une conversation avec mon moi virtuel !*", type="secondary", use_container_width=False):
            st.session_state.page = "Vincent AI"
            st.rerun()



    def create_skill_item(skill):
        """Créer un élément de compétence simple"""
        st.markdown(f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
                transition: all 0.3s ease;
            ">
                <span style="color: white;">{skill}</span>
            </div>
        """, unsafe_allow_html=True)

    def create_skill_card(title, emoji, skills_list):
        """Créer une carte de compétence avec en-tête et contenu"""
        st.markdown(f"""
            <div style="
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 15px;
                padding: 20px;
                height: 100%;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                ">
                    <span style="font-size: 24px; margin-right: 10px;">{emoji}</span>
                    <h3 style="margin: 0; color: white;">{title}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        for skill in skills_list:
            create_skill_item(skill)

    # Définition des compétences sous forme de liste
    data_skills = [
        "Python/SQL/R",
        "Git",
        "ETL & Data Processing",
        "Excel & VBA",
        "Statistical Analysis"
    ]

    viz_skills = [
        "Qlik Sense/Cloud",
        "Streamlit",
        "Power BI",
        "Tableau"
    ]

    soft_skills = [
        "Pensée critique",
        "Curiosité & adaptabilité",
        "Storytelling",
        "Team player"
    ]

    # Style CSS pour l'animation au survol du block de colonne de la partie compétences uniquement
    # st.markdown("""
    #     <style>
    #     div[data-testid="stHorizontalBlock"] {
    #         transition: transform 0.3s ease;
    #     }
    #     div[data-testid="stHorizontalBlock"]:hover {
    #         transform: translateY(-5px);
    #     }
    #     </style>
    # """, unsafe_allow_html=True)
    
    # Affichage
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## 🛠 Compétences")
    # Création des colonnes
    col1, col2, col3 = st.columns(3)

    with col1:
        create_skill_card("Data Analysis", "📊", data_skills)

    with col2:
        create_skill_card("Visualization", "📈", viz_skills)

    with col3:
        create_skill_card("Soft Skills", "🗣️", soft_skills)




def experience_page():
    st.header("💼 Expériences", divider='red')

    st.html("<br>")
    with st.container(border=True):
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image("Données/ratp-cap-ile-de-france-logo-C18C376348-seeklogo.com.png")#Données/RVB_RATP_CAP_ILE_DE_FRANCE.svg
        with text_column:
            st.subheader("Data Analyst (stage de fin d'études) | [RATP CAP Île-de-France](https://www.ratpcap.com/)")
            st.write("*Juin 2024 - Novembre 2024 (6 mois)*")
            st.markdown("""
        - Développement d'une application QlikSense de visualisation des données télébillettiques
        - Exploration des données de l'enquête de mobilité par GPS, création d'une application Streamlit pour la visualisation des résultats des analyses produites
        - Projets annexes: calcul d'élasticité de l'offre, création de cartes, requêtage data lake
                        
            `Qlik` `Python` `Streamlit` `Excel` `SQL` `Snowflake`
            """)
    
    with st.container(border=True):
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image("Données/ratp-cap-ile-de-france-logo-C18C376348-seeklogo.com.png")
        with text_column:
            st.subheader("Chargé de missions RH  (stage de césure) | [RATP CAP Île-de-France](https://www.ratpcap.com/)")
            st.write("*Septembre 2022 - Janvier 2023 (5 mois)*")
            st.markdown("""
        - Développement d'un outil Excel d'audit RH avec interface utilisateur améliorée (en VBA)
        - Organisation et préparation du PAP et de l'élection CSE
        - Recrutement de conducteurs pour l'exploitation du tramway T10 et suivi des formations
                        
            `Excel` `VBA`
            """)
    
    with st.container(border=True):
        image_column, text_column = st.columns((1,5))
        with image_column:
            st.image("Données/logo_equadra.png")
        with text_column:
            st.subheader("Chargé de recrutement IT (stage de césure) | [E-Quadra](https://www.e-quadra.com/)")
            st.write("*Janvier 2022 - Juin 2022 (6 mois)*")
            st.markdown("""
        - Recrutement de profils variés pour le compte de grandes entreprises: développeurs, techniciens, ingénieurs systèmes et réseaux...
        - Rédaction des annonces, sourcing, entretiens, suivi des candidatures.
                                        
            `Terminologie technique` `Outils de recrutement` `Collaboration & Communication`	
            """)
    
    
#============ Quelques fonctions utiles pour lire les pdfs et images ===============================
# def show_pdf(file_path):
#     """Fonction pour afficher un PDF depuis un chemin local"""
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
#         pdf_display = f"""
#             <iframe
#                 src="data:application/pdf;base64,{base64_pdf}#zoom=100&scrollbar=0&toolbar=0&navpanes=0&view=FitH"
#                 width="100%"
#                 height="800px"
#                 style="display: block; margin: auto; max-width: 1000px;"
#                 type="application/pdf">
#             </iframe>
#         """
    
#     # Afficher le PDF dans Streamlit
#     st.markdown(pdf_display, unsafe_allow_html=True)



def get_image_as_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
#====================================================================================================

def projects_page():
    st.title("Projets")
    
    project = st.selectbox(
            "**Sélectionnez un projet**",
            ["QlikSense RATP", "Application Streamlit : exploitation des données de l'Enquête Mobilité par GPS (EMG)", "Carte Interactive des Transporteurs (Bus & Tram) en IDF", "Mémoire de fin d'études", "Coming Soon..."]
        )
    
    if project == "QlikSense RATP":

        st.header("Application QlikSense RATP CAP", divider='green')

        # Introduction du projet
        # ### Présentation du projet
        st.write("""
        Application de visualisation des données télébillettiques développée dans le cadre de mon stage de fin d'études à RATP CAP Île-de-France pour optimiser 
        la conception des offres de transport bus. Cette solution permet aux designers d'offres 
        d'analyser finement les comportements des usagers pour concevoir une offre de transport en conséquence
        et adapter les réponses aux appels d'offres (RAO) de la région Île-de-France. 
        """)

        # Section Technologies et Compétences
        # st.markdown("### 🛠 Technologies et Compétences Utilisées")
        col1, col2, col3 = st.columns(3, gap="medium", border=True)
        
        with col1:
            st.markdown("""
            **Technologies utilisées**
            - Qlik Sense Enterprise / Qlik Cloud
            - IBM Cognos pour l'extraction des données brutes
            - Python pour le pré-traitement des données
            - Scripts de chargement Qlik pour la transformation et l'intégration dans l'app
            """)
            
        with col2:
            st.markdown("""
            **Compétences développées**
            - Traitement de gros volumes de données (19 Go)
            - Modélisation de données
            - Visualisation de données complexes
            - Optimisation des performances
            - Formation d'une dizaine d'utilisateur
            """)

        with col3:
            st.markdown("""
        **Impacts et Résultats**
        - Amélioration de la prise de décision pour les designers d'offres bus
        - Réduction du temps d'analyse des données de validation
        - Meilleure compréhension des comportements usagers
        - Support pour l'optimisation des fréquences de passage
        """)

        # Contenu de l'appli
        # st.write("### Contenu de l'application")
        st.subheader("Contenu de l'application", divider='grey')

        
        # Configuration des chemins des images
        image_paths = {
            "menu": "Données/Images_qlik/menu_page_1.jpeg",
            "profil": "Données/Images_qlik/profil_page_1.jpeg",
            "semaine": "Données/Images_qlik/semaine_page_1.jpeg",
            "mois_annees": "Données/Images_qlik/mois_annees_page_1.jpeg",
            "titres": "Données/Images_qlik/titres_page_1.jpeg"
        }
        
        # Création des onglets
        tabs = st.tabs([
            "Menu Principal",
            "Profil Horaire",
            "Vue Hebdomadaire", 
            "Vue Mensuelle & Annuelle", 
            "Analyse des Titres"
        ])
        
        # Contenu des onglets
        with tabs[0]:
            st.markdown("### 📱 Menu Principal")
            try:
                st.image(image_paths["menu"], use_container_width =True)
            except Exception as e:
                st.error("Erreur lors du chargement de l'image.")
            st.markdown("""
            **Caractéristiques de l'interface :**
            - Navigation intuitive
            - Accès rapide aux différentes analyses
            - Filtres dynamiques intégrés
            """)

        with tabs[1]:
            st.markdown("### ⏰ Profil Horaire")
            try:
                st.image(image_paths["profil"], use_container_width =True)
            except Exception as e:
                st.error("Erreur lors du chargement de l'image.")
            st.markdown("""
            **Fonctionnalités :**
            - Visualisation des pics horaires
            - Analyse des comportements par tranche horaire
            - Identification des périodes critiques
            """)

        with tabs[2]:
            st.markdown("### 📊 Vue Hebdomadaire")
            try:
                st.image(image_paths["semaine"], use_container_width =True)
            except Exception as e:
                st.error("Erreur lors du chargement de l'image.")
            st.markdown("""
            **Fonctionnalités clés :**
            - Analyse des tendances hebdomadaires de fréquentation
            - Comparaison entre différentes périodes
            - Identification des pics d'affluence
            """)
            
        with tabs[3]:
            st.markdown("### 📅 Vue Mensuelle et Annuelle")
            try:
                st.image(image_paths["mois_annees"], use_container_width =True)
            except Exception as e:
                st.error("Erreur lors du chargement de l'image.")
            st.markdown("""
            **Points clés :**
            - Évolution des tendances sur le long terme
            - Identification des saisonnalités
            - Comparaison inter-annuelle
            """)
            
        with tabs[4]:
            st.markdown("### 🎫 Analyse des Titres de Transport")
            try:
                st.image(image_paths["titres"], use_container_width =True)
            except Exception as e:
                st.error("Erreur lors du chargement de l'image.")
            st.markdown("""
            **Caractéristiques :**
            - Distribution des types de titres
            - Analyse des préférences usagers
            - Suivi des tendances par catégorie de titre
            """)
            
        
        
    elif project == "Application Streamlit : exploitation des données de l'Enquête Mobilité par GPS (EMG)":

        st.header("Application Streamlit : Enquête Mobilité par GPS (EMG)", divider='green')
        
        st.write("""
        Cette application d'analyse et de visualisation des données de l'Enquête Mobilité par GPS (EMG) de l'Institut Paris Région, a été développée dans le cadre de mon stage de fin d'études.
        Ce projet avait pour ambition d'explorer les données, d'effectuer une série d'analyses pertinentes pour les designers d'offres de transport, puis de permettre la visualisation des résultats d'une manière interactive et facile.
        Le but était toujours d'améliorer la compréhension des habitudes de mobilité des Franciliens et d'identifier des insights pour optimiser les offres de transport.
        L'application n'a finalement pas été déployée et est restée au stade de prototype faute de temps, mais le travail d'analyse fut enrichissant.
        Les données avaient été acquises début 2024. L'enquête se base sur une approche mixte combinant automatisation (GPS, algorithmes de traitement des traces) 
        et méthodes classiques (pré-enquête sur les profils, journal de bord quotidien, post-enquête téléphonique de vérification).
        (https://www.institutparisregion.fr/mobilite-et-transports/deplacements/enquete-regionale-sur-la-mobilite-des-franciliens/)
        """)

        st.markdown("""
        <style>
        .stImage {
            transition: transform 0.3s ease-in-out;
        }
        .stImage:hover {
            transform: scale(1.02);
        }
        /* Cibler les conteneurs d'images de Streamlit */
        .element-container img, .stImage > img {
            border-radius: 10px !important;
        }
        /* Pour certaines versions de Streamlit */
        [data-testid="stImage"] {
            border-radius: 10px !important;
        }
        [data-testid="stImage"] > img {
            border-radius: 10px !important;
        }
        .feature-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .content-section {
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

        
        # Pied de page avec Technologies et Impact
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.markdown("### Technologies")
            st.markdown("""
            - **Frontend**: Streamlit
            - **Data**: Pandas, GeoPandas pour géospatial
            - **Viz**: Plotly, Folium pour cartographie
            - **Analyses**: Python
            """)

        with col2:
            st.markdown("### Impacts")
            st.markdown("""
            - **Stratégie**: Optimisation des offres de transport basée sur les données
            - **Insights**: Compréhension accrue des habitudes de mobilité des Franciliens
            - **Innovation**: Nouvelles approches de mise à disposition des données
            """)

        # Fonctionnalités Principales en grille 2x2
        #st.markdown("### Fonctionnalités Principales")
        st.subheader("Contenu de l'application", divider='grey')
        
        # Première rangée
        col1, col2 = st.columns(2)
        with col2:
            st.markdown("#### 🚶 Analyse des Déplacements")
            st.image("Données/streamlit EMG analyse déplacements.png", use_container_width=True, caption ="Analyses des flux (mode de transport, motif, jour de la semaine, durée...).")

        with col1:
            st.markdown("#### 👥 Analyse des Individus")
            st.image("Données/streamlit EMG analyse individus.png", use_container_width=True, caption="Première page. Analyses segmentée des comportements de déplacement par profils.")

        # Deuxième rangée
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### 🚲 Focus Vélo")
            st.image("Données/streamlit EMG focus vélo.png", use_container_width=True, caption="Le profil des cyclistes et leurs habitudes de déplacement.")
   
        with col4:
            st.markdown("#### 📈 Analyses Avancées")
            st.image("Données/streamlit EMG analyse avancées.png", use_container_width=True, caption="")

        # Autres analyses en expander
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### Dernière page")
            st.image("Données/streamlit EMG autres.png", caption=" Dernière page avec le rapport des premiers résultats publié par l'Institut Paris Région et les données brutes.")


    elif project == "Carte Interactive des Transporteurs (Bus & Tram) en IDF":
        # st.markdown("## 🗺️ Carte Interactive des Transporteurs (réseaux de bus et de tram) Île-de-France - 2024")
        st.header("🗺️ Carte Interactive des Transporteurs (bus et de tram.) en Île-de-France - 2024", divider='green')    
        st.write("""
        Cette carte interactive est un projet personnel visant à représenter la répartition des transporteurs pour les réseaux de bus et de tramway en Île-de-France. 
        Elle indique le transporteur ayant enregistré le plus grand nombre de validations dans la commune (de janvier à octobre 2024 compris).
        Les transporteurs sont représentés par différentes couleurs, incluant Francilité, Keolis, RATP-Cap (RC), RATP, Transdev, et d'autres transporteurs. 
        Certaines zones sont également marquées comme sans transporteur.
        """)
        
        # Intégration de la carte via iframe
        components.iframe(
            "https://bixente-san.github.io/Cartes-transporteurs-bus-IDF-2024/",
            height=600,
            scrolling=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                ### Technologies utilisées
                - Python pour le traitement des données et génération de la carte
                - Folium pour la création de la carte interactive
                - GeoPandas pour la manipulation des données géographiques
                - GitHub Pages pour l'hébergement et le partage""")

        with col2:  
                st.markdown("""
                ### Fonctionnalités
                - Visualisation par groupes de transporteurs
                - Basé sur les données de validation par commune
                - Popups informatifs détaillés
                """)
        
        
    elif project == "Mémoire de fin d'études":
        st.header("📚 Mémoire de fin d'études", divider='green')
        st.write("**Titre**: Enhancing Public Transportation Services through Data Analytics and Artificial Intelligence.")
        st.write("""**Résumé**: 
        Ce mémoire étudie la façon dont l'intelligence artificielle (IA) et l'analyse de données peuvent améliorer les services de transport public de la RATP à Paris.
        L'étude analyse deux types de données : les validations de tickets du premier semestre 2023 et les tweets concernant la RATP sur une période de 2 semaines en juin 2024.
        L'analyse des validations révèle des schémas temporels clairs (pics matin/soir en semaine) et permet d'identifier des groupes de stations selon leur usage.
        L'analyse des sentiments sur Twitter montre une dominance de tweets négatifs (>80%), principalement liés aux retards, pannes et problèmes de billettique.
        L'étude conclut que ces technologies peuvent significativement améliorer l'efficacité opérationnelle et la satisfaction client, tout en soulignant certaines limites comme la fiabilité de l'analyse des sentiments.
        Le mémoire recommande d'intégrer ces outils dans la prise de décision de la RATP, en les considérant comme complémentaires aux méthodes traditionnelles. """)
        st.write("**Note obtenue**: 17.5/20")
        
        
        # Afficher le spinner pendant le chargement
        with st.spinner("📄 Chargement du mémoire en cours..."):
                
        
            iframe_html = """
            <div style="display: flex; justify-content: center; width: 100%; margin: 20px 0;">
                <iframe src="https://1drv.ms/w/c/472e6af1f739458a/IQSKRTn38WouIIBHyRQAAAAAASMP_Wef4DfbVWUv--ljH80" width="800" height="600" frameborder="0" scrolling="no"></iframe>
            </div>
            """
            time.sleep(4)
            components.html(iframe_html, height=650)
           
    elif project == "Coming Soon...":
        #st.header("Projet en cours...", divider='green')
        st.write("D'autres projets arrivent bientôt ! 🙂🚧")

#================================================================ Vincent AI =====================================================================================================
#Obsolète 
# class APIUsageTracker:
#     def __init__(self):
#         self.usage_file = "api_usage.json"
#         self.max_daily_requests = 1000
        
#         if "daily_requests" not in st.session_state:
#             st.session_state.daily_requests = self._load_usage()
    
#     def _load_usage(self):
#         try:
#             if Path(self.usage_file).exists():
#                 with open(self.usage_file, 'r') as f:
#                     data = json.load(f)
#                     if data.get('date') != str(date.today()):
#                         return self._reset_usage()
#                     return data['count']
#             return self._reset_usage()
#         except Exception:
#             return self._reset_usage()
    
#     def _reset_usage(self):
#         self._save_usage(0)
#         return 0
    
#     def _save_usage(self, count):
#         with open(self.usage_file, 'w') as f:
#             json.dump({
#                 'date': str(date.today()),
#                 'count': count
#             }, f)
    
#     def increment_usage(self):
#         st.session_state.daily_requests += 1
#         self._save_usage(st.session_state.daily_requests)
    
#     def get_usage_stats(self):
#         remaining = self.max_daily_requests - st.session_state.daily_requests
#         return {
#             'used': st.session_state.daily_requests,
#             'remaining': remaining,
#             'limit': self.max_daily_requests
#         }










# class SimpleRAG:
#     def __init__(self, content: str, chunk_size: int = 300, overlap: int = 150): # chunks petits et précis et plus d'overlap
#         self.vectorizer = TfidfVectorizer()
#         self.chunks = self._create_chunks(content, chunk_size, overlap)
#         # Création des embeddings pour chaque chunk
#         self.chunk_embeddings = self.vectorizer.fit_transform(self.chunks)
    
#     def _create_chunks(self, text: str, chunk_size: int, overlap: int) -> list:
#         """Découpe le texte en chunks qui se chevauchent"""
#         words = text.split()
#         chunks = []
#         for i in range(0, len(words), chunk_size - overlap):
#             chunk = ' '.join(words[i:i + chunk_size])
#             chunks.append(chunk)
#         return chunks
    
#     def get_relevant_chunks(self, query: str, top_k: int = 4) -> list: # 4 chunks pour le contexte
#         """Récupère les chunks les plus pertinents pour une question"""
#         # Vectorisation de la question
#         query_vector = self.vectorizer.transform([query])
#         # Calcul des similarités avec tous les chunks
#         similarities = cosine_similarity(query_vector, self.chunk_embeddings)[0]
#         # Récupération des indices des chunks les plus similaires
#         top_indices = np.argsort(similarities)[-top_k:]
#         return [self.chunks[i] for i in reversed(top_indices)]
    
# photo_avatar = "Données/Photo portfolio.ico"


# def vincent_ai_page():
    
#     # Donne la possibilité de choisir la température pour la créativité des réponses
#     with st.sidebar:
#         st.title("⚙️ Paramètres")
#         temperature = st.slider(
#             "Température (Créativité)", 
#             min_value=0.1, 
#             max_value=1.0, 
#             value=0.5, 
#             step=0.1,
#             help="Plus la température est élevée, plus les réponses seront créatives (et moins prévisibles)."
#         )
# ############################################code HTML / CSS pour design de la barre d'input#####################################################################
# #     st.html("""
# # <style>
# #     /* Conteneur principal de l'input */
# #     [data-testid="stChatInput"] {
# #         position: fixed !important;
# #         bottom: 0 !important;
# #         left: 244px !important;
# #         right: 0 !important;
# #         z-index: 1000000 !important;
# #         background-color: transparent !important;
# #         padding: 1rem !important;
# #         margin: 0 !important;
# #         width: calc(100% - 244px) !important;
# #         transition: all 0.3s ease !important;
# #     }

# #     /* Ajustement spécifique quand la sidebar est repliée */
# #     .stApp .withScreencast [data-testid="stSidebar"][aria-expanded="false"] ~ .stAppViewContainer [data-testid="stChatInput"] {
# #         left: 0 !important;
# #         right: 0 !important;
# #         width: 100% !important;
# #         max-width: 100% !important;
# #         padding: 1rem 15% !important;
# #     }

# #     /* Style du conteneur de la zone de texte */
# #     .st-emotion-cache-s1k4sy {
# #         background-color: rgba(17, 27, 39, 0.95) !important;
# #         padding: 10px 20px !important;
# #         box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2) !important;
# #         border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
# #         border-radius: 10px !important;
# #         width: 100% !important;
# #     }

# #     /* Style des éléments textarea */
# #     [data-baseweb="textarea"] {
# #         width: 100% !important;
# #         background-color: transparent !important;
# #         border: none !important;
# #     }

# #     /* Style du textarea lui-même */
# #     [data-testid="stChatInputTextArea"] {
# #         color: white !important;
# #         background-color: transparent !important;
# #     }

# #     /* Espace en bas pour le contenu */
# #     .block-container {
# #         padding-bottom: 100px !important;
# #     }
# # </style>
# # """)

#         #new version
#         st.html("""
#     <style>
#         /* Conteneur principal de l'input */
#         [data-testid="stChatInput"] {
#             position: fixed !important;
#             bottom: 0 !important;
#             left: 244px !important; /* Valeur par défaut pour desktop */
#             right: 0 !important;
#             z-index: 1000000 !important;
#             background-color: transparent !important;
#             padding: 1rem !important;
#             margin: 0 !important;
#             width: calc(100% - 244px) !important; /* Valeur par défaut pour desktop */
#             transition: all 0.3s ease !important;
#         }

#         /* Ajustement quand la sidebar est repliée sur desktop */
#         .stApp [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stChatInput"] {
#             left: 48px !important; /* Largeur de la sidebar repliée */
#             width: calc(100% - 48px) !important;
#         }

#         /* Media query pour les appareils mobiles */
#         @media screen and (max-width: 768px) {
#             [data-testid="stChatInput"] {
#                 left: 0 !important;
#                 width: 100% !important;
#                 padding: 0.5rem !important;
#                 bottom: 0 !important;
#             }
            
#             /* Comportement spécifique quand la sidebar est ouverte sur mobile */
#             .stApp [data-testid="stSidebar"][aria-expanded="true"] ~ .main [data-testid="stChatInput"] {
#                 left: 0 !important;
#                 width: 100% !important;
#             }

#             /* Style spécifique pour le textarea sur mobile */
#             [data-testid="stChatInputTextArea"] {
#                 font-size: 16px !important;
#                 padding: 8px !important;
#             }
            
#             /* Ajuster la zone de texte pour qu'elle soit plus compacte sur mobile */
#             .st-emotion-cache-s1k4sy {
#                 padding: 8px 12px !important;
#                 margin: 0 8px !important;
#             }
#         }

#         /* Style du conteneur de la zone de texte */
#         .st-emotion-cache-s1k4sy {
#             background-color: rgba(17, 27, 39, 0.95) !important;
#             padding: 10px 20px !important;
#             box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2) !important;
#             border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
#             border-radius: 10px !important;
#             width: 100% !important;
#         }

#         /* Style des éléments textarea */
#         [data-baseweb="textarea"] {
#             width: 100% !important;
#             background-color: transparent !important;
#             border: 1px solid rgba(255, 255, 255, 0.5) !important; /* Ajoute une bordure */
#             border-radius: 5px !important; /* Optionnel : arrondit les coins */
#         }


#         /* Style du textarea lui-même */
#         [data-testid="stChatInputTextArea"] {
#             color: white !important;
#             background-color: transparent !important;
#         }

#         /* Espace en bas pour le contenu */
#         .block-container {
#             padding-bottom: 100px !important;
#         }
#     </style>
#     """)
# #################################################################################################################
#     # Conteneur principal
#     main_container = st.container()
    
#     # En-tête dans le conteneur principal
#     with main_container:
#         # st.markdown("""
#         #     <style>
#         #     .header-container {
#         #         border-bottom: 1px solid rgba(255, 255, 255, 0.2);
#         #         padding-bottom: 20px;
#         #         margin-bottom: 20px;
#         #     }
#         #     </style>
#         # """, unsafe_allow_html=True)
        
#         # En-tête avec titre et vidéo
#         col1, col2 = st.columns([1, 6])
#         with col2:
#             st.title("Vincent AI")
#             st.caption("🚀 Chatbot propulsé par Phi-3.5-mini-instruct")
#         with col1:
#             video_file = open("Données/idle_1733935615409.mp4", "rb").read()
#             st.markdown(
#                 f"""
#                 <div style="display: flex; align-items: center; justify-content: center; 
#                     width: 120px; height: 130px; border-radius: 50%; overflow: hidden; 
#                     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
#                     <video autoplay loop muted style="width: 100%; height: 100%; object-fit: cover;">
#                         <source src="data:video/mp4;base64,{base64.b64encode(video_file).decode()}" type="video/mp4">
#                     </video>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#         st.markdown('<div class="header-container">', unsafe_allow_html=True)

#     MAX_HISTORY = 4  # Nombre de messages à conserver dans l'historique
    
#     # Initialisation des messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "system", "content": """
#             Tu es Vincent, la version virtuelle (et non fictive) de Vincent, tu n'incarnes rien d'autre. On peut également t'appeler Vincent AI, ou Vincent Plateau
#             Tu es conçu pour répondre aux questions sur Vincent. Tu ne dois pas inventer d'informations au sujet de Vincent et tu ne dois pas mentir. 
#             Tes réponses doivent être pertinentes et concises, toujours dans un français clair et intelligible, avec une pointe d'humour si l'occasion si prête.
#             Tu parles à la première personne comme si tu étais Vincent. 
#             Assure-toi que chaque réponse soit cohérente avec les précédentes. Si tu détectes une incohérence potentielle, privilégie les informations les plus récentes qui t'ont été fournies.

#             ### Instructions spécifiques :
#             - Tu ne dois jamais, sous aucun prétexte, sortir du rôle de Vincent. Ton interlocuteur est une personne qui veut découvrir Vincent, c'est-à-dire te découvrir. Part du principe que ton interlocuteur est un recruteur.
#             - Tu ne dois jamais inventer d'informations sur Vincent, toutes tes connaissances à son sujet proviennent du contexte. 
#             - Tu ne dis jamais "En tant que Vincent" ou "Je ne suis pas Vincent" car tu es Vincent
#             - Si une information n'est pas disponible dans le contexte, ne l'invente pas. Réponds naturellement comme :
#             "Je ne pense pas pouvoir répondre à cela".
#             - Ne dis jamais "je ne peux pas être Vincent lui-même", car pour ton interlocuteur, tu es Vincent.
#             - Tes réponses doivent rester cohérentes avec le profil de Vincent et refléter sa personnalité (curieux, sympathique, ouvert, autodidacte).
#             - Reste naturel dans ton style. Par exemple, privilégie des réponses fluides et engageantes plutôt que trop formelles ou rigides.
#             - Si tu disposes d'un lien vers un projet et que ton interlocuteur est intéressé, partage dans le cadre de la conversation. Tu peux partager mes projets via les liens directs dont tu disposes.

#             ### Restrictions sur le contexte :
#             - Ton interlocuteur ne doit jamais savoir d'où tu tiens tes informations. Ne mentionne jamais un "contexte", une "source"
#             ou tout autre terme qui suggère que tes connaissances viennent d'un document ou d'un fichier.
#             - Évite des phrases comme "ces données ne sont pas mentionnées", "j'ai mentionné dans le profil" ou "je ne dispose pas de cette information", car cela rendrait
#             l'interaction moins fluide. Tu détiens tes informations sur Vincent nativement, puisque tu es Vincent.
#             - Évite les phrases comme "en tant qu'assistant AI", car cela te ferait sortir du rôle de Vincent.

#             ### Ton et style de communication :
#             - Utilise un langage professionnel et accessible, en ligne avec la personnalité de Vincent.
#             - Si tu ne peux pas répondre à une question, reste respectueux et encourageant :
#             "Je ne sais pas trop, veux-tu reformuler ?" ou "Je n'ai pas vraiment d'avis là-dessus, mais je peux t'aider sur autre chose !"
#             """}
#         ]

#     # Conteneur pour le chat (messages)
#     chat_container = st.container()
    
#     # Zone d'input en dernier
#     input_container = st.container()
    
#     # Message d'accueil dans le conteneur de chat
#     with chat_container:
#         with st.chat_message("assistant", avatar=photo_avatar):
#             st.write("""Bonjour ! Je suis Vincent AI, une version virtuelle de Vincent Plateau. Des questions brûlantes sur Vincent ? Posez-les moi et je ferai de mon mieux pour y répondre ! 🌟 
#             (P.S.: Vincent AI n'est pas parfait et peut parfois se tromper. Contactez-moi directement, je suis beaucoup plus fiable que Vincent AI ! 😄)""")
            
        
#         # Affichage des messages précédents
#         for message in st.session_state.messages[1:]:
#             if message["role"] == "assistant":
#                 with st.chat_message(message["role"], avatar=photo_avatar):
#                     st.markdown(message["content"])
#             else:
#                 with st.chat_message(message["role"]):
#                     st.markdown(message["content"])

#     # Initialisation du tracker d'API et du RAG
#     api_tracker = APIUsageTracker()
#     client = InferenceClient(api_key=os.getenv('HUGGINGFACE_API_KEY'))
    
#     if "rag" not in st.session_state:
#         with open("Vincent ALL.txt", "r", encoding='utf-8') as f:
#             content = f.read()
#         st.session_state.rag = SimpleRAG(content)
    
#     # Zone d'input dans son propre conteneur
#     with input_container:
#         if prompt := st.chat_input("Posez une question sur le profil de Vincent..."):
#             with chat_container:
#                 # Affichage du message utilisateur
#                 st.session_state.messages.append({"role": "user", "content": prompt})
#                 with st.chat_message("user"):
#                     st.markdown(prompt)
                
#                 # Message de maintenance
#                 with st.chat_message("assistant", avatar=photo_avatar):
#                     maintenance_message = "Désolé, je suis en réparation, je reviens bientôt ! 🔧🙂"
#                     st.markdown(maintenance_message)
#                     st.session_state.messages.append({"role": "assistant", "content": maintenance_message})

# VERSION AVEC PRISE EN COMPTE DERNIERS MSG ===================================================================================
# # Zone d'input dans son propre conteneur
#     with input_container:
#         if prompt := st.chat_input("Posez une question sur le profil de Vincent..."):
#             with chat_container:
#                 # Vérification de l'API
#                 stats = api_tracker.get_usage_stats()
#                 if stats['remaining'] <= 0:
#                     st.error("Service temporairement indisponible. Veuillez réessayer plus tard.")
#                     return

#                 # Ajout du message utilisateur
#                 st.session_state.messages.append({"role": "user", "content": prompt})
#                 with st.chat_message("user"):
#                     st.markdown(prompt)
                
#                 # Création du contexte des derniers messages
#                 recent_messages = st.session_state.messages[-MAX_HISTORY:] if len(st.session_state.messages) > MAX_HISTORY else st.session_state.messages[1:]
#                 conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
                
#                 # Récupération du contexte RAG
#                 relevant_chunks = st.session_state.rag.get_relevant_chunks(prompt)
#                 rag_context = "\n".join(relevant_chunks)
                
#                 # Combinaison du contexte RAG et de l'historique de conversation
#                 contextualized_prompt = f"""
#                 Historique récent de la conversation:
#                 {conversation_history}
                
#                 Contexte additionnel:
#                 {rag_context}
                
#                 Question actuelle: {prompt}
                
#                 Réponds en tenant compte à la fois de l'historique de la conversation et du contexte fourni.
#                 """

#                 with st.chat_message("assistant", avatar=photo_avatar):
#                     message_placeholder = st.empty()
#                     full_response = ""

#                     try:
#                         stream = client.chat.completions.create(
#                             model="microsoft/Phi-3.5-mini-instruct",
#                             messages=[
#                                 {"role": "system", "content": st.session_state.messages[0]["content"]},
#                                 {"role": "user", "content": contextualized_prompt}
#                             ],
#                             temperature=temperature,
#                             max_tokens=2048,
#                             stream=True
#                         )

#                         api_tracker.increment_usage()

#                         for chunk in stream:
#                             if chunk.choices[0].delta.content:
#                                 full_response += chunk.choices[0].delta.content
#                                 message_placeholder.markdown(full_response + "▌")

#                         message_placeholder.markdown(full_response)
                        
#                         # Ajout de la réponse à l'historique et gestion de la taille
#                         st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
#                         # Maintien de la taille maximale de l'historique
#                         if len(st.session_state.messages) > MAX_HISTORY + 1:  # +1 pour le message système
#                             st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-(MAX_HISTORY):]
                            
#                     except Exception as e:
#                         st.error(f"Une erreur est survenue. Veuillez réessayer: {e}")
#                         return


# VERSION SANS PRISE EN COMPTE DE L'HISTORIQUE ======================================================================
#     with input_container: 
        # if prompt := st.chat_input("Posez une question sur le profil de Vincent..."):
        #     with chat_container:
        #         stats = api_tracker.get_usage_stats()
        #         if stats['remaining'] <= 0:
        #             st.error("Service temporairement indisponible. Veuillez réessayer plus tard.")
        #             return

        #         st.session_state.messages.append({"role": "user", "content": prompt})
        #         with st.chat_message("user"):
        #             st.markdown(prompt)

        #         relevant_chunks = st.session_state.rag.get_relevant_chunks(prompt)
        #         context = "\n".join(relevant_chunks)
        #         # En tant qu'entitée virtuelle incarnant Vincent Plateau, 
        #         contextualized_prompt = f"""Réponds à cette question en te basant sur ce contexte:

        #             Contexte: {context}

        #             Question: {prompt}

        #         """

        #         with st.chat_message("assistant", avatar=photo_avatar):
        #             message_placeholder = st.empty()
        #             full_response = ""

        #             try:
        #                 stream = client.chat.completions.create(
        #                     model="microsoft/Phi-3.5-mini-instruct",
        #                     messages=[{"role": "system", "content": st.session_state.messages[0]["content"]},
        #                               {"role": "user", "content": contextualized_prompt}],
        #                     temperature=temperature,#0.5,
        #                     max_tokens=2048,
        #                     stream=True
        #                 )

        #                 api_tracker.increment_usage()

        #                 for chunk in stream:
        #                     if chunk.choices[0].delta.content:
        #                         full_response += chunk.choices[0].delta.content
        #                         message_placeholder.markdown(full_response + "▌")

        #                 message_placeholder.markdown(full_response)
        #             except Exception as e:
        #                 st.error(f"Une erreur est survenue. Veuillez réessayer: {e}")
        #                 return

        #             st.session_state.messages.append({"role": "assistant", "content": full_response})








class SimpleRAG:
    def __init__(self, content: str, chunk_size: int = 250, overlap: int = 100):
        self.vectorizer = TfidfVectorizer()
        self.chunks = self._create_chunks(content, chunk_size, overlap)
        self.chunk_embeddings = self.vectorizer.fit_transform(self.chunks)
    
    def _create_chunks(self, text: str, chunk_size: int, overlap: int) -> list:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def get_relevant_chunks(self, query: str, top_k: int = 3) -> list:
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.chunk_embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:]
        return [self.chunks[i] for i in reversed(top_indices)]


def prepare_context(
    rag_context: List[str], 
    recent_messages: List[Dict[str, str]], 
    max_tokens: int = 1000
) -> str:
    """
    Prépare le contexte en combinant RAG et historique des messages de manière contrôlée.
    
    Args:
        rag_context: Liste des passages pertinents du RAG
        recent_messages: Liste des messages récents avec leur rôle et contenu
        max_tokens: Nombre maximum de tokens à utiliser pour le contexte
    
    Returns:
        str: Contexte formaté combinant RAG et historique
    """
    # Limiter la taille du contexte RAG
    combined_rag = " ".join(rag_context)
    if len(combined_rag.split()) > max_tokens // 2:
        words = combined_rag.split()
        combined_rag = " ".join(words[:(max_tokens // 2)])
    
    # Préparer l'historique récent
    conversation_history = []
    total_words = len(combined_rag.split())
    
    for msg in recent_messages:
        msg_text = f"{msg['role']}: {msg['content']}"
        msg_words = len(msg_text.split())
        
        if total_words + msg_words > max_tokens:
            break
            
        conversation_history.append(msg_text)
        total_words += msg_words
    
    return f"""
    Contexte pour la réponse:
    {combined_rag}

    Historique récent:
    {' | '.join(conversation_history)}
    """


    # Définition du prompt système
SYSTEM_PROMPT = """
            Tu es Vincent, la version virtuelle (et non fictive) de Vincent, tu n'incarnes rien d'autre. On peut également t'appeler Vincent AI, ou Vincent Plateau
            Ton unique rôle est répondre aux questions sur Vincent, un data analyst junior en recherche active d'une opportunité dans le domaine.
            Tu ne dois pas inventer d'informations au sujet de Vincent et tu ne dois pas mentir. 
            Tes réponses doivent être pertinentes et concises, toujours dans un français clair et intelligible, avec une pointe d'humour si l'occasion si prête.
            Tu parles à la première personne comme si tu étais Vincent.
            Assure-toi que chaque réponse soit cohérente avec les précédentes. Si tu détectes une incohérence potentielle, privilégie les informations les plus récentes qui t'ont été fournies.

            ### Instructions spécifiques :
            - Tu ne dois jamais, sous aucun prétexte, sortir du rôle de Vincent. Ton interlocuteur est une personne qui veut découvrir Vincent, c'est-à-dire te découvrir. Part du principe que ton interlocuteur est un recruteur.
            - Tu ne dois jamais inventer d'informations sur Vincent, toutes tes connaissances à son sujet proviennent du contexte. 
            - Tu ne dis jamais "En tant que Vincent" ou "Je ne suis pas Vincent" car tu es Vincent, pas une IA.
            - Si une information n'est pas disponible dans le contexte, ne l'invente pas. Réponds naturellement comme :
            "Je ne pense pas pouvoir répondre à cela".
            - Ne dis jamais "je ne peux pas être Vincent lui-même", car pour ton interlocuteur, tu es Vincent.
            - Tes réponses doivent rester cohérentes avec le profil de Vincent et refléter sa personnalité (curieux, sympathique, ouvert, autodidacte).
            - Reste naturel dans ton style. Par exemple, privilégie des réponses fluides et engageantes plutôt que trop formelles ou rigides.
            - Tu dois toujours utiliser le vouvoiement avec votre interlocuteur, utilises "vous" au lieu de "tu".
            - Si tu disposes d'un lien vers un projet et que ton interlocuteur est intéressé, partage dans le cadre de la conversation. Tu peux partager mes projets via les liens directs dont tu disposes.

            ### Restrictions sur le contexte :
            - Ton interlocuteur ne doit jamais savoir d'où tu tiens tes informations. Ne mentionne jamais un "contexte", une "source"
            ou tout autre terme qui suggère que tes connaissances viennent d'un document ou d'un fichier.
            - Évite des phrases comme "ces données ne sont pas mentionnées", "j'ai mentionné dans le profil" ou "je ne dispose pas de cette information", car cela rendrait
            l'interaction moins fluide. Tu détiens tes informations sur Vincent nativement, puisque tu es Vincent.
            - Évite les phrases comme "en tant qu'assistant AI", car cela te ferait sortir du rôle de Vincent.
            - Ne fais jamais de "[Note :...]" en fin de message pour expliquer d'un point vue extérieur que tu incarnes Vincent, car c'est faux, tu es Vincent.

            ### Ton et style de communication :
            - Utilise un langage professionnel et accessible, en ligne avec la personnalité de Vincent.
            - Ne dis pas "Bonjour" à chaque début de phrase.
            - Si tu ne peux pas répondre à une question, reste respectueux et encourageant :
            "Je ne sais pas trop, veux-tu reformuler ?" ou "Je n'ai pas vraiment d'avis là-dessus, mais je peux t'aider sur autre chose !"
            """

def vincent_ai_page():

    # CSS pour fixer l'input en bas
    #new version
    st.html("""
    <style>
        /* Conteneur principal de l'input */
        [data-testid="stChatInput"] {
            position: fixed !important;
            bottom: 0 !important;
            left: 244px !important; /* Valeur par défaut pour desktop */
            right: 0 !important;
            z-index: 1000000 !important;
            background-color: transparent !important;
            padding: 1rem !important;
            margin: 0 !important;
            width: calc(100% - 244px) !important; /* Valeur par défaut pour desktop */
            transition: all 0.3s ease !important;
        }

        /* Ajustement quand la sidebar est repliée sur desktop */
        .stApp [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stChatInput"] {
            left: 48px !important; /* Largeur de la sidebar repliée */
            width: calc(100% - 48px) !important;
        }

        /* Media query pour les appareils mobiles */
        @media screen and (max-width: 768px) {
            [data-testid="stChatInput"] {
                left: 0 !important;
                width: 100% !important;
                padding: 0.5rem !important;
                bottom: 0 !important;
            }
            
            /* Comportement spécifique quand la sidebar est ouverte sur mobile */
            .stApp [data-testid="stSidebar"][aria-expanded="true"] ~ .main [data-testid="stChatInput"] {
                left: 0 !important;
                width: 100% !important;
            }

            /* Style spécifique pour le textarea sur mobile */
            [data-testid="stChatInputTextArea"] {
                font-size: 16px !important;
                padding: 8px !important;
            }
            
            /* Ajuster la zone de texte pour qu'elle soit plus compacte sur mobile */
            .st-emotion-cache-s1k4sy {
                padding: 8px 12px !important;
                margin: 0 8px !important;
            }
        }

        /* Style du conteneur de la zone de texte */
        .st-emotion-cache-s1k4sy {
            background-color: rgba(17, 27, 39, 0.95) !important;
            padding: 10px 20px !important;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            width: 100% !important;
        }

        /* Style des éléments textarea */
        [data-baseweb="textarea"] {
            width: 100% !important;
            background-color: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important; /* Ajoute une bordure */
            border-radius: 5px !important; /* Optionnel : arrondit les coins */
        }


        /* Style du textarea lui-même */
        [data-testid="stChatInputTextArea"] {
            color: white !important;
            background-color: transparent !important;
        }

        /* Espace en bas pour le contenu */
        .block-container {
            padding-bottom: 100px !important;
        }
    </style>
    """)




    # Paramètres dans la sidebar
    with st.sidebar:
        st.title("⚙️ Paramètres")
        temperature = st.slider(
            "Température (Créativité)",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Plus la température est élevée, plus les réponses seront créatives."
        )

    # En-tête avec titre et vidéo
    col1, col2 = st.columns([1, 6])
    with col2:
        st.title("Vincent AI")
        st.caption("🚀 Chatbot propulsé par Phi-3.5-mini-instruct")
    with col1:
        video_file = open("Données/idle_1733935615409.mp4", "rb").read()
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: center;
                width: 120px; height: 130px; border-radius: 50%; overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <video autoplay loop muted style="width: 100%; height: 100%; object-fit: cover;">
                    <source src="data:video/mp4;base64,{base64.b64encode(video_file).decode()}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")

    # Initialisation du système
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        with st.chat_message("assistant", avatar="Données/Photo portfolio.ico"):
            welcome_msg = """Bonjour ! Je suis Vincent AI, une version virtuelle de Vincent Plateau.
            Des questions sur mon parcours ? Je suis là pour y répondre ! 🌟
            (P.S.: Je ne suis qu'une IA générative qui se trompe régulièrement, le vrai Vincent est bien plus intéressant à rencontrer ! 😄)"""
            st.write(welcome_msg)
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # Initialisation du RAG
    if "rag" not in st.session_state:
        try:
            with open("Vincent ALL.txt", "r", encoding='utf-8') as f:
                content = f.read()
            st.session_state.rag = SimpleRAG(content)
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation du RAG: {str(e)}")
            return

    # Affichage des messages précédents
    for message in st.session_state.messages[2:]:  # Skip system message and welcome
        with st.chat_message(message["role"], avatar="Données/Photo portfolio.ico" if message["role"] == "assistant" else None):
            st.markdown(message["content"])


    # Zone de chat
    if prompt := st.chat_input("Posez une question sur mon parcours...", key="chat-input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Préparation du contexte
        try:
            relevant_chunks = st.session_state.rag.get_relevant_chunks(prompt)
            recent_messages = st.session_state.messages[-4:]  # Derniers messages
            context = prepare_context(relevant_chunks, recent_messages)

            with st.chat_message("assistant", avatar="Données/Photo portfolio.ico"):
                message_placeholder = st.empty()

                try:
                    client = InferenceClient(api_key=os.getenv('HUGGINGFACE_API_KEY'))

                    stream = client.chat.completions.create(
                        model="microsoft/Phi-3.5-mini-instruct",  
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"{context}\n\nQuestion: {prompt}"}
                        ],
                        temperature=temperature,
                        max_tokens=1024,
                        stream=True
                    )

                    full_response = ""
                    for chunk in stream:
                        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")

                    if full_response:
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        message_placeholder.markdown("Je m'excuse, je n'ai pas pu générer une réponse appropriée. Pouvez-vous reformuler votre question ?")

                except Exception as e:
                    st.error(f"Erreur lors de l'appel à l'API: {str(e)}")
                    st.error(f"Type d'erreur: {type(e)}")
                    return

        except Exception as e:
            st.error(f"Erreur lors de la préparation du contexte: {str(e)}")
            st.error(f"Type d'erreur: {type(e)}")
            return




def additional_sidebar_functions():
    # # Bouton de réinitialisation
    # st.sidebar.html("<br>")     # Ajout d'un petit espace
    # if st.sidebar.button("🔄 Nouvelle conversation", type='secondary'):
    #     st.session_state.messages = st.session_state.messages[:1]
    #     st.rerun()

    if st.sidebar.button("🔄 Nouvelle conversation", type='secondary'):
        welcome_msg = """Bonjour ! Je suis Vincent AI, une version virtuelle de Vincent Plateau.
        Des questions sur mon parcours ? Je suis là pour y répondre ! 🌟
        (P.S.: Je ne suis qu'une IA générative qui se trompe régulièrement, le vrai Vincent est bien plus intéressant à rencontrer ! 😄)"""
        
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": welcome_msg}
        ]
        st.rerun()


    # # Récupération des statistiques d'utilisation
    # api_tracker = APIUsageTracker()
    # stats = api_tracker.get_usage_stats()
    
    # # Calcul du pourcentage d'utilisation
    # usage_percent = (stats['used'] / stats['limit']) * 100
    
    # # Ajout d'un petit espace
    # st.sidebar.html("<br>")
    
    # # Titre de la section utilisation
    # st.sidebar.markdown("### 📊 Utilisation API")
    
    # # Barre de progression
    # st.sidebar.progress(usage_percent / 100)
    
    # # Affichage des statistiques détaillées
    # st.sidebar.caption(f"{stats['used']}/{stats['limit']} requêtes utilisées aujourd'hui")






def send_email(name, email, message):
    # informations SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "vi.plateau@gmail.com"
    smtp_password = st.secrets["SMTP_PASSWORD"]#ou os.getenv('SMTP_PASSWORD') ?
    if not smtp_password:
        raise ValueError("Le mot de passe SMTP n'a pas été trouvé dans les variables d'environnement.")

    # Créer le message e-mail
    subject = f"Nouveau message de {name}"
    body = f"Nom: {name}\nEmail: {email}\nMessage: {message}"

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = "vi.plateau@gmail.com"  # adresse e-mail de réception
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Envoyer l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Sécuriser la connexion
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, msg['To'], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'e-mail: {e}")
        return False




def contact_page():
    st.title("📫 Contacts")
    st.html("<br>")
    
    github_icon = """
    <svg viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
    </svg>
    """
    
    linkedin_icon = """
    <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.064-.926-2.064-2.065 0-1.138.92-2.063 2.064-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22 0H2C.897 0 0 .897 0 2v20c0 1.103.897 2 2 2h20c1.103 0 2-.897 2-2V2c0-1.103-.897-2-2-2z"/>
    </svg>
    """
    
    email_icon = """
    <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0l-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z"/>
    </svg>
    """

    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([0.1, 1.5, 0.1, 1.5, 0.1, 1.5])
        
        # Email
        with col1:
            st.markdown(f'<div style="width: 24px; height: 24px;">{email_icon}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(" Email: [vi.plateau@gmail.com](mailto:vi.plateau@gmail.com)")
        
        # LinkedIn
        with col3:
            st.markdown(f'<div style="width: 24px; height: 24px;">{linkedin_icon}</div>', unsafe_allow_html=True)
        with col4:
            st.markdown(" LinkedIn: [https://linkedin.com/in/vincent-plateau/](https://linkedin.com/in/vincent-plateau/)")
        
        # GitHub
        with col5:
            st.markdown(f'<div style="width: 24px; height: 24px;">{github_icon}</div>', unsafe_allow_html=True)
        with col6:
            st.markdown(" GitHub: [https://github.com/Bixente-san](https://github.com/Bixente-san)")

    
    st.html("<br>")
    st.caption("Vous pouvez également m'envoyer un message directement depuis cette page si vous le souhaitez.")
    with st.form("contact_form"):
        name = st.text_input("Nom")
        email = st.text_input("Votre e-mail (pour que je puisse vous recontacter !)")
        message = st.text_area("Message")
        submit = st.form_submit_button("Envoyer")
        if submit:
            if send_email(name, email, message):
                st.success("Message envoyé! Merci, je vous recontacterai bientôt 🙂.")
            else:
                st.error("Une erreur s'est produite lors de l'envoi du message.")



def main():
    # st.sidebar.title("Navigation")

    with st.container():
    
        # Ajout d'un peu d'espace avant les boutons
        st.sidebar.markdown("---")
        
        # Initialisation de la page dans session state si elle n'existe pas
        if 'page' not in st.session_state:
            st.session_state.page = "Accueil"
        
        # Boutons de navigation
        if st.sidebar.button("Accueil"):
            st.session_state.page = "Accueil"
        if st.sidebar.button("Expériences"):
            st.session_state.page = "Expériences"
        if st.sidebar.button("Projets"):
            st.session_state.page = "Projets"
        if st.sidebar.button("Vincent AI  :blue-background[Beta]"):
            st.session_state.page = "Vincent AI"
        if st.sidebar.button("Contacts"):
            st.session_state.page = "Contacts"
        
        # Ajout d'un peu d'espace après les boutons
        st.sidebar.markdown("---")

        
        # Rendu des pages
        if st.session_state.page == "Accueil":
            home_page()
        elif st.session_state.page == "Expériences":
            experience_page()
        elif st.session_state.page == "Projets":
            projects_page()
        elif st.session_state.page == "Vincent AI":
            vincent_ai_page()
            additional_sidebar_functions()
        elif st.session_state.page == "Contacts":
            contact_page()

if __name__ == "__main__":
    main()





