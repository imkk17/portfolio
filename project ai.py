from flask import Flask, render_template, request
from transformers import pipeline

# Créer une instance de Flask
app = Flask(__name__)

# Charger le modèle GPT-2 pour la génération de texte
chatbot = pipeline('text-generation', model='gpt2')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    # Récupérer la question de l'utilisateur depuis le formulaire
    user_input = request.form["user_input"]
    
    # Utiliser GPT-2 pour générer une réponse
    response = chatbot(user_input, max_length=50, num_return_sequences=1)
    
    # Renvoyer la réponse au frontend (index.html)
    return render_template("index.html", user_input=user_input, response=response[0]['generated_text'])

if __name__ == "__main__":
    app.run(debug=True)
