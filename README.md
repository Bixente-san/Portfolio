# Portfolio Interactif d'un Analyste de Données

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

- **Framework principal**: Python/Streamlit
- **Visualisation de données**: Plotly, Folium
- **IA et NLP**: Hugging Face (Phi-3.5-mini-instruct)
- **Gestion des documents**: PyPDF2, docx
- **Traitement des données**: Pandas, NumPy
- **RAG System**: TF-IDF, Cosine Similarity

## Installation

```bash
# Cloner le repository
git clone https://github.com/votre-username/portfolio-data-analyst.git

# Se déplacer dans le dossier
cd portfolio-data-analyst

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## Configuration requise

Pour exécuter l'application, vous aurez besoin de :

- Python 3.8 ou version supérieure
- Les packages listés dans requirements.txt
- Une clé API Hugging Face pour le chatbot (à configurer dans config.py)

## Structure du projet

```
portfolio/
│
├── app.py                # Point d'entrée de l'application
├── requirements.txt      # Dépendances du projet
├── config.py            # Configuration et variables d'environnement
│
├── data/                # Données et ressources
│   ├── images/         
│   ├── documents/      
│   └── corpus/         
│
├── src/                 # Code source
│   ├── pages/          # Pages du portfolio
│   ├── components/     # Composants réutilisables
│   └── utils/          # Fonctions utilitaires
│
└── tests/              # Tests unitaires et d'intégration
```

## Contribution

Les suggestions et contributions sont les bienvenues. Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Déploiement

L'application peut être déployée sur Streamlit Cloud ou sur votre propre serveur. Pour le déploiement sur Streamlit Cloud, suivez la [documentation officielle](https://docs.streamlit.io/streamlit-cloud).

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Contact

Vincent PLATEAU - vi.plateau@gmail.com  
Lien du projet: [https://github.com/votre-username/portfolio-data-analyst](https://github.com/votre-username/portfolio-data-analyst)

---
Développé avec ❤️ par Vincent PLATEAU
