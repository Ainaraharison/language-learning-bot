"""
Module de gestion de la mémoire de conversation
Stocke l'historique des conversations par utilisateur (par chat_id)
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class ConversationMemory:
    """Gère la mémoire des conversations par utilisateur"""
    
    def __init__(self, max_messages: int = 20):
        """
        Initialise le gestionnaire de mémoire
        
        Args:
            max_messages: Nombre maximum de messages à conserver par conversation
        """
        self.max_messages = max_messages
        self.conversations: Dict[int, List[Dict]] = {}
        self.data_dir = Path("data/conversations")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def add_message(self, user_id: int, role: str, content: str):
        """
        Ajoute un message à l'historique de conversation
        
        Args:
            user_id: ID Telegram de l'utilisateur
            role: Rôle ('user' ou 'assistant')
            content: Contenu du message
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversations[user_id].append(message)
        
        # Limiter la taille de l'historique (fenêtre glissante)
        if len(self.conversations[user_id]) > self.max_messages:
            self.conversations[user_id] = self.conversations[user_id][-self.max_messages:]
        
        # Sauvegarder automatiquement
        self._save_conversation(user_id)
    
    def get_conversation(self, user_id: int) -> List[Dict]:
        """
        Récupère l'historique de conversation d'un utilisateur
        
        Args:
            user_id: ID Telegram de l'utilisateur
        
        Returns:
            Liste des messages (format OpenAI)
        """
        if user_id not in self.conversations:
            # Essayer de charger depuis le disque
            self._load_conversation(user_id)
        
        if user_id not in self.conversations:
            return []
        
        # Retourner uniquement role et content (format OpenAI)
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversations[user_id]
        ]
    
    def clear_conversation(self, user_id: int):
        """
        Efface l'historique de conversation d'un utilisateur
        
        Args:
            user_id: ID Telegram de l'utilisateur
        """
        if user_id in self.conversations:
            # Sauvegarder l'historique avant de l'effacer (backup)
            self._backup_conversation(user_id)
            del self.conversations[user_id]
        
        # Supprimer le fichier
        file_path = self.data_dir / f"user_{user_id}.json"
        if file_path.exists():
            file_path.unlink()
    
    def get_message_count(self, user_id: int) -> int:
        """
        Retourne le nombre de messages dans la conversation
        
        Args:
            user_id: ID Telegram de l'utilisateur
        
        Returns:
            Nombre de messages
        """
        if user_id not in self.conversations:
            self._load_conversation(user_id)
        
        return len(self.conversations.get(user_id, []))
    
    def get_last_message(self, user_id: int) -> Dict:
        """
        Retourne le dernier message de la conversation
        
        Args:
            user_id: ID Telegram de l'utilisateur
        
        Returns:
            Dernier message ou None
        """
        conversation = self.get_conversation(user_id)
        return conversation[-1] if conversation else None
    
    def _save_conversation(self, user_id: int):
        """
        Sauvegarde la conversation sur le disque
        
        Args:
            user_id: ID Telegram de l'utilisateur
        """
        if user_id not in self.conversations:
            return
        
        file_path = self.data_dir / f"user_{user_id}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversations[user_id], f, ensure_ascii=False, indent=2)
    
    def _load_conversation(self, user_id: int):
        """
        Charge la conversation depuis le disque
        
        Args:
            user_id: ID Telegram de l'utilisateur
        """
        file_path = self.data_dir / f"user_{user_id}.json"
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.conversations[user_id] = json.load(f)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de la conversation {user_id}: {e}")
                self.conversations[user_id] = []
    
    def _backup_conversation(self, user_id: int):
        """
        Crée une sauvegarde de la conversation
        
        Args:
            user_id: ID Telegram de l'utilisateur
        """
        if user_id not in self.conversations:
            return
        
        backup_dir = self.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"user_{user_id}_{timestamp}.json"
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversations[user_id], f, ensure_ascii=False, indent=2)
    
    def get_all_users(self) -> List[int]:
        """
        Retourne la liste de tous les utilisateurs avec des conversations
        
        Returns:
            Liste des IDs utilisateurs
        """
        users = set(self.conversations.keys())
        
        # Ajouter les utilisateurs depuis les fichiers
        for file in self.data_dir.glob("user_*.json"):
            try:
                user_id = int(file.stem.split("_")[1])
                users.add(user_id)
            except:
                pass
        
        return list(users)
    
    def get_statistics(self) -> str:
        """
        Retourne les statistiques globales
        
        Returns:
            Statistiques formatées
        """
        users = self.get_all_users()
        total_messages = sum(self.get_message_count(u) for u in users)
        
        stats = []
        stats.append("📊 **Conversation Statistics**\n")
        stats.append(f"Total users: {len(users)}")
        stats.append(f"Total messages: {total_messages}")
        
        if users:
            avg_messages = total_messages / len(users)
            stats.append(f"Average messages per user: {avg_messages:.1f}")
        
        return "\n".join(stats)
    
    def export_conversation(self, user_id: int, format: str = "txt") -> str:
        """
        Exporte une conversation dans un format lisible
        
        Args:
            user_id: ID Telegram de l'utilisateur
            format: Format d'export ('txt' ou 'json')
        
        Returns:
            Chemin du fichier exporté
        """
        if user_id not in self.conversations:
            self._load_conversation(user_id)
        
        if user_id not in self.conversations:
            return None
        
        export_dir = self.data_dir / "exports"
        export_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "txt":
            file_path = export_dir / f"conversation_{user_id}_{timestamp}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Conversation Export - User {user_id}\n")
                f.write(f"Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for msg in self.conversations[user_id]:
                    role = "🧑 User" if msg["role"] == "user" else "🤖 Assistant"
                    timestamp = msg.get("timestamp", "")
                    f.write(f"{role} [{timestamp}]:\n")
                    f.write(f"{msg['content']}\n\n")
                    f.write("-" * 50 + "\n\n")
        
        elif format == "json":
            file_path = export_dir / f"conversation_{user_id}_{timestamp}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "user_id": user_id,
                    "export_date": datetime.now().isoformat(),
                    "messages": self.conversations[user_id]
                }, f, ensure_ascii=False, indent=2)
        
        return str(file_path)
