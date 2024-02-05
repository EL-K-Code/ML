from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Charger les modèles entraînés
model1 = joblib.load('model1.pkl')
model2 = joblib.load('model2.pkl')

# Définir une route pour la page d'accueil
@app.route('/')
def index():
    return 'Hello, World!'

# Définir une route pour effectuer la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données saisies par l'utilisateur depuis la requête POST
        user_inputs = request.json

        # Créer un dataframe avec les valeurs saisies par l'utilisateur
        user_input_df = pd.DataFrame([user_inputs])

        # Vérifier si EnergyStarScore est renseigné
        if 'ENERGYSTARScore' in user_inputs and user_inputs['ENERGYSTARScore']==0 :
            prediction = model1.predict(user_input_df)
        else:
            prediction = model2.predict(user_input_df)

        # Retourner la prédiction
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

