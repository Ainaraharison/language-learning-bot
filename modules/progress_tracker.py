"""
Module de suivi des progrès
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config import Config


class ProgressTracker:
    """Suit les progrès de l'utilisateur"""
    
    def __init__(self):
        self.config = Config()
        self.progress_file = self.config.data_dir / "progress" / "user_progress.json"
        self.data = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """Charge les données de progrès depuis le fichier"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "start_date": datetime.now().isoformat(),
                "total_sessions": 0,
                "conversations": [],
                "exercises_completed": [],
                "corrections": [],
                "vocabulary_learned": [],
                "time_spent_minutes": 0
            }
    
    def _save_progress(self):
        """Sauvegarde les données de progrès"""
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_session(self, duration_minutes: int = 0):
        """
        Enregistre une nouvelle session
        
        Args:
            duration_minutes: Durée de la session en minutes
        """
        self.data["total_sessions"] += 1
        self.data["time_spent_minutes"] += duration_minutes
        self._save_progress()
    
    def add_conversation(self, topic: str, message_count: int):
        """
        Enregistre une conversation
        
        Args:
            topic: Sujet de la conversation
            message_count: Nombre de messages échangés
        """
        self.data["conversations"].append({
            "date": datetime.now().isoformat(),
            "topic": topic,
            "message_count": message_count
        })
        self._save_progress()
    
    def add_exercise(self, exercise_type: str, score: float = None):
        """
        Enregistre un exercice complété
        
        Args:
            exercise_type: Type d'exercice
            score: Score obtenu (optionnel)
        """
        self.data["exercises_completed"].append({
            "date": datetime.now().isoformat(),
            "type": exercise_type,
            "score": score
        })
        self._save_progress()
    
    def add_correction(self, original_text: str, feedback: str):
        """
        Enregistre une correction
        
        Args:
            original_text: Texte original
            feedback: Feedback reçu
        """
        self.data["corrections"].append({
            "date": datetime.now().isoformat(),
            "original": original_text[:100],  # Limiter la longueur
            "feedback": feedback[:200]
        })
        self._save_progress()
    
    def add_vocabulary(self, words: List[str]):
        """
        Ajoute des mots au vocabulaire appris
        
        Args:
            words: Liste de mots appris
        """
        for word in words:
            if word not in self.data["vocabulary_learned"]:
                self.data["vocabulary_learned"].append(word)
        self._save_progress()
    
    def get_statistics(self) -> str:
        """
        Retourne les statistiques de progrès formatées
        
        Returns:
            Statistiques formatées
        """
        stats = []
        stats.append("="*50)
        stats.append("📊 VOS STATISTIQUES D'APPRENTISSAGE")
        stats.append("="*50)
        
        # Durée totale
        start_date = datetime.fromisoformat(self.data["start_date"])
        days_learning = (datetime.now() - start_date).days
        stats.append(f"\n🗓️  Apprentissage depuis: {days_learning} jours")
        
        # Sessions
        stats.append(f"📅 Sessions totales: {self.data['total_sessions']}")
        stats.append(f"⏱️  Temps total: {self.data['time_spent_minutes']} minutes")
        
        # Conversations
        conv_count = len(self.data["conversations"])
        stats.append(f"\n💬 Conversations: {conv_count}")
        if conv_count > 0:
            total_messages = sum(c["message_count"] for c in self.data["conversations"])
            stats.append(f"   Messages échangés: {total_messages}")
        
        # Exercices
        ex_count = len(self.data["exercises_completed"])
        stats.append(f"\n📝 Exercices complétés: {ex_count}")
        if ex_count > 0:
            ex_types = {}
            for ex in self.data["exercises_completed"]:
                ex_type = ex["type"]
                ex_types[ex_type] = ex_types.get(ex_type, 0) + 1
            
            stats.append("   Par type:")
            for ex_type, count in ex_types.items():
                stats.append(f"   - {ex_type}: {count}")
        
        # Corrections
        corr_count = len(self.data["corrections"])
        stats.append(f"\n🎯 Corrections reçues: {corr_count}")
        
        # Vocabulaire
        vocab_count = len(self.data["vocabulary_learned"])
        stats.append(f"\n📚 Mots appris: {vocab_count}")
        
        # Moyenne quotidienne
        if days_learning > 0:
            avg_sessions = self.data['total_sessions'] / days_learning
            avg_minutes = self.data['time_spent_minutes'] / days_learning
            stats.append(f"\n📈 Moyenne par jour:")
            stats.append(f"   Sessions: {avg_sessions:.1f}")
            stats.append(f"   Minutes: {avg_minutes:.1f}")
        
        # Conseils
        stats.append("\n" + "="*50)
        stats.append("💡 CONSEILS:")
        
        if self.data['total_sessions'] < 5:
            stats.append("   • Continue! La régularité est la clé du succès")
        
        if conv_count < ex_count / 2:
            stats.append("   • Essaye plus de conversations pour pratiquer!")
        
        if corr_count < 10:
            stats.append("   • N'hésite pas à demander des corrections")
        
        if self.data['time_spent_minutes'] < 60:
            stats.append("   • Vise 15-30 minutes par jour pour progresser")
        
        stats.append("="*50)
        
        return "\n".join(stats)
    
    def get_recent_activity(self, days: int = 7) -> str:
        """
        Retourne l'activité récente
        
        Args:
            days: Nombre de jours à afficher
        
        Returns:
            Activité formatée
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        activity = []
        activity.append(f"\n📅 Activité des {days} derniers jours:\n")
        
        # Conversations récentes
        recent_convs = [
            c for c in self.data["conversations"]
            if datetime.fromisoformat(c["date"]) > cutoff_date
        ]
        
        if recent_convs:
            activity.append(f"💬 {len(recent_convs)} conversations")
        
        # Exercices récents
        recent_exs = [
            e for e in self.data["exercises_completed"]
            if datetime.fromisoformat(e["date"]) > cutoff_date
        ]
        
        if recent_exs:
            activity.append(f"📝 {len(recent_exs)} exercices")
        
        if not recent_convs and not recent_exs:
            activity.append("Aucune activité récente. C'est le moment de pratiquer!")
        
        return "\n".join(activity)
    
    def reset_progress(self):
        """Réinitialise tous les progrès"""
        confirm = input("⚠️  Êtes-vous sûr de vouloir réinitialiser vos progrès? (oui/non): ")
        if confirm.lower() in ["oui", "yes", "y"]:
            self.data = {
                "start_date": datetime.now().isoformat(),
                "total_sessions": 0,
                "conversations": [],
                "exercises_completed": [],
                "corrections": [],
                "vocabulary_learned": [],
                "time_spent_minutes": 0
            }
            self._save_progress()
            print("✅ Progrès réinitialisés")
        else:
            print("❌ Réinitialisation annulée")
