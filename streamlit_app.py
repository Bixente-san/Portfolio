import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="Mon Portfolio", layout="wide")

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Aller à", ["Accueil", "Expérience", "Compétences", "Projets", "Contact"])

    # Contenu principal
    if page == "Accueil":
        st.title("Bienvenue sur mon Portfolio")
        st.write("Je suis Vincent PLATEAU, un professionnel passionné en analyse de donnée.")
        # Vous pouvez ajouter une image de profil ici
        image = Image.open(r"C:\Users\vyuof\OneDrive\Images\Pellicule\WIN_20240312_10_42_20_Pro.jpg")
        st.image(image, caption="Vincent", width=300)

    elif page == "Expérience":
        st.title("Expérience Professionnelle")
        st.write("### Entreprise A")
        st.write("Poste: Développeur Full Stack")
        st.write("Période: 2018 - Présent")
        st.write("Responsabilités:")
        st.write("- Développement d'applications web")
        st.write("- Gestion de projets agiles")

        st.write("### Entreprise B")
        st.write("Poste: Développeur Front-end Junior")
        st.write("Période: 2016 - 2018")
        st.write("Responsabilités:")
        st.write("- Création d'interfaces utilisateur réactives")
        st.write("- Collaboration avec l'équipe de design")

    elif page == "Compétences":
        st.title("Compétences Techniques")
        col1, col2 = st.columns(2)
        with col1:
            st.write("- Python")
            st.write("- JavaScript")
            st.write("- React")
        with col2:
            st.write("- SQL")
            st.write("- Git")
            st.write("- Docker")

    elif page == "Projets":
        st.title("Projets Personnels")
        st.write("### Projet 1: Application de Gestion de Tâches")
        st.write("Technologies utilisées: React, Node.js, MongoDB")
        st.write("Description: Une application web permettant aux utilisateurs de gérer leurs tâches quotidiennes.")

        st.write("### Projet 2: Bot Discord pour la Modération")
        st.write("Technologies utilisées: Python, Discord API")
        st.write("Description: Un bot Discord automatisant la modération des serveurs.")

    elif page == "Contact":
        st.title("Contactez-moi")
        st.write("Email: vi.plateau@gmail.com")
        st.write("LinkedIn: [Votre profil LinkedIn]")
        st.write("GitHub: [Votre profil GitHub]")

        # Formulaire de contact simple
        with st.form("contact_form"):
            name = st.text_input("Nom")
            email = st.text_input("Email")
            message = st.text_area("Message")
            submit = st.form_submit_button("Envoyer")
            if submit:
                st.success("Message envoyé! Je vous recontacterai bientôt.")

if __name__ == "__main__":
    main()