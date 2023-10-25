import numpy as np
import pandas as pd
import pickle
import streamlit as st
import base64

def main():
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
            }
            .header {
                color: #2E4053;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .subheader {
                color: white;
                font-size: 24px;
                margin-bottom: 10px;
            }
            .markdown-text {
                color: gold;
                font-size: 18px;
                margin-bottom: 30px;
            }
            .sidebar-header {
                color: #2E4053;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .result {
                color: #e74c3c;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    def set_background(image_file):
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image_data}");
            background-size: cover;
            background-position: bottom; /* Ajout de cette ligne pour ajuster la position de l'image */
            height: 125vh; /* Hauteur à 100% de la hauteur de la vue */
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    # Utilisez la fonction set_background pour définir l'arrière-plan avec "logo.jpg"
    set_background("image/bg2.jpg")
    
    st.markdown('<p class="header">Analyse de l’attrition des employés d’une entreprise</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">ODILIA SOME & MOHAMED DIOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="markdown-text"><strong>MASTER 2 BUSINESS INTELLIGENCE & BIG DATA</strong></p>', unsafe_allow_html=True)

    def input_features():
        st.sidebar.markdown('<p class="sidebar-header">Faire glisser pour modifier les variables</p>', unsafe_allow_html=True)
        
        age = st.sidebar.slider('Âge de l\'employé', 18, 65, 30)
        
        dep_options = ['Ventes', 'Ressources humaines', 'Recherche et développement']
        dep = st.sidebar.selectbox('Département', dep_options)
        dept = 0 if dep == "Ventes" or dep == "Ressources humaines" else 1

        distancefromhome = st.sidebar.slider('Distance du domicile (km)', 0, 50, 5)
        
        efield_options = ['Ressources humaines', 'Marketing', 'Technique', 'Sciences de la vie', 'Médical', 'Autre']
        efield = st.sidebar.selectbox('Domaine d\'études', efield_options)
        edu_field = 1 if efield == "Ressources humaines" or efield == "Marketing" or efield == "Technique" else 0
        
        en = st.sidebar.slider('Nombre de personnes dans l\'équipe', 1, 2000, 100)
        employeenumber = 0 if en < 1495 else 1
            
        envsat_options = ['Faible', 'Moyenne', 'Élevée']
        envsat = st.sidebar.selectbox('Satisfaction environnementale', envsat_options)
        env_sat = 1 if envsat == "Faible" else 0
            
        gend_options = ['Homme', 'Femme']
        gend = st.sidebar.selectbox('Genre', gend_options)
        gender = 1 if gend == "Homme" else 0
            
        involve_options = ['Faible', 'Moyenne', 'Élevée', 'Très élevée']
        involve = st.sidebar.selectbox('Implication au travail', involve_options)
        job_inv = 1 if involve == "Faible" else 2 if involve == "Moyenne" else 3 if involve == "Élevée" else 4
        
        role_options = ['Directeur de recherche', 'Manager', 'Représentant en soins de santé', 'Directeur de fabrication', 'Technicien de laboratoire', 'Scientifique de recherche', 'Cadre commercial', 'RH', 'Représentant commercial']
        role = st.sidebar.selectbox('Poste de travail', role_options)
        jobrole = 0 if role == "Directeur de recherche" else 1 if role == "Manager" or role == "Représentant en soins de santé" or role == "Directeur de fabrication" else 3 if role == "Technicien de laboratoire" else 2 if role == "Scientifique de recherche" or role == "Cadre commercial" else 4 if role == "RH" else 5
            
        jobsat_options = ['Faible', 'Moyenne', 'Élevée', 'Très élevée']
        jobsat = st.sidebar.selectbox('Satisfaction au travail', jobsat_options)
        job_sat = 1 if jobsat == "Faible" else 2 if jobsat == "Moyenne" or jobsat == "Élevée" else 3
            
        mar_options = ['Marié', 'Divorcé', 'Célibataire']
        mar = st.sidebar.selectbox('État civil', mar_options)
        mar_stat = 0 if mar == "Marié" or mar == "Divorcé" else 1
            
        income = st.sidebar.slider('Salaire mensuel', 0, 50000, 5000)
        
        num_worked = st.sidebar.number_input('Nombre d\'entreprises travaillées', 0., 10., step=1.)
        num_com = 0 if num_worked <= 4 else 1
            
        otime_options = ['Non', 'Oui']
        otime = st.sidebar.selectbox("L'employé travaille-t-il en heures supplémentaires?", otime_options)
        overtime = 0 if otime == "Non" else 1
            
        sol_options = ['Pas d\'actions', 'Actions modérées', 'Beaucoup d\'actions']
        sol = st.sidebar.selectbox('Actions de l\'employé dans l\'entreprise', sol_options)
        stocks = 0 if sol == "Pas d'actions" else 1 if sol == "Actions modérées" else 2
            
        total_exp = st.sidebar.number_input("Expérience totale de l'employé", 0., 35., step=1.)
        
        training = st.sidebar.number_input("Nombre de formations suivies par l'employé", 0., 7., step=1.)
        
        years_com = st.sidebar.number_input("Nombre d'années passées dans l'entreprise", 0., 30., step=1.)
        
        years_role = st.sidebar.number_input("Nombre d'années dans le rôle actuel", 0., 30., step=1.)
        
        ym = st.sidebar.number_input("Années avec le gestionnaire actuel", 0., 20., step=1.)
        years_man = 0 if ym == 0 else 1 if ym < 12 else 2
            
        com_options = ['Mauvaise', 'Médiocre', 'Bonne', 'Meilleure', 'La meilleure']
        com = st.sidebar.selectbox("Compétences en communication", com_options)
        com_skills = 1 if com == "Mauvaise" else 2 if com == "Médiocre" else 3 if com == "Bonne" else 4 if com == "Meilleure" else 5
            
        inp = [age, dept, distancefromhome, edu_field, employeenumber, env_sat, gender, job_inv, jobrole, job_sat, mar_stat, income, num_com, overtime, stocks, total_exp, training, years_com, years_role, years_man, com_skills]
        
        return inp
    
    df = input_features()
    model = pickle.load(open('model1.pkl', 'rb'))
    proba = model.predict_proba([df])[0][0]
    result = "Le client ne risque pas de partir." if proba < 0.5 else "Le client risque de partir."

    # Ajouter une couleur en fonction du résultat
    result_color = "green" if proba < 0.5 else "red"

    # Encadrer le résultat et donner une couleur
    styled_result = f'<div style="border: 2px solid {result_color}; padding: 10px; border-radius: 10px;"><p style="color: {result_color}; font-size: 18px; font-weight: bold;">{result}</p></div>'

    # Afficher le résultat stylisé
    st.markdown(styled_result, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
