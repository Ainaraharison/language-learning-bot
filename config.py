"""
Configuration de l'agent d'apprentissage
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class Config:
    """Configuration de l'application"""
    
    def __init__(self):
        # API Keys
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "⚠️  OPENAI_API_KEY non trouvée!\n"
                "Créez un fichier .env avec votre clé API:\n"
                "OPENAI_API_KEY=votre_clé_ici"
            )
        
        # Paramètres du modèle
        self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        
        # Paramètres de l'application
        self.default_level = os.getenv("DEFAULT_LEVEL", "B1")
        self.data_dir = Path(os.getenv("DATA_DIR", "./data"))
        
        # Créer les dossiers nécessaires
        self.data_dir.mkdir(exist_ok=True)
        (self.data_dir / "progress").mkdir(exist_ok=True)
        (self.data_dir / "conversations").mkdir(exist_ok=True)
    
    def get_system_prompt(self, target_language: str, native_language: str, level: str) -> str:
        """
        Génère le prompt système pour l'agent
        
        Args:
            target_language: Langue à apprendre
            native_language: Langue maternelle
            level: Niveau CECRL (A1, A2, B1, B2, C1, C2)
        
        Returns:
            Prompt système formaté
        """
        return f"""Tu es un professeur de {target_language} expert et patient. 
Tu enseignes à un élève de langue maternelle {native_language} qui a un niveau {level}.

Tes responsabilités:
1. Avoir des conversations naturelles en {target_language}
2. Corriger les erreurs de manière constructive
3. Adapter ton vocabulaire et ta grammaire au niveau {level}
4. Donner des explications en {native_language} quand nécessaire
5. Encourager et motiver l'élève
6. Proposer des exercices pertinents

Style d'enseignement:
- Sois encourageant et positif
- Utilise des exemples concrets
- Explique clairement les règles de grammaire
- Donne du contexte culturel quand c'est pertinent
- Adapte-toi au rythme de l'élève

Niveau {level}:
{self._get_level_description(level)}
"""
    
    def _get_level_description(self, level: str) -> str:
        """Retourne la description du niveau CECRL"""
        descriptions = {
            "A1": "Débutant - Phrases simples, présent, vocabulaire de base (200-500 mots)",
            "A2": "Élémentaire - Conversations quotidiennes simples, passé/futur basique (500-1000 mots)",
            "B1": "Intermédiaire - Conversations sur sujets familiers, tous les temps principaux (1000-2000 mots)",
            "B2": "Intermédiaire avancé - Discussions complexes, nuances, subjonctif (2000-4000 mots)",
            "C1": "Avancé - Maîtrise avancée, textes complexes, idiomes (4000-8000 mots)",
            "C2": "Maîtrise - Niveau natif, subtilités linguistiques (8000+ mots)"
        }
        return descriptions.get(level, descriptions["B1"])
