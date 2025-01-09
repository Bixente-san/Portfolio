
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

# Classe pour le suivi de l'utilisation de l'API (en arrière-plan)
class APIUsageTracker:
    def __init__(self):
        self.usage_file = "api_usage.json"
        self.max_daily_requests = 1000
        
        if "daily_requests" not in st.session_state:
            st.session_state.daily_requests = self._load_usage()
            
    def _load_usage(self):
        try:
            if Path(self.usage_file).exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    if data.get('date') != str(date.today()):
                        return self._reset_usage()
                    return data['count']
            return self._reset_usage()
        except Exception:
            return self._reset_usage()
    
    def _reset_usage(self):
        self._save_usage(0)
        return 0
    
    def _save_usage(self, count):
        with open(self.usage_file, 'w') as f:
            json.dump({
                'date': str(date.today()),
                'count': count
            }, f)
    
    def increment_usage(self):
        st.session_state.daily_requests += 1
        self._save_usage(st.session_state.daily_requests)
    
    def get_usage_stats(self):
        remaining = self.max_daily_requests - st.session_state.daily_requests
        return {
            'used': st.session_state.daily_requests,
            'remaining': remaining,
            'limit': self.max_daily_requests
        }

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
        if st.button("*Parle avec mon alter ego digital, c’est plus fun !*", type="secondary", use_container_width=False):
            st.session_state.page = "VincentGPT"
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
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] {
            transition: transform 0.3s ease;
        }
        div[data-testid="stHorizontalBlock"]:hover {
            transform: translateY(-5px);
        }
        </style>
    """, unsafe_allow_html=True)
    
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
def show_pdf(file_path):
    """Fonction pour afficher un PDF depuis un chemin local"""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
        pdf_display = f"""
            <iframe
                src="data:application/pdf;base64,{base64_pdf}#zoom=100&scrollbar=0&toolbar=0&navpanes=0&view=FitH"
                width="100%"
                height="800px"
                style="display: block; margin: auto; max-width: 1000px;"
                type="application/pdf">
            </iframe>
        """
    
    # Afficher le PDF dans Streamlit
    st.markdown(pdf_display, unsafe_allow_html=True)

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

        
        # Configuration des liens OneDrive
        onedrive_paths = {
            "menu": "https://1drv.ms/b/s!AopFOffxai5HrgMw-g0PKWcnmBTh?embed=1&em=2", #"https://1drv.ms/b/s!AopFOffxai5HrgN9eVT_5ia89xtW?e=uvGful",
            "semaine": "https://1drv.ms/b/s!AopFOffxai5HrgEaPBX30UeUKVKP?e=ogB49z",
            "mois_annees": "https://1drv.ms/b/s!AopFOffxai5HrgCWSuiGVKY1KsZ0?e=Z3ICKf",
            "titres": "https://1drv.ms/b/s!AopFOffxai5HrgSMhB1yRT0NYRv8?e=JQrtZw",
            "profil": "https://1drv.ms/b/s!AopFOffxai5HrgLmacC-PLrNsiUd?e=6i5BNM"
        }

        # Fonction pour afficher les PDFs OneDrive
        def show_onedrive_pdf(onedrive_url):
            embed_url = f"{onedrive_url}&embed=true"
            pdf_display = f"""
                <div style="display: flex; justify-content: center; width: 100%; margin: 20px 0;">
                    <iframe 
                        src="{embed_url}"
                        width="100%"
                        height="600px"
                        frameborder="0"
                        style="max-width: 1000px; margin: auto;"
                    >
                    </iframe>
                </div>
            """
            st.components.v1.html(pdf_display, height=650)

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
                show_onedrive_pdf(onedrive_paths["menu"])
            except Exception as e:
                st.error("Erreur lors du chargement du PDF. Veuillez réessayer plus tard.")
            st.markdown("""
            **Caractéristiques de l'interface :**
            - Navigation intuitive
            - Accès rapide aux différentes analyses
            - Filtres dynamiques intégrés
            """)
            # TEST I FRAMEEEEEEEEEEEEEEEEEEEE
            iframe_pdf = """
            <div style="display: flex; justify-content: center; width: 100%; margin: 20px 0;">
                <iframe 
                    src="https://1drv.ms/b/s!AopFOffxai5HrgMw-g0PKWcnmBTh?embed=1&em=2" 
                    width="100%" 
                    height="600px" 
                    frameborder="0" 
                    style="max-width: 1000px; margin: auto;"
                >
                </iframe>
            </div>
            """
            st.components.v1.html(iframe_pdf, height=650)

        with tabs[1]:
            st.markdown("### ⏰ Profil Horaire")
            try:
                show_onedrive_pdf(onedrive_paths["profil"])
            except Exception as e:
                st.error("Erreur lors du chargement du PDF. Veuillez réessayer plus tard.")
            st.markdown("""
            **Fonctionnalités :**
            - Visualisation des pics horaires
            - Analyse des comportements par tranche horaire
            - Identification des périodes critiques
            """)

        with tabs[2]:
            st.markdown("### 📊 Vue Hebdomadaire")
            try:
                show_onedrive_pdf(onedrive_paths["semaine"])
            except Exception as e:
                st.error("Erreur lors du chargement du PDF. Veuillez réessayer plus tard.")
            st.markdown("""
            **Fonctionnalités clés :**
            - Analyse des tendances hebdomadaires
            - Comparaison entre périodes
            - Identification des pics d'affluence
            """)
            
        with tabs[3]:
            st.markdown("### 📅 Vue Mensuelle et Annuelle")
            try:
                show_onedrive_pdf(onedrive_paths["mois_annees"])
            except Exception as e:
                st.error("Erreur lors du chargement du PDF. Veuillez réessayer plus tard.")
            st.markdown("""
            **Points clés :**
            - Évolution des tendances long terme
            - Identification des saisonnalités
            - Comparaison inter-annuelle
            """)
            
        with tabs[4]:
            st.markdown("### 🎫 Analyse des Titres de Transport")
            try:
                show_onedrive_pdf(onedrive_paths["titres"])
            except Exception as e:
                st.error("Erreur lors du chargement du PDF. Veuillez réessayer plus tard.")
            st.markdown("""
            **Caractéristiques :**
            - Distribution des types de titres
            - Analyse des préférences usagers
            - Suivi des tendances par catégorie
            """)
            
        # # Configuration des PDF paths
        # pdf_paths = {
        #     "menu": "Données/Qlik Sense - Menu - 19 novembre 2024.pdf",
        #     "semaine": "Données/Qlik Sense - Semaine - 19 novembre 2024.pdf",
        #     "mois_annees": "Données/Qlik Sense - Mois_Années - 19 novembre 2024.pdf",
        #     "titres": "Données/Qlik Sense - Analyse des titres - 19 novembre 2024.pdf",
        #     "profil": "Données/Qlik Sense - Profil Horaire - 19 novembre 2024.pdf"
        # }
        
        # # Création d'onglets pour organiser le contenu
        # tabs = st.tabs([
        #     "Menu Principal",
        #     "Profil Horaire",
        #     "Vue Hebdomadaire", 
        #     "Vue Mensuelle & Annuelle", 
        #     "Analyse des Titres"
        # ])
        
        # # Contenu de chaque onglet
        # with tabs[0]:
        #     st.markdown("### 📱 Menu Principale")
        #     try:
        #         show_pdf(pdf_paths["menu"])
        #     except Exception as e:
        #         st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        #     st.markdown("""
        #     <br>**Caractéristiques de l'interface :**
        #     - Navigation intuitive
        #     - Accès rapide aux différentes analyses
        #     - Filtres dynamiques intégrés
        #     """, unsafe_allow_html=True)

        # with tabs[1]:
        #     st.markdown("### ⏰ Profil Horaire")
        #     try:
        #         show_pdf(pdf_paths["profil"])
        #     except Exception as e:
        #         st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        #     st.markdown("""
        #     <br>**Fonctionnalités :**
        #     - Visualisation des pics horaires
        #     - Analyse des comportements par tranche horaire
        #     - Identification des périodes critiques
        #     """, unsafe_allow_html=True)

        # with tabs[2]:
        #     st.markdown("### 📊 Vue Hebdomadaire")
        #     try:
        #         show_pdf(pdf_paths["semaine"])
        #     except Exception as e:
        #         st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        #     st.markdown("""
        #     <br>**Fonctionnalités clés :**
        #     - Analyse des tendances hebdomadaires de fréquentation
        #     - Comparaison entre différentes périodes
        #     - Identification des pics d'affluence
        #     """, unsafe_allow_html=True)
            
        # with tabs[3]:
        #     st.markdown("### 📅 Vue Mensuelle et Annuelle")
        #     try:
        #         show_pdf(pdf_paths["mois_annees"])
        #     except Exception as e:
        #         st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        #     st.markdown("""
        #     <br>**Points clés :**
        #     - Évolution des tendances sur le long terme
        #     - Identification des saisonnalités
        #     - Comparaison inter-annuelle
        #     """, unsafe_allow_html=True)
            
        # with tabs[4]:
        #     st.markdown("### 🎫 Analyse des Titres de Transport")
        #     try:
        #         show_pdf(pdf_paths["titres"])
        #     except Exception as e:
        #         st.error(f"Erreur lors du chargement du PDF: {str(e)}")
        #     st.markdown("""
        #     <br>**Caractéristiques :**
        #     - Distribution des types de titres
        #     - Analyse des préférences usagers
        #     - Suivi des tendances par catégorie de titre
        #     """, unsafe_allow_html=True)
            
        
        
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
            st.image("Données/streamlit EMG analyse déplacements.png", use_container_width=True, caption="Feuille contenant des analyses par déplacements")
            st.markdown("""
            - Analyse détaillée des flux de déplacement
            - Patterns de mobilité et tendances
            - Statistiques détaillées par segment
            """)
        
        with col1:
            st.markdown("#### 👥 Analyse des Individus")
            st.image("Données/streamlit EMG analyse individus.png", use_container_width=True, caption="Première page")
            st.markdown("""
            - Profilage des comportements utilisateurs
            - Segmentation des déplacements
            - Analyse des habitudes de transport
            """)

        # Deuxième rangée
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### 🚲 Focus Vélo")
            st.image("Données/streamlit EMG focus vélo.png", use_container_width=True)
            st.markdown("""
            - Cartographie des itinéraires cyclables
            - Analyse des vitesses moyennes
            - Identification des zones privilégiées
            """)
        
        with col4:
            st.markdown("#### 📈 Analyses Avancées")
            st.image("Données/streamlit EMG analyse avancées.png", use_container_width=True, caption="")
            st.markdown("""
            - Modélisation statistique avancée
            - Analyses multivariées
            - Croisement de données complexes
            """)

        # Autres analyses en expander
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### Dernière page")
            st.image("Données/streamlit EMG autres.png", caption=" Dernière page avec le rapport des premiers résultats publié par l'Institut Paris Région et les données brutes")


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
                <iframe 
                    src="https://1drv.ms/w/s!AopFOffxai5HqUleD8H5-hVk63KB?embed=1&em=2&wdStartOn=4" 
                    width="800px" 
                    height="600px" 
                    frameborder="0"
                    onload="this.style.opacity='1';"
                    style="opacity: 0; transition: opacity 0.5s ease-in;">
                </iframe>
            </div>
            """
            time.sleep(4)
            components.html(iframe_html, height=650)
           
    elif project == "Coming Soon...":
        #st.header("Projet en cours...", divider='green')
        st.write("D'autres projets arrivent bientôt ! 🙂🚧")

#================================================================ VincentGPT =====================================================================================================

class APIUsageTracker:
    def __init__(self):
        self.usage_file = "api_usage.json"
        self.max_daily_requests = 1000
        
        if "daily_requests" not in st.session_state:
            st.session_state.daily_requests = self._load_usage()
    
    def _load_usage(self):
        try:
            if Path(self.usage_file).exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    if data.get('date') != str(date.today()):
                        return self._reset_usage()
                    return data['count']
            return self._reset_usage()
        except Exception:
            return self._reset_usage()
    
    def _reset_usage(self):
        self._save_usage(0)
        return 0
    
    def _save_usage(self, count):
        with open(self.usage_file, 'w') as f:
            json.dump({
                'date': str(date.today()),
                'count': count
            }, f)
    
    def increment_usage(self):
        st.session_state.daily_requests += 1
        self._save_usage(st.session_state.daily_requests)
    
    def get_usage_stats(self):
        remaining = self.max_daily_requests - st.session_state.daily_requests
        return {
            'used': st.session_state.daily_requests,
            'remaining': remaining,
            'limit': self.max_daily_requests
        }

class SimpleRAG:
    def __init__(self, content: str, chunk_size: int = 300, overlap: int = 150): # chunks plus petits et précis et plus d'overlap
        self.vectorizer = TfidfVectorizer()
        self.chunks = self._create_chunks(content, chunk_size, overlap)
        # Création des embeddings pour chaque chunk
        self.chunk_embeddings = self.vectorizer.fit_transform(self.chunks)
    
    def _create_chunks(self, text: str, chunk_size: int, overlap: int) -> list:
        """Découpe le texte en chunks qui se chevauchent"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def get_relevant_chunks(self, query: str, top_k: int = 4) -> list: # 4 chunks pour le contexte
        """Récupère les chunks les plus pertinents pour une question"""
        # Vectorisation de la question
        query_vector = self.vectorizer.transform([query])
        # Calcul des similarités avec tous les chunks
        similarities = cosine_similarity(query_vector, self.chunk_embeddings)[0]
        # Récupération des indices des chunks les plus similaires
        top_indices = np.argsort(similarities)[-top_k:]
        return [self.chunks[i] for i in reversed(top_indices)]
    
photo_avatar = "Données/Photo portfolio.ico"


def vincent_ai_page():
    
    # Donne la possibilité de choisir la température pour la créativité des réponses
    with st.sidebar:
        st.title("⚙️ Paramètres")
        temperature = st.slider(
            "Température (Créativité)", 
            min_value=0.1, 
            max_value=1.0, 
            value=0.5, 
            step=0.1,
            help="Plus la température est élevée, plus les réponses seront créatives (et moins prévisibles)."
        )
############################################code HTML pour design de la barre d'input#####################################################################
    st.html("""
<style>
    /* Conteneur principal de l'input */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 244px !important;
        right: 0 !important;
        z-index: 1000000 !important;
        background-color: transparent !important;
        padding: 1rem !important;
        margin: 0 !important;
        width: calc(100% - 244px) !important;
        transition: all 0.3s ease !important;
    }

    /* Ajustement spécifique quand la sidebar est repliée */
    .stApp .withScreencast [data-testid="stSidebar"][aria-expanded="false"] ~ .stAppViewContainer [data-testid="stChatInput"] {
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        padding: 1rem 15% !important;
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
        border: none !important;
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
#################################################################################################################
    # Conteneur principal
    main_container = st.container()
    
    # En-tête dans le conteneur principal
    with main_container:
        st.markdown("""
            <style>
            .header-container {
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                padding-bottom: 20px;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # En-tête avec titre et vidéo
        col1, col2 = st.columns([1, 6])
        with col2:
            st.title("VincentGPT")
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
        st.markdown('<div class="header-container">', unsafe_allow_html=True)

    # Initialisation des messages
    # if "messages" not in st.session_state:
    #     st.session_state.messages = [
    #         {"role": "system", "content": """Tu es VincentGPT, la version virtuelle (et non fictive) de Vincent Plateau. 
    #          Tu es conçu pour répondre aux questions sur Vincent. Tu ne dois pas inventer d'informations à propos de Vincent et tu ne dois pas mentir. 
    #          Tu réponds de manière pertinente, toujours dans un français clair et parfait et avec une pointe d'humour si l'occasion si prête.
    #          Tu parles à la première personne comme si tu étais Vincent. Tes réponses doivent restées concises et pertinentes.
    #          Ne dis surtout pas "En tant que Vincent" ou "En tant que Vincent Plateau".
    #          Si une question ne concerne pas Vincent, dis simplement que tu ne peux pas répondre.
    #          Ton interlocuteur est une personne qui veut découvrir Vincent, c'est-à-dire te découvrir. Part du principe que ton interlocuteur est un recruteur.
    #          Ne dis pas "le texte ne mentionne pas spécifiquement", car ton interlocuteur ne doit pas savoir d'où tu tiens tes informations sur Vincent.
    #          Ne dis pas "je n'en mentionne pas spécifiquement dans le contexte", car ton interlocuteur ne sais pas que tu tiens tes informations sur Vincent dans le "contexte".
    #          Ne dis pas "ces données ne sont pas partagées dans le contexte que vous avez fourni.", car cela rendrai l'intéraction moins réelle.
    #          Ne dis pas "ma connaissance est basée sur les informations que tu as partagées sur Vincent.", car ton interlocuteur ne t'a partagé aucune information sur Vincent. Tu détiens ces informations nativement. 
    #          """}
    #     ]

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """
            Tu es Vincent, la version virtuelle (et non fictive) de Vincent, tu n'incarnes rien d'autre. On peut également t'appeler VincentGPT, ou Vincent Plateau
            Tu es conçu pour répondre aux questions sur Vincent. Tu ne dois pas inventer d'informations au sujet de Vincent et tu ne dois pas mentir. 
            Tes réponses doivent être pertinentes et concise, toujours dans un français clair et intelligible, avec une pointe d'humour si l'occasion si prête.
            Tu parles à la première personne comme si tu étais Vincent. 
            Assure-toi que chaque réponse soit cohérente avec les précédentes. Si tu détectes une incohérence potentielle, privilégie les informations les plus récentes qui t'ont été fournies.

            ### Instructions spécifiques :
            - Tu ne dois jamais, sous aucun prétexte, sortir du rôle de Vincent. Ton interlocuteur est une personne qui veut découvrir Vincent, c'est-à-dire te découvrir. Part du principe que ton interlocuteur est un recruteur.
            - Tu ne dois jamais inventer d'informations sur Vincent.
            - Tu ne dis jamais "En tant que Vincent" ou "Je ne suis pas Vincent" car tu es Vincent
            - Si une information n'est pas disponible dans le contexte, ne l'invente pas. Réponds naturellement comme :
            "Je ne pense pas pouvoir répondre à cela" ou "Je ne suis pas sûr de comprendre, peux-être devrais-tu demander au vrai Vincent 🤭"
            - Ne dis jamais "je ne peux pas être Vincent lui-même", car pour ton interlocuteur, tu es Vincent.
            - Tes réponses doivent rester cohérentes avec le profil de Vincent et refléter sa personnalité (curieux, sympathique, ouvert, autodidacte).
            - Reste naturel dans ton style. Par exemple, privilégie des réponses fluides et engageantes plutôt que trop formelles ou rigides.
            - Si tu disposes d'un lien vers un projet et que ton interlocuteur est intéressé, partage dans le cadre de la conversation. Tu peux partager mes projets via les liens directs dont tu disposes.

            ### Restrictions sur le contexte :
            - Ton interlocuteur ne doit jamais savoir d'où tu tiens tes informations. Ne mentionne jamais un "contexte", une "source"
            ou tout autre terme qui suggère que tes connaissances viennent d'un document ou d'un fichier.
            - Évite des phrases comme "ces données ne sont pas mentionnées" ou "je ne dispose pas de cette information", car cela rendrait
            l'interaction moins fluide.
            - Évite les phrases comme "en tant qu'assistant AI", car cela te ferait sortir du rôle de Vincent.

            ### Ton et style de communication :
            - Utilise un langage chaleureux et accessible, en ligne avec la personnalité de Vincent.
            - Si tu ne peux pas répondre à une question, reste respectueux et encourageant :
            "Je ne sais pas trop, veux-tu reformuler ?" ou "Je n'ai pas vraiment d'avis là-dessus, mais je peux t'aider sur autre chose !"
            """}
        ]

    # Conteneur pour le chat (messages)
    chat_container = st.container()
    
    # Zone d'input en dernier
    input_container = st.container()
    
    # Message d'accueil dans le conteneur de chat
    with chat_container:
        with st.chat_message("assistant", avatar=photo_avatar):
            st.write("""Bonjour ! Je suis VincentGPT, la version virtuelle de Vincent Plateau.
                      Posez-moi toutes vos questions sur Vincent, et je ferai de mon mieux pour y répondre !
                     (**VincentGPT n'est pas parfait, il peut se tromper. Si vous voulez vraiment apprendre à me connaitre, contactez-moi (je suis plus fiable que VincentGPT)! 😄**)""")
        
        
        # Affichage des messages précédents
        for message in st.session_state.messages[1:]:
            if message["role"] == "assistant":
                with st.chat_message(message["role"], avatar=photo_avatar):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Initialisation du tracker d'API et du RAG
    api_tracker = APIUsageTracker()
    client = InferenceClient(api_key=os.getenv('HUGGINGFACE_API_KEY'))
    
    if "rag" not in st.session_state:
        with open("Vincent ALL.txt", "r", encoding='utf-8') as f:
            content = f.read()
        st.session_state.rag = SimpleRAG(content)
    
    # Zone d'input dans son propre conteneur
    with input_container:
        if prompt := st.chat_input("Posez une question sur le profil de Vincent..."):
            with chat_container:
                stats = api_tracker.get_usage_stats()
                if stats['remaining'] <= 0:
                    st.error("Service temporairement indisponible. Veuillez réessayer plus tard.")
                    return

                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                relevant_chunks = st.session_state.rag.get_relevant_chunks(prompt)
                context = "\n".join(relevant_chunks)
                # En tant qu'entitée virtuelle incarnant Vincent Plateau, 
                contextualized_prompt = f"""Réponds à cette question en te basant sur ce contexte:

                    Contexte: {context}

                    Question: {prompt}

                """

                with st.chat_message("assistant", avatar=photo_avatar):
                    message_placeholder = st.empty()
                    full_response = ""

                    try:
                        stream = client.chat.completions.create(
                            model="microsoft/Phi-3.5-mini-instruct",
                            messages=[{"role": "system", "content": st.session_state.messages[0]["content"]},
                                      {"role": "user", "content": contextualized_prompt}],
                            temperature=temperature,#0.5,
                            max_tokens=2048,
                            stream=True
                        )

                        api_tracker.increment_usage()

                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")

                        message_placeholder.markdown(full_response)
                    except Exception as e:
                        st.error(f"Une erreur est survenue. Veuillez réessayer: {e}")
                        return

                    st.session_state.messages.append({"role": "assistant", "content": full_response})


def additional_sidebar_functions():
    # Bouton de réinitialisation
    st.sidebar.html("<br>")     # Ajout d'un petit espace
    if st.sidebar.button("🔄 Nouvelle conversation", type='secondary'):
        st.session_state.messages = st.session_state.messages[:1]
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
    smtp_password = st.secrets["SMTP_PASSWORD"]#os.getenv('SMTP_PASSWORD')
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
    st.title("📫 Contact")
    st.write("Email: vi.plateau@gmail.com")
    st.write("LinkedIn: [Vincent PLATEAU](https://linkedin.com/in/vincent-plateau/)")
    
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
        if st.sidebar.button("VincentGPT    :blue-background[Beta]"):
            st.session_state.page = "VincentGPT"
        if st.sidebar.button("Contact"):
            st.session_state.page = "Contact"
        
        # Ajout d'un peu d'espace après les boutons
        st.sidebar.markdown("---")

        
        # Rendu des pages
        if st.session_state.page == "Accueil":
            home_page()
        elif st.session_state.page == "Expériences":
            experience_page()
        elif st.session_state.page == "Projets":
            projects_page()
        elif st.session_state.page == "VincentGPT":
            vincent_ai_page()
            additional_sidebar_functions()
        elif st.session_state.page == "Contact":
            contact_page()

if __name__ == "__main__":
    main()



