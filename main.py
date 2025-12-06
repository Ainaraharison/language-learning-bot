"""
Agent IA d'apprentissage de langue
Un assistant intelligent pour apprendre une langue étrangère
"""

import os
from typing import Optional
from openai import OpenAI
from config import Config
from modules.conversation import ConversationManager
from modules.exercises import ExerciseManager
from modules.progress_tracker import ProgressTracker


class LanguageLearningAgent:
    """Agent IA principal pour l'apprentissage de langue"""
    
    def __init__(self, target_language: str = "anglais", native_language: str = "français"):
        """
        Initialise l'agent d'apprentissage
        
        Args:
            target_language: Langue à apprendre
            native_language: Langue maternelle de l'utilisateur
        """
        self.config = Config()
        self.client = OpenAI(api_key=self.config.api_key)
        self.target_language = target_language
        self.native_language = native_language
        
        # Modules de l'agent
        self.conversation = ConversationManager(self.client, target_language, native_language)
        self.exercises = ExerciseManager(self.client, target_language, native_language)
        self.progress = ProgressTracker()
        
        print(f"🤖 Agent d'apprentissage de {target_language} initialisé!")
        print(f"Langue maternelle: {native_language}\n")
    
    def start(self):
        """Démarre l'interface interactive de l'agent"""
        self.show_menu()
        
        while True:
            try:
                choice = input("\n🎯 Votre choix: ").strip()
                
                if choice == "1":
                    self.practice_conversation()
                elif choice == "2":
                    self.do_exercise()
                elif choice == "3":
                    self.get_feedback()
                elif choice == "4":
                    self.show_progress()
                elif choice == "5":
                    self.change_level()
                elif choice == "6":
                    print("\n👋 Au revoir! Continue à pratiquer!")
                    break
                else:
                    print("❌ Choix invalide. Essayez encore.")
                    self.show_menu()
                    
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir!")
                break
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
    
    def show_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*50)
        print("📚 AGENT D'APPRENTISSAGE DE LANGUE")
        print("="*50)
        print("1. 💬 Conversation libre")
        print("2. 📝 Exercices ciblés")
        print("3. 🎯 Corrections et feedback")
        print("4. 📊 Voir mes progrès")
        print("5. ⚙️  Changer de niveau")
        print("6. 🚪 Quitter")
        print("="*50)
    
    def practice_conversation(self):
        """Lance une session de conversation"""
        print("\n💬 Mode Conversation")
        print("Tapez 'menu' pour revenir au menu principal\n")
        
        # Obtenir un sujet de conversation
        topics = [
            "voyage et tourisme",
            "nourriture et cuisine",
            "travail et carrière",
            "loisirs et hobbies",
            "actualités et culture",
            "vie quotidienne"
        ]
        
        print("Sujets disponibles:")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")
        
        topic_choice = input("\nChoisissez un sujet (1-6) ou appuyez sur Entrée pour un sujet aléatoire: ").strip()
        
        if topic_choice and topic_choice.isdigit() and 1 <= int(topic_choice) <= len(topics):
            topic = topics[int(topic_choice) - 1]
        else:
            import random
            topic = random.choice(topics)
        
        print(f"\n🎭 Sujet: {topic}")
        self.conversation.start_conversation(topic)
    
    def do_exercise(self):
        """Lance un exercice d'apprentissage"""
        print("\n📝 Mode Exercices")
        print("="*40)
        print("1. Vocabulaire")
        print("2. Grammaire")
        print("3. Conjugaison")
        print("4. Compréhension de texte")
        print("5. Traduction")
        print("="*40)
        
        ex_choice = input("Type d'exercice (1-5): ").strip()
        
        exercise_types = {
            "1": "vocabulaire",
            "2": "grammaire",
            "3": "conjugaison",
            "4": "comprehension",
            "5": "traduction"
        }
        
        ex_type = exercise_types.get(ex_choice, "vocabulaire")
        self.exercises.generate_exercise(ex_type)
    
    def get_feedback(self):
        """Affiche les corrections et feedback"""
        print("\n🎯 Feedback et Corrections")
        text = input("Entrez votre texte pour correction: ").strip()
        
        if text:
            feedback = self.conversation.get_correction(text)
            print("\n" + feedback)
            self.progress.add_correction(text, feedback)
    
    def show_progress(self):
        """Affiche les statistiques de progrès"""
        print("\n📊 Vos Progrès")
        stats = self.progress.get_statistics()
        print(stats)
    
    def change_level(self):
        """Permet de changer le niveau de difficulté"""
        print("\n⚙️  Niveaux disponibles:")
        print("1. A1 - Débutant")
        print("2. A2 - Élémentaire")
        print("3. B1 - Intermédiaire")
        print("4. B2 - Intermédiaire avancé")
        print("5. C1 - Avancé")
        
        level_choice = input("Choisissez votre niveau (1-5): ").strip()
        levels = {"1": "A1", "2": "A2", "3": "B1", "4": "B2", "5": "C1"}
        
        new_level = levels.get(level_choice, "B1")
        self.conversation.set_level(new_level)
        self.exercises.set_level(new_level)
        print(f"✅ Niveau changé à: {new_level}")


def main():
    """Point d'entrée de l'application"""
    print("🌍 Bienvenue dans l'Agent d'Apprentissage de Langue!")
    
    # Demander la langue cible
    print("\nLangues disponibles:")
    languages = ["anglais", "espagnol", "allemand", "italien", "portugais", "japonais", "chinois"]
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang}")
    
    lang_choice = input("\nChoisissez une langue (1-7) ou tapez le nom: ").strip().lower()
    
    if lang_choice.isdigit() and 1 <= int(lang_choice) <= len(languages):
        target_language = languages[int(lang_choice) - 1]
    elif lang_choice in languages:
        target_language = lang_choice
    else:
        target_language = "anglais"
        print(f"Langue par défaut sélectionnée: {target_language}")
    
    # Créer et lancer l'agent
    agent = LanguageLearningAgent(target_language=target_language)
    agent.start()


if __name__ == "__main__":
    main()
