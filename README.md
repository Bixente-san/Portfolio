# Mon portfolio 

## À propos du projet

Ce portfolio a été développé avec Streamlit pour présenter de manière interactive mes compétences et projets en analyse de données. L'application offre une expérience utilisateur fluide et moderne, permettant aux visiteurs d'explorer mon parcours professionnel, mes réalisations et mes compétences techniques.

## Fonctionnalités principales

Le portfolio comprend plusieurs sections clés pour une présentation complète :

- Une page d'accueil avec un aperçu de mon profil et mes compétences principales
- Une section expérience détaillant mon parcours professionnel
- Une présentation interactive des projets data avec visualisations dynamiques
- Un chatbot IA (VincentGPT) pour une interaction personnalisée
- Une section contact pour les opportunités professionnelles

## Technologies utilisées

- Framework et Interface Utilisateur

Streamlit : Framework principal pour le développement de l'application web
PIL (Python Imaging Library) : Gestion et manipulation des images

- Modèle de langage / IA

Hugging Face Hub : Intégration du modèle de langage pour le chatbot
Scikit-learn : Implémentation du système RAG avec TF-IDF et calculs de similarité cosinus
NumPy : Support pour les opérations mathématiques et le traitement des données

- Gestion des Données et Fichiers

JSON : Stockage et manipulation des données structurées
Pathlib : Gestion des chemins de fichiers cross-platform
Base64 : Encodage des fichiers multimédias pour l'affichage web

- Communication

SMTP : Gestion de l'envoi d'emails via le formulaire de contact
MIME : Formatage des emails avec pièces jointes et contenus enrichis

## Structure du projet

La structure du projet est restée volontairement simple. Pour aller plus vite, tous le programme est dans un seul fichier python (c'est moins pro mais c'est volontaire !).
```
portfolio/
│
├── portfolio_streamlit.py     # Point d'entrée de l'application
├── requirements.txt           # Dépendances du projet
├── config.py                  # Configuration et variables d'environnement
├── Vincent ALL.txt            # Texte contenant des infos sur moi pour RAG
│
└──Données/                # Données et ressources
    └── images                
```

## Contribution

Les suggestions et contributions sont les bienvenues. 


## Contact

Vincent PLATEAU - vi.plateau@gmail.com  
Lien du projet: [https://portfolio-vincent-plateau.streamlit.app/](https://portfolio-vincent-plateau.streamlit.app/)

---
Développé par Vincent PLATEAU (avec l'aide bienveillante de quelques IA)
