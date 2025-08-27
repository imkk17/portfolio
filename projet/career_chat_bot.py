import json
import customtkinter as ctk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Téléchargez les ressources NLTK si nécessaire
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Base de connaissances avec spécialités recommandées
KNOWLEDGE_BASE = {
    "questions": [
        {
            "text": "Aimez-vous résoudre des problèmes techniques ou travailler avec des ordinateurs ?",
            "keywords": ["oui", "ordinateurs", "technique", "programmation", "résoudre"],
            "sectors": ["Informatique", "Intelligence Artificielle"]
        },
        {
            "text": "Êtes-vous intéressé par la biologie, la santé ou aider les gens ?",
            "keywords": ["oui", "biologie", "santé", "aider", "svt", "sciences vie terre"],
            "sectors": ["Médecine"]
        },
        {
            "text": "Aimez-vous concevoir, construire ou travailler sur des projets techniques ?",
            "keywords": ["oui", "concevoir", "construire", "technique", "projets"],
            "sectors": ["Ingénierie"]
        },
        {
            "text": "Êtes-vous attiré par les chiffres, l'analyse financière ou la gestion ?",
            "keywords": ["oui", "chiffres", "finance", "gestion", "analyse"],
            "sectors": ["Finance"]
        },
        {
            "text": "Aimez-vous enseigner, partager des connaissances ou travailler avec des jeunes ?",
            "keywords": ["oui", "enseigner", "connaissances", "jeunes", "éducation"],
            "sectors": ["Éducation"]
        },
        {
            "text": "Êtes-vous passionné par la créativité, l'art ou le design ?",
            "keywords": ["oui", "créativité", "art", "design", "graphisme"],
            "sectors": ["Arts et Design"]
        }
    ],
    "sectors": {
        "Informatique": {
            "description": "Le secteur de l'informatique inclut le développement de logiciels, la cybersécurité et la gestion de réseaux. Idéal pour coder ou résoudre des problèmes techniques.",
            "specialties": ["Mathématiques", "Numérique et Sciences Informatiques (NSI)", "Physique-Chimie"],
            "score": 0
        },
        "Intelligence Artificielle": {
            "description": "L'IA concerne la création de systèmes intelligents, comme les chatbots ou les modèles prédictifs. Parfait pour les passionnés de données et d'innovation.",
            "specialties": ["Mathématiques", "Numérique et Sciences Informatiques (NSI)", "Physique-Chimie"],
            "score": 0
        },
        "Médecine": {
            "description": "Le secteur médical est axé sur les soins, la recherche en santé et la biologie. Convient si vous aimez aider les gens ou êtes intéressé par la SVT.",
            "specialties": ["Sciences de la Vie et de la Terre (SVT)", "Physique-Chimie", "Mathématiques"],
            "score": 0
        },
        "Ingénierie": {
            "description": "L'ingénierie couvre la conception et la construction, de ponts aux systèmes électroniques. Idéal pour les esprits analytiques et créatifs.",
            "specialties": ["Mathématiques", "Physique-Chimie", "Sciences de l'Ingénieur"],
            "score": 0
        },
        "Finance": {
            "description": "Le secteur financier inclut la gestion d'actifs, la banque et l'analyse économique. Parfait si vous aimez les chiffres et la stratégie.",
            "specialties": ["Mathématiques", "Sciences Économiques et Sociales (SES)", "Histoire-Géographie, Géopolitique et Sciences Politiques (HGGSP)"],
            "score": 0
        },
        "Éducation": {
            "description": "Le secteur de l'éducation implique l'enseignement et la formation. Idéal si vous aimez transmettre des connaissances.",
            "specialties": ["Sciences Économiques et Sociales (SES)", "Histoire-Géographie, Géopolitique et Sciences Politiques (HGGSP)", "Littérature, Langues et Cultures de l'Antiquité (LLCA)"],
            "score": 0
        },
        "Arts et Design": {
            "description": "Les arts et le design concernent la création visuelle ou artistique. Parfait pour les personnes créatives.",
            "specialties": ["Arts", "Littérature, Langues et Cultures de l'Antiquité (LLCA)", "Histoire-Géographie, Géopolitique et Sciences Politiques (HGGSP)"],
            "score": 0
        }
    }
}

# Fonction pour prétraiter le texte
def preprocess_text(text):
    tokens = word_tokenize(text.lower(), language='french')
    stop_words = set(stopwords.words('french'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return filtered_tokens

# Classe pour l'interface graphique avec CustomTkinter
class CareerQuizChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quiz d'Orientation Professionnelle")
        ctk.set_appearance_mode("dark")  # Thème sombre
        ctk.set_default_color_theme("blue")  # Thème bleu

        self.history = []  # Historique des échanges
        self.current_question_index = 0  # Suivi de la question
        self.scores = {sector: 0 for sector in KNOWLEDGE_BASE["sectors"]}  # Scores des secteurs

        # Zone de chat
        self.chat_area = ctk.CTkTextbox(master, wrap="word", width=600, height=400, font=("Helvetica", 14))
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.chat_area.configure(state="disabled")

        # Champ de saisie
        self.entry = ctk.CTkEntry(master, width=500, placeholder_text="Tapez votre réponse ici...", font=("Helvetica", 14))
        self.entry.grid(row=1, column=0, padx=(20, 5), pady=10, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        # Bouton d'envoi
        self.send_button = ctk.CTkButton(master, text="Envoyer", command=self.send_message, font=("Helvetica", 14))
        self.send_button.grid(row=1, column=1, padx=(5, 20), pady=10, sticky="w")

        # Configurer la grille
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Message d'accueil
        self.display_message("Chatbot: Bienvenue dans le quiz d'orientation professionnelle ! Je vais vous poser quelques questions pour découvrir vos intérêts. Répondez par 'Oui', 'Non', ou décrivez vos intérêts (ex. : 'J'aime SVT'). À la fin, je vous suggérerai des spécialités du bac. Prêt ?")
        self.ask_next_question()

    def display_message(self, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", message + "\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def ask_next_question(self):
        if self.current_question_index < len(KNOWLEDGE_BASE["questions"]):
            question = KNOWLEDGE_BASE["questions"][self.current_question_index]["text"]
            self.display_message(f"Chatbot: {question}")
        else:
            self.show_results()

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return

        self.display_message(f"Vous: {user_message}")
        self.entry.delete(0, "end")

        if self.current_question_index < len(KNOWLEDGE_BASE["questions"]):
            self.process_answer(user_message)
            self.current_question_index += 1
            self.ask_next_question()

        # Ajouter à l'historique (10 derniers échanges)
        self.history.append({"user": user_message, "bot": "Réponse enregistrée"})
        if len(self.history) > 10:
            self.history.pop(0)

    def process_answer(self, user_answer):
        user_tokens = preprocess_text(user_answer)
        current_question = KNOWLEDGE_BASE["questions"][self.current_question_index]

        # Vérifier si la réponse est positive
        positive_indicators = ["oui", "yes", "bien sûr", "évidement", "j'aime", "intéresse", "passionné"]
        if any(token in positive_indicators or token in current_question["keywords"] for token in user_tokens):
            for sector in current_question["sectors"]:
                self.scores[sector] += 1

    def show_results(self):
        max_score = max(self.scores.values()) if self.scores else 0
        if max_score == 0:
            self.display_message("Chatbot: Hmm, aucune préférence claire détectée. Essayez de répondre avec plus de détails ou recommencez le quiz !")
            return

        suggested_sectors = [sector for sector, score in self.scores.items() if score == max_score]
        suggestions = ""
        for sector in suggested_sectors:
            specialties = ", ".join(KNOWLEDGE_BASE["sectors"][sector]["specialties"])
            suggestions += f"- {sector}: {KNOWLEDGE_BASE['sectors'][sector]['description']}\n  Spécialités recommandées : {specialties}\n"

        self.display_message(f"Chatbot: D'après vos réponses, voici les secteurs qui vous correspondent le mieux :\n{suggestions}")
        self.display_message("Chatbot: Voulez-vous recommencer le quiz ? Répondez 'Oui' pour relancer ou fermez la fenêtre.")

        # Réinitialiser pour permettre un nouveau quiz
        self.entry.bind("<Return>", self.check_restart)

    def check_restart(self, event=None):
        user_message = self.entry.get().strip().lower()
        if user_message in ["oui", "yes"]:
            self.current_question_index = 0
            self.scores = {sector: 0 for sector in KNOWLEDGE_BASE["sectors"]}
            self.display_message("Chatbot: Super, on recommence !")
            self.ask_next_question()
        self.entry.delete(0, "end")
        self.entry.bind("<Return>", self.send_message)

# Fonction principale
if __name__ == "__main__":
    root = ctk.CTk()
    app = CareerQuizChatbotGUI(root)
    root.mainloop()