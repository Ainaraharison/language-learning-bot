"""
Module de gestion des conversations
"""

from typing import List, Dict
from openai import OpenAI
from config import Config


class ConversationManager:
    """Gère les conversations d'apprentissage"""
    
    def __init__(self, client: OpenAI, target_language: str, native_language: str):
        self.client = client
        self.target_language = target_language
        self.native_language = native_language
        self.config = Config()
        self.level = self.config.default_level
        self.conversation_history: List[Dict] = []
    
    def set_level(self, level: str):
        """Change le niveau de difficulté"""
        self.level = level
        self.conversation_history = []  # Reset la conversation
    
    def start_conversation(self, topic: str):
        """
        Démarre une conversation sur un sujet donné
        
        Args:
            topic: Sujet de conversation
        """
        # Initialiser la conversation
        system_prompt = self.config.get_system_prompt(
            self.target_language, 
            self.native_language, 
            self.level
        )
        
        self.conversation_history = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Commence une conversation sur le sujet: {topic}"}
        ]
        
        # Obtenir le premier message de l'assistant
        response = self._get_response()
        print(f"\n🤖 Assistant: {response}\n")
        
        # Boucle de conversation
        while True:
            user_input = input("Vous: ").strip()
            
            if user_input.lower() in ["menu", "quit", "exit", "retour"]:
                break
            
            if not user_input:
                continue
            
            # Ajouter le message de l'utilisateur
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Obtenir la réponse
            response = self._get_response()
            print(f"\n🤖 Assistant: {response}\n")
            
            # Vérifier si l'utilisateur veut une correction
            if "?" in user_input or "correct" in user_input.lower():
                correction = self._check_for_errors(user_input)
                if correction:
                    print(f"💡 Correction: {correction}\n")
    
    def _get_response(self) -> str:
        """Obtient une réponse du modèle"""
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.conversation_history,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
            # Ajouter à l'historique
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"❌ Erreur lors de la génération de la réponse: {e}"
    
    def _check_for_errors(self, text: str) -> str:
        """
        Vérifie les erreurs dans le texte de l'utilisateur
        
        Args:
            text: Texte à vérifier
        
        Returns:
            Corrections suggérées
        """
        correction_prompt = f"""Analyse ce texte en {self.target_language} et fournis des corrections si nécessaire:
"{text}"

Si il y a des erreurs, donne:
1. La version corrigée
2. Explication brève en {self.native_language}
3. Un exemple similaire correct

Si le texte est parfait, félicite l'utilisateur."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.config.get_system_prompt(
                        self.target_language, self.native_language, self.level
                    )},
                    {"role": "user", "content": correction_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Erreur lors de la correction: {e}"
    
    def get_correction(self, text: str) -> str:
        """
        Obtient une correction détaillée d'un texte
        
        Args:
            text: Texte à corriger
        
        Returns:
            Feedback détaillé
        """
        return self._check_for_errors(text)
    
    def save_conversation(self, filename: str = None):
        """Sauvegarde la conversation actuelle"""
        import json
        from datetime import datetime
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        filepath = self.config.data_dir / "conversations" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Conversation sauvegardée: {filepath}")
