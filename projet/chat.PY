# Projet simple d'IA : Prédiction de la réussite à un examen
# Ce programme utilise un réseau de neurones pour prédire si un étudiant
# réussira un examen en fonction de ses heures d'étude et de sommeil.

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

# Données d'exemple : [heures d'étude, heures de sommeil, réussite (1=r成功, 0=échec)]
data = np.array([
    [2, 6, 0],
    [4, 7, 1],
    [3, 5, 0],
    [6, 8, 1],
    [1, 4, 0],
    [5, 6, 1],
    [7, 7, 1],
    [3, 6, 0]
])

# Séparer les caractéristiques (X) et les étiquettes (y)
X = data[:, :2]  # Heures d'étude et de sommeil
y = data[:, 2]   # Résultat (réussite ou échec)

# Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Création du modèle de réseau de neurones
model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, random_state=42)

# Entraînement du modèle
model.fit(X_scaled, y)

# Fonction pour prédire la réussite
def predire_reussite(heures_etude, heures_sommeil):
    entree = scaler.transform([[heures_etude, heures_sommeil]])
    prediction = model.predict(entree)
    return "Réussite" if prediction[0] == 1 else "Échec"

# Exemple d'utilisation
etude = int(input("Entrez le nombre d'heures d'étude : "))  
sommeil = int(input("Entrez le nombre d'heures de sommeil : "))
resultat = predire_reussite(etude, sommeil)
print(f"Pour {etude} heures d'étude et {sommeil} heures de sommeil : {resultat}")
