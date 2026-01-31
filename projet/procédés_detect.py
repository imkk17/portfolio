import re
import matplotlib.pyplot as plt
from collections import Counter

# Dictionnaire des procédés littéraires avec motifs et explications
literary_devices = {
    'métaphore': {
        'keywords': [r'\b(comme|tel|telle)\b.*\b(est|sont)\b', r'\b(semble|semblent)\b.*\b(comme|tel|telle)\b'],
        'explanation': 'Compare deux éléments sans mot de comparaison explicite, crée une image poétique.'
    },
    'anaphore': {
        'keywords': [r'^\b(\w+)\b.*\n\s*\1\b'],
        'explanation': 'Répétition d’un mot ou groupe de mots en début de phrase, insiste sur une idée.'
    },
    'hyperbole': {
        'keywords': [r'\b(toujours|jamais|énorme|immense|terrible|infini)\b'],
        'explanation': 'Exagération pour amplifier l’effet ou l’émotion.'
    },
    'personnification': {
        'keywords': [r'\b(nature|vent|soleil|lune|mer|ciel)\b.*\b(parle|chante|danse|pleure|rit)\b'],
        'explanation': 'Donne des caractéristiques humaines à des objets ou éléments naturels.'
    },
    'antithèse': {
        'keywords': [r'\b(mais|cependant|pourtant)\b.*\b(opposé|contraire|différent)\b'],
        'explanation': 'Met en opposition deux idées pour créer un contraste.'
    },
    'allitération': {
        'keywords': [r'\b(\w)\w*\s+\1\w*'],
        'explanation': 'Répétition d’un son consonantique pour renforcer le rythme.'
    }
}

# Fonction pour nettoyer le texte
def clean_text(text):
    text = re.sub(r'[^\w\s.,\n]', '', text)  # Conserver espaces, ponctuation de base et retours à la ligne
    return text

# Fonction pour détecter les procédés littéraires et identifier les lignes/mots
def detect_literary_devices(text):
    text = clean_text(text)
    lines = text.split('\n')
    device_counts = {key: 0 for key in literary_devices}
    device_details = {key: [] for key in literary_devices}
    
    # Analyser chaque ligne
    for line_num, line in enumerate(lines, 1):
        line_clean = line.lower().strip()
        if not line_clean:
            continue
        for device, info in literary_devices.items():
            for pattern in info['keywords']:
                matches = re.finditer(pattern, line_clean, re.IGNORECASE)
                for match in matches:
                    device_counts[device] += 1
                    # Identifier le mot ou la phrase correspondant au procédé
                    matched_text = match.group(0)
                    device_details[device].append({
                        'line': line_num,
                        'text': matched_text,
                        'full_line': line.strip()
                    })
    
    return device_counts, device_details

# Fonction pour afficher les résultats et le graphique
def display_results(device_counts, device_details):
    total_devices = sum(device_counts.values())
    
    print("\nProcédés littéraires détectés :")
    if total_devices == 0:
        print("Aucun procédé littéraire détecté.")
    else:
        for device, count in device_counts.items():
            if count > 0:
                print(f"\n- {device.capitalize()} ({count} fois) : {literary_devices[device]['explanation']}")
                print("  Exemples trouvés :")
                for detail in device_details[device]:
                    print(f"    Ligne {detail['line']} : « {detail['full_line']} »")
                    print(f"    Mot ou expression : « {detail['text']} »")
    
    # Graphique
    devices = list(device_counts.keys())
    counts = list(device_counts.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(devices, counts, color=['blue', 'green', 'red', 'purple', 'orange', 'cyan'])
    plt.xlabel('Procédés littéraires')
    plt.ylabel('Nombre d’occurrences')
    plt.title('Procédés littéraires dans le texte')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Exemple de texte à tester (inspiré d’un style littéraire)
default_text = """Le soleil chante comme un poète libre,
Mon cœur pleure, toujours pleure, de tristesse infinie.
La mer danse et le vent murmure des secrets.
Mais l’espoir brille, pourtant tout semble perdu."""
print("Texte testé :\n", default_text)
device_counts, device_details = detect_literary_devices(default_text)
display_results(device_counts, device_details)

# Demander un autre texte à l'utilisateur
text = input("\nEntrez votre propre texte : ")
if text.strip():
    device_counts, device_details = detect_literary_devices(text)
    display_results(device_counts, device_details)