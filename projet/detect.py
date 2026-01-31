import re
import matplotlib.pyplot as plt
from collections import Counter

# Dictionnaires de mots pour chaque émotion (en français, extensible)
emotions_words = {
    'joie': ['heureux', 'joie', 'content', ' ravi', 'excité', 'souriant', 'plaisir', 'bonheur', 'gai', 'enthousiaste'],
    'colère': ['colère', 'furieux', 'énervé', 'rage', 'fâché', 'irrité', 'agressif', 'frustré', 'haine', 'vexé'],
    'tristesse': ['triste', 'tristesse', 'déprimé', 'pleurer', 'malheur', 'souffrance', 'désespoir', 'mélancolie', 'chagrin', 'abattu'],
    'peur': ['peur', 'effrayé', 'anxieux', 'terreur', 'crainte', 'panique', 'inquiétude', 'frayeur', 'trembler', 'angoissé'],
    'neutralité': []  # La neutralité sera calculée si aucun mot émotionnel n'est détecté
}

def clean_text(text):
    # Nettoyer le texte : minuscule, supprimer ponctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Supprimer ponctuation
    words = text.split()
    return words

def detect_emotions(text):
    words = clean_text(text)
    emotion_counts = {emotion: 0 for emotion in emotions_words}
    
    # Compter les occurrences
    word_count = Counter(words)
    for emotion, word_list in emotions_words.items():
        for word in word_list:
            emotion_counts[emotion] += word_count.get(word, 0)
    
    total_emotion_words = sum(emotion_counts.values())
    
    if total_emotion_words == 0:
        # Si aucun mot émotionnel, tout est neutre
        emotion_scores = {emotion: 0.0 for emotion in emotion_counts}
        emotion_scores['neutralité'] = 1.0
    else:
        # Calculer les probabilités (normalisation simple)
        emotion_scores = {emotion: count / total_emotion_words for emotion, count in emotion_counts.items()}
        # Ajouter neutralité comme le reste (mots non émotionnels / total mots)
        neutral_words = len(words) - total_emotion_words
        emotion_scores['neutralité'] = neutral_words / len(words) if len(words) > 0 else 0.0
    
    return emotion_scores

def display_results(emotion_scores):
    print("Émotions détectées avec scores de probabilité :")
    for emotion, score in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{emotion.capitalize()}: {score:.2f}")
    
    # Graphique
    emotions = list(emotion_scores.keys())
    scores = list(emotion_scores.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(emotions, scores, color=['green', 'red', 'blue', 'orange', 'gray'])
    plt.xlabel('Émotions')
    plt.ylabel('Score de probabilité')
    plt.title('Détection des émotions dominantes')
    plt.ylim(0, 1)
    plt.show()

# Entrée utilisateur
text = input("Entrez une phrase ou un paragraphe : ")
emotion_scores = detect_emotions(text)
display_results(emotion_scores)