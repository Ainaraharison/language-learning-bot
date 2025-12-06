"""
Module de génération d'exercices
"""

from typing import Dict, List
from openai import OpenAI
from config import Config


class ExerciseManager:
    """Gère la génération et la correction d'exercices"""
    
    def __init__(self, client: OpenAI, target_language: str, native_language: str):
        self.client = client
        self.target_language = target_language
        self.native_language = native_language
        self.config = Config()
        self.level = self.config.default_level
    
    def set_level(self, level: str):
        """Change le niveau de difficulté"""
        self.level = level
    
    def generate_exercise(self, exercise_type: str):
        """
        Génère un exercice du type spécifié
        
        Args:
            exercise_type: Type d'exercice (vocabulaire, grammaire, etc.)
        """
        exercise_generators = {
            "vocabulaire": self._generate_vocabulary_exercise,
            "grammaire": self._generate_grammar_exercise,
            "conjugaison": self._generate_conjugation_exercise,
            "comprehension": self._generate_comprehension_exercise,
            "traduction": self._generate_translation_exercise
        }
        
        generator = exercise_generators.get(exercise_type, self._generate_vocabulary_exercise)
        generator()
    
    def _generate_vocabulary_exercise(self):
        """Génère un exercice de vocabulaire"""
        print("\n📚 Exercice de Vocabulaire\n")
        
        prompt = f"""Crée un exercice de vocabulaire en {self.target_language} pour un niveau {self.level}.

Fournis:
1. Un thème (ex: la maison, le travail, les voyages)
2. 10 mots ou expressions avec leur traduction en {self.native_language}
3. 5 phrases d'exemple utilisant ces mots
4. 3 questions pour tester la compréhension

Format clair et numéroté."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
        
        # Interaction avec l'utilisateur
        print("\n" + "="*50)
        input("\nAppuyez sur Entrée pour voir les réponses...")
        
        # Obtenir les réponses
        answer_prompt = f"""Fournis les réponses aux questions de l'exercice de vocabulaire précédent.
Explique chaque réponse brièvement."""
        
        answers = self._get_exercise_content(answer_prompt)
        print("\n✅ Réponses:\n")
        print(answers)
    
    def _generate_grammar_exercise(self):
        """Génère un exercice de grammaire"""
        print("\n📖 Exercice de Grammaire\n")
        
        prompt = f"""Crée un exercice de grammaire en {self.target_language} pour un niveau {self.level}.

Fournis:
1. Un point de grammaire spécifique adapté au niveau {self.level}
2. Une explication claire en {self.native_language}
3. 3 exemples illustrant la règle
4. 5 phrases à compléter ou corriger
5. 3 phrases à traduire du {self.native_language} vers le {self.target_language}

Format clair et pédagogique."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
        
        print("\n" + "="*50)
        print("Faites l'exercice, puis appuyez sur Entrée pour voir les corrections...")
        input()
        
        answer_prompt = """Fournis les corrections complètes de l'exercice de grammaire.
Explique chaque réponse avec la règle grammaticale applicable."""
        
        answers = self._get_exercise_content(answer_prompt)
        print("\n✅ Corrections:\n")
        print(answers)
    
    def _generate_conjugation_exercise(self):
        """Génère un exercice de conjugaison"""
        print("\n🔄 Exercice de Conjugaison\n")
        
        prompt = f"""Crée un exercice de conjugaison en {self.target_language} pour un niveau {self.level}.

Fournis:
1. 2 verbes importants adaptés au niveau {self.level}
2. Les temps à pratiquer (selon le niveau)
3. Un tableau de conjugaison partiel à compléter
4. 5 phrases où il faut conjuguer les verbes correctement
5. 3 phrases de traduction utilisant ces conjugaisons

Sois pédagogique et progressif."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
        
        print("\n" + "="*50)
        input("Appuyez sur Entrée pour voir les réponses...")
        
        answer_prompt = """Fournis toutes les réponses de l'exercice de conjugaison.
Inclus les tableaux de conjugaison complets et les explications."""
        
        answers = self._get_exercise_content(answer_prompt)
        print("\n✅ Réponses:\n")
        print(answers)
    
    def _generate_comprehension_exercise(self):
        """Génère un exercice de compréhension de texte"""
        print("\n📰 Exercice de Compréhension\n")
        
        prompt = f"""Crée un exercice de compréhension écrite en {self.target_language} pour un niveau {self.level}.

Fournis:
1. Un texte court adapté au niveau (150-300 mots)
2. Le vocabulaire difficile avec traductions en {self.native_language}
3. 5 questions de compréhension (vrai/faux, choix multiple, ouvertes)
4. 2 questions d'opinion personnelle

Choisis un sujet intéressant et actuel."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
        
        print("\n" + "="*50)
        input("Lisez le texte et répondez aux questions. Appuyez sur Entrée pour les réponses...")
        
        answer_prompt = """Fournis les réponses aux questions de compréhension.
Pour les questions ouvertes, donne des exemples de bonnes réponses."""
        
        answers = self._get_exercise_content(answer_prompt)
        print("\n✅ Réponses:\n")
        print(answers)
    
    def _generate_translation_exercise(self):
        """Génère un exercice de traduction"""
        print("\n🔄 Exercice de Traduction\n")
        
        prompt = f"""Crée un exercice de traduction pour un niveau {self.level}.

Fournis:
1. 5 phrases du {self.native_language} vers le {self.target_language} (difficulté progressive)
2. 5 phrases du {self.target_language} vers le {self.native_language}
3. Inclus des points de grammaire et vocabulaire importants pour le niveau

Varie les temps, structures et thèmes."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
        
        print("\n" + "="*50)
        input("Traduisez les phrases. Appuyez sur Entrée pour voir les traductions...")
        
        answer_prompt = """Fournis les traductions correctes.
Pour chaque phrase, ajoute:
- Des traductions alternatives possibles
- Les points de grammaire importants
- Des notes culturelles si pertinent"""
        
        answers = self._get_exercise_content(answer_prompt)
        print("\n✅ Traductions:\n")
        print(answers)
    
    def _get_exercise_content(self, prompt: str) -> str:
        """
        Génère le contenu d'un exercice via l'API
        
        Args:
            prompt: Prompt de génération
        
        Returns:
            Contenu de l'exercice
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.config.get_system_prompt(
                            self.target_language,
                            self.native_language,
                            self.level
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Erreur lors de la génération de l'exercice: {e}"
    
    def custom_exercise(self, description: str):
        """
        Génère un exercice personnalisé selon la description
        
        Args:
            description: Description de l'exercice souhaité
        """
        print(f"\n🎯 Exercice Personnalisé\n")
        
        prompt = f"""L'utilisateur souhaite un exercice personnalisé: {description}

Crée un exercice adapté en {self.target_language} pour un niveau {self.level}.
Sois créatif et pédagogique."""
        
        exercise = self._get_exercise_content(prompt)
        print(exercise)
