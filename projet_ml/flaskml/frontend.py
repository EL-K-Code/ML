import streamlit as st
import pandas as pd
import requests

# URL de l'API Flask
API_URL = "http://127.0.0.1:8080/predict"

# Interface utilisateur Streamlit
st.title("Application de Prédiction de la consommation d'énergie des bâtiments non résidentiels")


user_inputs = {}

# Charger la base de données depuis le fichier CSV
data = pd.read_csv("C:/Users/DELL/Desktop/ISE2/Semestre1/Machine_learning1/Projet_ML/Data1/2016_Building_Energy_final.csv", sep=",")

# Récupérer la liste des noms de colonnes (variables)
variable_names = data.columns.tolist()
variable_names.remove('SiteEnergyUse(kBtu)')

YearBuilt = None

# Générer automatiquement les champs de saisie
for variable_name in variable_names:
    # Si la variable est 'SiteEnergyUse', utiliser un selectbox
    if len(data[variable_name].unique()) <= 13 and variable_name != 'NumberOfPropertyUseTypes' and variable_name != 'YearBuilt' and variable_name != 'NombreAnnees' and variable_name != 'NumberofBuildings':
        selected_value = st.selectbox(variable_name, data[variable_name].unique())
    # Si la variable a plus de 12 valeurs uniques et n'est pas 'SiteEnergyUse(kBtu)', et est numérique
    elif len(data[variable_name].unique()) > 13 and variable_name != 'NumberOfPropertyUseTypes' and variable_name != 'YearBuilt' and variable_name != 'NombreAnnees' and variable_name != 'NumberofBuildings' and pd.api.types.is_numeric_dtype(data[variable_name]):
        selected_value = st.number_input(variable_name, min_value=0)
    elif variable_name == 'NumberOfPropertyUseTypes':
        selected_value = st.number_input(variable_name, min_value=1, max_value=10)
    elif variable_name == 'NumberofBuildings':
        selected_value = st.number_input(variable_name, min_value=1, max_value=50)
    # Si la variable est 'YearBuilt', utiliser un champ de saisie numérique avec des valeurs limites
    elif variable_name == 'YearBuilt':
        selected_value = st.number_input(variable_name, min_value=1800, max_value=2016)
        YearBuilt = selected_value
    # Si la variable est 'NombreAnnees', calculer automatiquement en fonction de 'YearBuilt'
    elif variable_name == 'NombreAnnees':
        selected_value = 2016 - YearBuilt if YearBuilt else None
    # Sinon, utiliser un champ de texte pour les autres variables
    else:
        selected_value = st.text_input(variable_name)

    
    # Stocker la valeur sélectionnée dans le dictionnaire
    user_inputs[variable_name] = selected_value

if st.button("Effectuer la prédiction"):
    try:
        # Collecter les valeurs saisies par l'utilisateur à partir du dictionnaire
        inputs = {
        "BuildingType" : str(user_inputs["BuildingType"]),
        "CouncilDistrictCode" : int(user_inputs["CouncilDistrictCode"]),
        "Neighborhood" : str(user_inputs["Neighborhood"]),
        "YearBuilt" : int(user_inputs["YearBuilt"]),
        "NumberofBuildings" : int(user_inputs["NumberofBuildings"]),
        "NumberofFloors" : int(user_inputs["NumberofFloors"]),
        "PropertyGFAParking" : int(user_inputs["PropertyGFAParking"]),
        "PropertyGFABuilding(s)" : int(user_inputs["PropertyGFABuilding(s)"]),
        "LargestPropertyUseTypeGFA" : int(user_inputs["LargestPropertyUseTypeGFA"]),
        "SecondLargestPropertyUseTypeGFA" : int(user_inputs["SecondLargestPropertyUseTypeGFA"]),
        "ThirdLargestPropertyUseTypeGFA" : int(user_inputs["ThirdLargestPropertyUseTypeGFA"]),
        "ENERGYSTARScore" : int(user_inputs["ENERGYSTARScore"]),
        "TotalGHGEmissions" : int(user_inputs["TotalGHGEmissions"]),
        "PrimaryProperty" : str(user_inputs["PrimaryProperty"]),
        "SecondLargest" : str(user_inputs["SecondLargest"]),
        "ThirdLargest" : str(user_inputs["ThirdLargest"]),
        "NumberOfPropertyUseTypes" : int(user_inputs["NumberOfPropertyUseTypes"]),
        "NombreAnnees" : int(user_inputs["NombreAnnees"])
    }

        # Faire une requête à l'API Flask pour obtenir la prédiction
        response = requests.post(API_URL, json=inputs)

        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.success(f"La prédiction de la consommation d'énergie sur site en kBtu pour ce batiment est : {prediction}")
        else:
            st.error("Erreur lors de la prédiction.")

    except Exception as e:
        st.error(f"Erreur: {e}")
