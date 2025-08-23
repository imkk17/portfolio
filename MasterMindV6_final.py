# librairie
# Importation de la librairie customtkinter pour la création de l'interface graphique
import  customtkinter  as ctk

# Importation de la librairie tkinter pour la création de l'interface de base
import tkinter as tk

# Importation du module messagebox de tkinter pour afficher des boîtes de dialogue
from tkinter import messagebox

# Importation de diverses librairies nécessaires pour la logique du jeu
import random  # Pour générer des nombres aléatoires
import locale  # Pour gérer la localisation (langue et format)
import winsound  # Pour jouer des sons sous Windows
import platform  # Pour détecter le système d'exploitation
from datetime import datetime  # Pour manipuler les dates et heures
import requests  # Pour envoyer des requêtes HTTP (utilisé pour accéder aux API)
import warnings  # Pour gérer les avertissements
from urllib3.exceptions import InsecureRequestWarning  # Pour ignorer certains avertissements de sécurité SSL

# Importation de la classe font de tkinter pour définir des polices personnalisées
from tkinter import font

# Ignorer les avertissements liés aux certificats SSL pour les requêtes HTTP
warnings.simplefilter('ignore', InsecureRequestWarning)
# Configuration de base pour le thème et l'apparence
ctk.deactivate_automatic_dpi_awareness()# Désactive le DPI automatique pour une apparence cohérente
ctk.set_appearance_mode("dark") # Mode sombre activé
ctk.set_default_color_theme("blue") # Thème bleu par défaut
# Thème de couleurs pour l'interface
COLORS = {
    'bg': '#1a1a1a',# Couleur de fond principale
    'text': '#ffffff', # Couleur du texte
    'button': '#4169E1', # Couleur des boutons
    'frame': '#1a1a1a'# Couleur des cadres
}
# Définition des couleurs pour le jeu en fonction de la langue
colors = {
    "en": ["Black", "Red", "Green", "White", "Blue"],# en anglais
    "fr": ["Noir", "Rouge", "Vert", "Blanc", "Bleu"]# en francais
}
# URL pour stocker et récupérer les scores via une base de données Firebase fait par mathias
SCORES_API_URL = "https://mastermind-df170-default-rtdb.europe-west1.firebasedatabase.app/scores.json"
# MasterMindV6_final.py

import random

def generate_secret_combination():
    colors = ["Black", "Red", "Green", "White", "Blue"]
    return [random.choice(colors) for _ in range(4)]

def check_guess(secret_combination, user_guess):
    correct_positions = sum(1 for i in range(4) if user_guess[i] == secret_combination[i])
    misplaced_positions = sum(min(secret_combination.count(c), user_guess.count(c)) for c in set(user_guess)) - correct_positions
    return {"correct": correct_positions, "misplaced": misplaced_positions}

def load_scores():
    """
    Charge les scores enregistrés depuis la base de données distante.
    Retourne un dictionnaire contenant les scores pour chaque niveau de difficulté.
    """
    try:
        response = requests.get(SCORES_API_URL, verify=False)
        if response.status_code == 200:
            scores = response.json()
            if scores is None:
                scores = {"Easy": [], "Medium": [], "Hard": []}
            return scores
        else:
            return {"Easy": [], "Medium": [], "Hard": []}
    except Exception as e:
        print(f"Erreur lors du chargement des scores: {e}")
        return {"Easy": [], "Medium": [], "Hard": []}
#Calcule le score du joueur en fonction de la difficulté, du temps écoulé, et des tentatives restantes.
def calculate_score(difficulty, time_taken, attempts_used, max_attempts, time_limit):
    difficulty_multiplier = {
        "Easy": 1, # multiplicateur de la difficulté facile
        "Medium": 2,# multiplicateur de la difficulté intermédiare 
        "Hard": 3# multiplicateur de la difficulté compliqué
    }
    # Points de base selon la difficulté
    base_points = 1000 * difficulty_multiplier[difficulty]
     # Calcul des points pour le temps restant
    time_points = 0
    if time_limit:# Vérifie s'il y a une limite de temps
        time_remaining = time_limit - time_taken
        time_points = (time_remaining / time_limit) * 500 * difficulty_multiplier[difficulty]
     # Calcul des points pour les tentatives restantes
    attempt_points = 0
    if max_attempts:# Vérifie s'il y a un nombre maximum de tentatives
        attempts_remaining = max_attempts - attempts_used
        attempt_points = (attempts_remaining / max_attempts) * 500 * difficulty_multiplier[difficulty]

    total_score = int(base_points + time_points + attempt_points)
    # Retourne le score total
    return total_score
#Sauvegarde le score du joueur dans la base de données distante.
def save_score(difficulty, time_taken, attempts_used, player_name):
    try:
        scores = load_scores() # Récupération des scores existants
        if scores is None:# Initialise les scores si vide
            scores = {"Easy": [], "Medium": [], "Hard": []}

        # Détermine les paramètres de la difficulté
        max_attempts = difficulty_levels[difficulty]
        time_limit = time_limits[difficulty]
        score_points = calculate_score(difficulty, time_taken, attempts_used, max_attempts, time_limit)
        
        if difficulty not in scores:# Initialise la catégorie si nécessaire
            scores[difficulty] = []
        
        new_score = {  # Crée une nouvelle entrée de score
            "name": player_name,
            "time": time_taken,
            "attempts": attempts_used,
            "score": score_points,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        scores[difficulty].append(new_score)# Ajoute le score à la liste
        
        scores[difficulty].sort(key=lambda x: (-x["score"], x["time"]))# Trie par score décroissant
        scores[difficulty] = scores[difficulty][:5]# Conserve uniquement les 5 meilleurs scores
        

        response = requests.put(SCORES_API_URL, json=scores, verify=False)# Envoie des scores mis à jour
        
        if response.status_code == 200: # Si la requête réussit
            print("Score sauvegardé avec succès!")
            print(f"Nouveau score: {new_score}")
            return True
        else: 
            print(f"Erreur lors de la sauvegarde du score: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False 
            
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du score: {e}")
        return False

def get_system_language():
    try:
        locale.setlocale(locale.LC_ALL, '')
        system_lang = locale.getlocale()[0]
        return 'fr' if system_lang and system_lang.startswith('fr') else 'en'
    except:
        return 'en'

texts = {
    "en": {
        "welcome": "Welcome to Mastermind!",
        "instructions": "Try to guess the secret color combination!\nSelect a difficulty level and press 'Play'.",
        "play_button": "Play",
        "change_language_button": "Change Language",
        "creator_label": "Created by Spice Thrower and The Redhead",
        "difficulty_label": "Select Difficulty:",
        "choose": "Choose",
        "attempts_left": "Attempts Left: ",
        "time_left": "Time Left: ",
        "infinity": "∞",
        "validate": "Validate",
        "restart": "Restart Game",
        "return": "Return to Menu",
        "attempt_result": "Attempt: ",
        "correct_result": "Correct: ",
        "misplaced_result": "Misplaced: ",
        "warning": "Warning",
        "select_colors": "Select a color for each position.",
        "victory": "Victory!",
        "congrats": "Congratulations! You've guessed the combination!",
        "game_over": "Game Over",
        "out_of_attempts": "Out of attempts! The combination was:",
        "time_up": "Time's Up!",
        "time_up_message": "Time is up! You have run out of time!",
        "instructions_game": "Select a color for each position and click Validate to submit.\nTry to guess the secret combination in limited attempts!",
        "confirm_restart": "Do you want to restart the game?",
        "confirm_return": "Do you want to return to the main menu?",
        "scoreboard": "High Scores",
        "no_scores": "No scores yet!",
        "score_entry": "Attempts: {}, Time: {}s",
        "show_scores": "Show Scores",
        "save_score_title": "Save Score",
        "save_score_message": "Would you like to save your score?",
        "enter_name": "Enter your name:",
        "default_name": "Anonymous",
        "position_1": "1st",
        "position_2": "2nd",
        "position_3": "3rd",
        "score": "Score: "
    },
    "fr": {
        "welcome": "Bienvenue dans Mastermind!",
        "instructions": "Essayez de deviner la combinaison secrète de couleurs !\nSélectionnez un niveau de difficulté et appuyez sur 'Jouer'.",
        "play_button": "Jouer",
        "change_language_button": "Changer la langue",
        "creator_label": "Créé par Spice Thrower et The Redhead",
        "difficulty_label": "Sélectionnez la difficulté :",
        "choose": "Choisir",
        "attempts_left": "Tentatives restantes : ",
        "time_left": "Temps restant : ",
        "infinity": "∞",
        "validate": "Valider",
        "restart": "Recommencer",
        "return": "Retour au Menu",
        "attempt_result": "Tentative : ",
        "correct_result": "Correct : ",
        "misplaced_result": "Mal placé : ",
        "warning": "Attention",
        "select_colors": "Sélectionnez une couleur pour chaque position.",
        "victory": "Victoire !",
        "congrats": "Félicitations ! Vous avez trouvé la combinaison !",
        "game_over": "Partie Terminée",
        "out_of_attempts": "Plus de tentatives ! La combinaison était :",
        "time_up": "Temps Écoulé !",
        "time_up_message": "Le temps est écoulé ! Vous n'avez plus de temps !",
        "instructions_game": "Sélectionnez une couleur pour chaque position et cliquez sur Valider pour soumettre.\nEssayez de deviner la combinaison secrète en un nombre limité de tentatives !",
        "confirm_restart": "Voulez-vous recommencer la partie ?",
        "confirm_return": "Voulez-vous retourner au menu principal ?",
        "scoreboard": "Meilleurs Scores",
        "no_scores": "Pas encore de scores !",
        "score_entry": "Tentatives : {}, Temps : {}s",
        "show_scores": "Voir les Scores",
        "save_score_title": "Sauvegarder le Score",
        "save_score_message": "Voulez-vous sauvegarder votre score ?",
        "enter_name": "Entrez votre nom :",
        "default_name": "Anonyme",
        "position_1": "1er",
        "position_2": "2ème",
        "position_3": "3ème",
        "score": "Score : "
    }
}

secret_combination = []
attempts_left = 10
current_proposition = ["", "", "", ""]
difficulty_levels = {"Easy": None, "Medium": 10, "Hard": 5}
time_limits = {"Easy": 300, "Medium": 180, "Hard": 120}
time_left = 0
timer_running = False
timer_id = None

current_language = get_system_language()

window = ctk.CTk()
window.title("Mastermind")
window.geometry("600x750")

ctk.set_default_color_theme("blue")

difficulty_var = ctk.StringVar(value="Medium")

def play_alert_sound(type="info"):
    if platform.system() == "Windows":
        if type == "info":
            winsound.MessageBeep(-1)
        elif type == "warning":
            winsound.MessageBeep(48)
        elif type == "error":
            winsound.MessageBeep(16)
        else:
            winsound.MessageBeep(0)
    else:
        import os
        os.system('bell')

class CustomMessageBox(tk.Toplevel):
    def __init__(self, title, message, type="info"):
        super().__init__()
        
        play_alert_sound(type)
        
        self.title(title)
        self.geometry("300x100")
        self.configure(bg=COLORS['bg'])

        self.response = None

        self.message_label = ctk.CTkLabel(self, text=message, fg_color=COLORS['bg'], justify="center")
        self.message_label.pack(pady=10)

        if type == "info":
            self.ok_button = ctk.CTkButton(self, text="OK", command=self.on_ok)
            self.ok_button.pack(pady=10)
        elif type == "yesno":
            self.yes_button = ctk.CTkButton(self, text="Yes", command=self.on_yes)
            self.yes_button.pack(side="left", padx=5)
            self.no_button = ctk.CTkButton(self, text="No", command=self.on_no)
            self.no_button.pack(side="right", padx=5)

    def on_ok(self):
        self.response = "ok"
        self.destroy()

    def on_yes(self):
        self.response = "yes"
        self.destroy()

    def on_no(self):
        self.response = "no"
        self.destroy()

def show_message(title, message, type="info"):
    dialog = CustomMessageBox(title, message, type)
    dialog.wait_window()
    return dialog.response

def show_confirm(title, message):
    return show_message(title, message, "yesno")

current_score = 0
score_label = None

def initialize_game(difficulty="Medium"):
    global attempts_left, current_proposition, time_left, timer_running, timer_id, current_score, score_label
    if timer_id:
        window.after_cancel(timer_id)
    attempts_left = difficulty_levels[difficulty]
    time_left = time_limits[difficulty]
    timer_running = True
    current_score = 0
    current_proposition = ["", "", "", ""]
    for combo in color_boxes:
        combo.set(texts[current_language]["choose"])
        combo.configure(values=colors[current_language])
    attempts_label.configure(text=f"{texts[current_language]['attempts_left']} {texts[current_language]['infinity'] if attempts_left is None else attempts_left}")
    score_label.configure(text=f"Score: {current_score}")
    result_text.delete("1.0", ctk.END)
    update_timer()

def update_timer():
    global time_left, timer_running, timer_id
    if timer_running:
        minutes, seconds = divmod(time_left, 60)
        timer_label.configure(text=f"{texts[current_language]['time_left']}{minutes:02}:{seconds:02}")
        if time_left > 0:
            time_left -= 1
            timer_id = window.after(1000, update_timer)
        else:
            timer_running = False
            messagebox.showinfo(texts[current_language]["time_up"], 
                              texts[current_language]["time_up_message"])
            game_screen.pack_forget()
            welcome_screen.pack(fill="both", expand=True)

def on_color_selected(selected_color, position):
    current_proposition[position] = selected_color

def verify_proposition():
    global attempts_left, current_score
    current_proposition = []
    for box in color_boxes:
        color = box.get()
        if color in colors["fr"]:
            index = colors["fr"].index(color)
            color = colors["en"][index]
        current_proposition.append(color)

    if texts[current_language]["choose"] in current_proposition:
        show_message(texts[current_language]["warning"], 
                    texts[current_language]["select_colors"])
        return

    correct_positions = sum(1 for i in range(4) if current_proposition[i] == secret_combination[i])
    misplaced_positions = sum(min(secret_combination.count(c), current_proposition.count(c)) for c in
                              set(current_proposition)) - correct_positions

    display_colors = []
    for color in current_proposition:
        if current_language == "fr":
            index = colors["en"].index(color)
            display_colors.append(colors["fr"][index])
        else:
            display_colors.append(color)

    formatted_colors = ", ".join(display_colors)

    result_text._textbox.insert(ctk.END, f"{texts[current_language]['attempt_result']}{formatted_colors}\n", "center")
    result_text._textbox.insert(ctk.END, f"{texts[current_language]['correct_result']}{correct_positions}, "
                             f"{texts[current_language]['misplaced_result']}{misplaced_positions}\n\n", "center")

    if correct_positions == 4:
        global timer_running
        timer_running = False  # Arrêter le timer

        time_taken = time_limits[difficulty_var.get()] - time_left
        initial_attempts = difficulty_levels[difficulty_var.get()]
        attempts_used = initial_attempts - attempts_left if initial_attempts else 1
        
        final_score = calculate_score(
            difficulty_var.get(),
            time_taken,
            attempts_used,
            initial_attempts,
            time_limits[difficulty_var.get()]
        )
        current_score = final_score
        score_label.configure(text=f"Score: {current_score}")
        
        show_message(texts[current_language]["victory"], 
                    texts[current_language]["congrats"])
        
        response = show_confirm(
            texts[current_language]["save_score_title"],
            texts[current_language]["save_score_message"]
        )
        
        if response == "yes":
            name_dialog = NameInputDialog(window)
            window.wait_window(name_dialog)
            player_name = name_dialog.name
            
            if player_name:
                print(f"Sauvegarde du score pour {player_name}")
                print(f"Difficulté: {difficulty_var.get()}")
                print(f"Temps: {time_taken}")
                print(f"Tentatives: {attempts_used}")
                
                save_score(
                    difficulty_var.get(),
                    time_taken,
                    attempts_used,
                    player_name
                )
                update_scoreboard()
        
        game_screen.pack_forget()
        welcome_screen.pack(fill="both", expand=True)
    else:
        if attempts_left is not None:
            attempts_left -= 1
            attempts_label.configure(text=f"{texts[current_language]['attempts_left']} {attempts_left}")
            if attempts_left == 0:
                display_secret = []
                for color in secret_combination:
                    if current_language == "fr":
                        index = colors["en"].index(color)
                        display_secret.append(colors["fr"][index])
                    else:
                        display_secret.append(color)
                
                formatted_secret = ", ".join(display_secret)
                        
                messagebox.showinfo(texts[current_language]["game_over"], 
                                  f"{texts[current_language]['out_of_attempts']} {formatted_secret}")
                game_screen.pack_forget()
                welcome_screen.pack(fill="both", expand=True)

def confirm_restart():
    if show_confirm(
        texts[current_language].get("warning", "Warning"),
        texts[current_language].get("confirm_restart", "Do you want to restart the game?")
    ):
        reset_game()

def confirm_return():
    if show_confirm(
        texts[current_language].get("warning", "Warning"),
        texts[current_language].get("confirm_return", "Do you want to return to the main menu?")
    ):
        game_screen.pack_forget()
        welcome_screen.pack(fill="both", expand=True)

def reset_game():
    global secret_combination
    selected_difficulty = difficulty_var.get()
    secret_combination = [random.choice(colors["en"]) for _ in range(4)]
    print(secret_combination)
    initialize_game(selected_difficulty)

def start_game():
    global secret_combination
    welcome_screen.pack_forget()
    game_screen.pack(fill="both", expand=True)
    secret_combination = [random.choice(colors["en"]) for _ in range(4)]
    print(secret_combination)
    reset_game()

def change_language(difficulty_label):
    global current_language
    current_language = "fr" if current_language == "en" else "en"

    welcome_label.configure(text=texts[current_language]["welcome"])
    instructions_label.configure(text=texts[current_language]["instructions"])
    play_button.configure(text=texts[current_language]["play_button"])
    language_button.configure(text=texts[current_language]["change_language_button"])
    creator_label.configure(text=texts[current_language]["creator_label"])
    difficulty_label.configure(text=texts[current_language]["difficulty_label"])

    for widget in difficulty_frame.winfo_children()[1:]:
        if isinstance(widget, ctk.CTkRadioButton):
            widget.configure(text=widget.fr_level if current_language == "fr" else widget.level)

    instructions.configure(text=texts[current_language]["instructions_game"])
    attempts_label.configure(
        text=f"{texts[current_language]['attempts_left']} {texts[current_language]['infinity'] if attempts_left is None else attempts_left}")
    timer_label.configure(text=f"{texts[current_language]['time_left']} --:--")
    
    validate_button.configure(text=texts[current_language]["validate"])
    restart_button.configure(text=texts[current_language]["restart"])
    return_button.configure(text=texts[current_language]["return"])
    
    for combo in color_boxes:
        current_value = combo.get()
        old_lang = "en" if current_language == "fr" else "fr"
        if current_value in colors[old_lang]:
            index = colors[old_lang].index(current_value)
            combo.set(colors[current_language][index])
        else:
            combo.set(texts[current_language]["choose"])
        combo.configure(values=colors[current_language])

    scoreboard_title.configure(text=texts[current_language]["scoreboard"])
    update_scoreboard()

def update_scoreboard():
    for widget in scoreboard_frame.winfo_children()[1:]:
        widget.destroy()
    
    scores = load_scores()
    
    diff_name = difficulty_var.get()
    if current_language == "fr":
        diff_map = {"Easy": "Facile", "Medium": "Moyen", "Hard": "Difficile"}
        diff_name = diff_map[diff_name]
    
    ctk.CTkLabel(scoreboard_frame,
                text=f"=== {diff_name} ===",
                font=("Courier New", 20, "bold"),
                text_color="#FFFFFF").pack(pady=5)
    
    center_container = ctk.CTkFrame(scoreboard_frame, 
                                  fg_color='#121212',
                                  corner_radius=10)
    center_container.pack(padx=20, pady=10)
    
    difficulty_scores = scores.get(difficulty_var.get(), [])
    if not difficulty_scores:
        ctk.CTkLabel(center_container,
                    text=texts[current_language]["no_scores"],
                    font=("Courier New", 16, "bold"),
                    text_color="#FF6B6B").pack(pady=3)
    else:
        header_frame = ctk.CTkFrame(center_container, fg_color='transparent')
        header_frame.pack(fill="x", padx=10)
        
        headers = {
            "en": ["RANK", "PLAYER", "SCORE", "TIME"],
            "fr": ["RANG", "JOUEUR", "SCORE", "TEMPS"]
        }
        
        header_content = ctk.CTkFrame(header_frame, fg_color='transparent')
        header_content.pack(padx=10)
        
        for header_text, width in zip(headers[current_language], [60, 120, 100, 100]):
            ctk.CTkLabel(header_content,
                        text=header_text,
                        font=("Courier New", 16, "bold"),
                        text_color="#FFFFFF",
                        width=width).pack(side="left", padx=5)
        
        scores_to_display = difficulty_scores[:5]
        rank_colors = ["#00BFFF", "#FF69B4", "#FFD700", "#FF4444", "#00FF00"]
        
        for i, score in enumerate(scores_to_display):
            score_frame = ctk.CTkFrame(center_container, fg_color='transparent')
            score_frame.pack(pady=2)
            
            row_content = ctk.CTkFrame(score_frame, fg_color='transparent')
            row_content.pack(padx=10)
            
            row_color = rank_colors[i]
            
            for text, width in zip([
                f"{i+1}.",
                score.get("name", texts[current_language]["default_name"]),
                str(score.get("score", "0")),
                f"{score.get('time', 0)}s"
            ], [60, 120, 100, 100]):
                ctk.CTkLabel(row_content,
                            text=text,
                            font=("Courier New", 16, "bold"),
                            text_color=row_color,
                            width=width).pack(side="left", padx=5)

welcome_screen = ctk.CTkFrame(master=window)
game_screen = ctk.CTkFrame(master=window)

welcome_label = ctk.CTkLabel(welcome_screen, 
                           text=texts[current_language]["welcome"],
                           font=("Arial", 24, "bold"))
welcome_label.configure(fg_color='transparent', text_color=COLORS['text'])
welcome_label.pack(pady=10)

instructions_label = ctk.CTkLabel(welcome_screen,
                                text=texts[current_language]["instructions"],
                                wraplength=600,
                                font=("Arial", 14),
                                justify="center")
instructions_label.pack(pady=10)

def on_difficulty_change():
    reset_game()
    update_scoreboard()

difficulty_frame = ctk.CTkFrame(welcome_screen, fg_color=COLORS['bg'])
difficulty_frame.pack(pady=10)
difficulty_label = ctk.CTkLabel(difficulty_frame, text=texts[current_language]["difficulty_label"], fg_color='transparent')
difficulty_label.pack(side="left")

for level, fr_level in zip(["Easy", "Medium", "Hard"], ["Facile", "Moyen", "Difficile"]):
    rb = ctk.CTkRadioButton(difficulty_frame, 
                           text=fr_level if current_language == "fr" else level,
                           variable=difficulty_var, 
                           value=level,
                           command=on_difficulty_change,
                           font=("Arial", 12),
                           fg_color=COLORS['button'])
    rb.pack(side="left", padx=10)
    rb.level = level
    rb.fr_level = fr_level

play_button = ctk.CTkButton(welcome_screen, 
                           text=texts[current_language]["play_button"], 
                           command=start_game,
                           width=200,
                           height=40,
                           fg_color="#2E7D32",
                           font=("Arial", 14, "bold"))
play_button.pack(pady=20)
play_button.configure(
    hover_color="#1B5E20"
)

language_button = ctk.CTkButton(welcome_screen,
                               text=texts[current_language]["change_language_button"],
                               command=lambda: change_language(difficulty_label),
                               width=200,
                               height=40,
                               fg_color="#F57C00",
                               font=("Arial", 14, "bold"))
language_button.pack(pady=10)
language_button.configure(
    hover_color="#EF6C00"
)

scoreboard_frame = ctk.CTkFrame(welcome_screen, fg_color=COLORS['bg'])
scoreboard_frame.pack(pady=10, padx=20, fill="x")

scoreboard_title = ctk.CTkLabel(scoreboard_frame, 
                               text=texts[current_language]["scoreboard"],
                               font=("Arial", 20, "bold"))
scoreboard_title.pack(pady=5)

update_scoreboard()

creator_label = ctk.CTkLabel(welcome_screen, 
                            text=texts[current_language]["creator_label"],
                            font=("Arial", 12, "italic"))
creator_label.pack(pady=(10, 20))

game_screen = ctk.CTkFrame(window)
game_screen.configure(fg_color=COLORS['bg'])

game_content_frame = ctk.CTkFrame(game_screen, fg_color=COLORS['bg'])
game_content_frame.pack(side="top", fill="both", expand=True)

instructions = ctk.CTkLabel(game_content_frame,
                          text=texts[current_language]["instructions_game"],
                          wraplength=600,
                          font=("Arial", 14),
                          justify="center")
instructions.pack(pady=10)

combo_frame = ctk.CTkFrame(game_content_frame, fg_color=COLORS['bg'])
combo_frame.pack(pady=10)

color_boxes = []
for i in range(4):
    option_menu = ctk.CTkOptionMenu(
        combo_frame,
        values=colors[current_language],
        command=lambda x, pos=i: on_color_selected(x, pos),
        width=150,
        height=40,
        font=("Arial", 14),
        dynamic_resizing=False,
        fg_color="#424242",
        button_color="#424242",
        button_hover_color="#616161"
    )
    option_menu.set(texts[current_language]["choose"])
    option_menu.pack(pady=5)
    color_boxes.append(option_menu)

attempts_label = ctk.CTkLabel(game_content_frame, 
                            text=f"{texts[current_language]['attempts_left']} {texts[current_language]['infinity']}", 
                            font=("Arial", 14))
attempts_label.pack(pady=10)

timer_label = ctk.CTkLabel(game_content_frame, 
                          text=f"{texts[current_language]['time_left']} --:--", 
                          font=("Arial", 14))
timer_label.pack(pady=10)

result_text = ctk.CTkTextbox(game_content_frame, 
                            height=100,
                            width=250,
                            font=("Arial", 12))
result_text.configure(fg_color='#121212', text_color=COLORS['text'])
result_text.pack(pady=20)
result_text._textbox.tag_configure("center", justify="center")

button_frame = ctk.CTkFrame(game_screen, fg_color=COLORS['bg'])
button_frame.pack(side="bottom", pady=20, fill="x", anchor="s")

buttons_container = ctk.CTkFrame(button_frame, fg_color=COLORS['bg'])
buttons_container.pack(expand=True)

validate_button = ctk.CTkButton(buttons_container, 
                               text=texts[current_language]["validate"], 
                               command=verify_proposition,
                               width=150,
                               height=40,
                               fg_color="#2E7D32",
                               font=("Arial", 12, "bold"))
validate_button.pack(side="left", padx=5)
validate_button.configure(hover_color="#1B5E20")

restart_button = ctk.CTkButton(buttons_container, 
                              text=texts[current_language]["restart"], 
                              command=confirm_restart,
                              width=150,
                              height=40,
                              fg_color="#1976D2",
                              font=("Arial", 12, "bold"))
restart_button.pack(side="left", padx=5)
restart_button.configure(hover_color="#1565C0")

return_button = ctk.CTkButton(buttons_container, 
                             text=texts[current_language]["return"], 
                             command=confirm_return,
                             width=150,
                             height=40,
                             fg_color="#C62828",
                             font=("Arial", 12, "bold"))
return_button.pack(side="left", padx=5)
return_button.configure(hover_color="#B71C1C")

welcome_screen.configure(fg_color=COLORS['bg'])
game_screen.configure(fg_color=COLORS['bg'])
difficulty_frame.configure(fg_color=COLORS['bg'])
combo_frame.configure(fg_color=COLORS['bg'])
button_frame.configure(fg_color=COLORS['bg'])

welcome_screen.pack(fill="both", expand=True)

class NameInputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title(texts[current_language]["enter_name"])
        self.geometry("250x200")
        self.configure(bg=COLORS['bg'])
        self.name = None
        
        self.frame = ctk.CTkFrame(self, fg_color=COLORS['bg'])
        self.frame.pack(expand=True, padx=20, pady=20)
        
        self.label = ctk.CTkLabel(self.frame, 
                                 text=texts[current_language]["enter_name"],
                                 font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.entry = ctk.CTkEntry(self.frame,
                                 width=200,
                                 font=("Arial", 14))
        self.entry.insert(0, texts[current_language]["default_name"])
        self.entry.pack(pady=10)
        
        self.button = ctk.CTkButton(self.frame, 
                                   text="OK",
                                   command=self.validate,
                                   font=("Arial", 14))
        self.button.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        self.entry.focus_set()

    def validate(self):
        entered_name = self.entry.get().strip()
        self.name = entered_name if entered_name else texts[current_language]["default_name"]
        self.destroy()

score_label = ctk.CTkLabel(game_content_frame,
                          text="Score: 0",
                          font=("Arial", 14, "bold"))
score_label.pack(pady=10)
def run_game(guess):
    """
    Fonction pour gérer une proposition (guess) envoyée via Flask.
    Retourne le résultat en termes de 'correct' et 'misplaced'.
    """
    global secret_combination  # Utiliser la combinaison secrète globale
    correct_positions = sum(1 for i in range(4) if guess[i] == secret_combination[i])
    misplaced_positions = sum(min(secret_combination.count(c), guess.count(c)) for c in set(guess)) - correct_positions

    return {
        "correct": correct_positions,
        "misplaced": misplaced_positions,
        "victory": correct_positions == 4
    }

window.mainloop()
