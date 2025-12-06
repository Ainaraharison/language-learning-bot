"""
Module de gestion du vocabulaire
Peut charger depuis un fichier CSV, JSON, Google Sheets ou scraper en ligne
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple
import random
import os
class VocabularyManager:
    """Gère le vocabulaire pour les exercices"""
    
    def __init__(self, vocab_file: str = None, auto_scrape: bool = False):
        """
        Initialise le gestionnaire de vocabulaire
        
        Args:
            vocab_file: Chemin vers le fichier de vocabulaire (optionnel)
            auto_scrape: Si True, scrape automatiquement des mots en ligne
        """
        self.vocab_file = vocab_file
        self.vocabulary: List[Dict[str, str]] = []
        self.auto_scrape = auto_scrape
        self.scraper = None
        
        # Initialiser le scraper si demandé
        if self.auto_scrape:
            try:
                from .word_scraper import WordScraper
                self.scraper = WordScraper()
                print("✅ Web scraper initialized")
            except ImportError:
                print("⚠️ Could not import word_scraper, auto-scraping disabled")
                self.auto_scrape = False
        
        self.load_vocabulary()
    
    def load_vocabulary(self):
        """Charge le vocabulaire depuis un fichier ou utilise des exemples par défaut"""
        if self.vocab_file and Path(self.vocab_file).exists():
            # Charger depuis un fichier
            file_ext = Path(self.vocab_file).suffix.lower()
            
            if file_ext == '.json':
                self._load_from_json()
            elif file_ext == '.csv':
                self._load_from_csv()
            else:
                print(f"⚠️ Format de fichier non supporté: {file_ext}")
                self._load_default_vocabulary()
        else:
            # Utiliser le vocabulaire par défaut
            self._load_default_vocabulary()
    
    def _load_from_json(self):
        """Charge le vocabulaire depuis un fichier JSON"""
        try:
            with open(self.vocab_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Format attendu: [{"chinese": "词汇", "english": "vocabulary"}, ...]
                if isinstance(data, list):
                    self.vocabulary = data
                    print(f"✅ Vocabulaire chargé: {len(self.vocabulary)} mots depuis {self.vocab_file}")
                else:
                    print("⚠️ Format JSON invalide")
                    self._load_default_vocabulary()
        except Exception as e:
            print(f"❌ Erreur lors du chargement du JSON: {e}")
            self._load_default_vocabulary()
    
    def _load_from_csv(self):
        """Charge le vocabulaire depuis un fichier CSV"""
        try:
            with open(self.vocab_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.vocabulary = []
                
                for row in reader:
                    # Nouveau format anglais avec définitions
                    if 'word' in row and 'definition' in row:
                        self.vocabulary.append({
                            'word': row['word'],
                            'definition': row['definition'],
                            'category': row.get('category', 'general')
                        })
                    # Ancien format chinois->anglais (rétrocompatibilité)
                    elif 'chinese' in row and 'english' in row:
                        self.vocabulary.append({
                            'chinese': row['chinese'],
                            'english': row['english']
                        })
                    elif 'initialText' in row and 'translatedText' in row:
                        # Format Google Sheets du workflow n8n
                        self.vocabulary.append({
                            'chinese': row['initialText'],
                            'english': row['translatedText']
                        })
                
                print(f"✅ Vocabulaire chargé: {len(self.vocabulary)} mots depuis {self.vocab_file}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du CSV: {e}")
            self._load_default_vocabulary()
    
    def _load_default_vocabulary(self):
        """Charge un vocabulaire par défaut en anglais pour les démonstrations"""
        self.vocabulary = [
            {"word": "warehouse", "definition": "a large building for storing goods", "category": "business"},
            {"word": "accomplish", "definition": "to succeed in doing something", "category": "general"},
            {"word": "accurate", "definition": "correct and exact", "category": "general"},
            {"word": "achieve", "definition": "to successfully complete something", "category": "general"},
            {"word": "analyze", "definition": "to examine something in detail", "category": "academic"},
            {"word": "approach", "definition": "a way of dealing with something", "category": "general"},
            {"word": "appropriate", "definition": "suitable or right for a situation", "category": "general"},
            {"word": "approximately", "definition": "close to a particular number or time", "category": "general"},
            {"word": "benefit", "definition": "an advantage or useful effect", "category": "general"},
            {"word": "challenge", "definition": "something difficult that tests your ability", "category": "general"},
            {"word": "collaborate", "definition": "to work together with others", "category": "business"},
            {"word": "complex", "definition": "having many parts and difficult to understand", "category": "academic"},
            {"word": "concept", "definition": "an idea or principle", "category": "academic"},
            {"word": "consequence", "definition": "a result of an action", "category": "general"},
            {"word": "considerable", "definition": "large in amount or importance", "category": "general"},
            {"word": "contribute", "definition": "to give something to help achieve a result", "category": "general"},
            {"word": "create", "definition": "to make something new", "category": "general"},
            {"word": "demonstrate", "definition": "to show or prove something", "category": "academic"},
            {"word": "develop", "definition": "to grow or create over time", "category": "general"},
            {"word": "efficient", "definition": "working well without wasting time or energy", "category": "business"},
            {"word": "emphasize", "definition": "to give special importance to something", "category": "academic"},
            {"word": "enhance", "definition": "to improve the quality of something", "category": "general"},
            {"word": "environment", "definition": "the surroundings or conditions", "category": "general"},
            {"word": "establish", "definition": "to create or set up something", "category": "business"},
            {"word": "evaluate", "definition": "to judge the value or quality of something", "category": "academic"},
            {"word": "evidence", "definition": "facts that prove something is true", "category": "academic"},
            {"word": "flexible", "definition": "able to change or adapt easily", "category": "general"},
            {"word": "fundamental", "definition": "forming a necessary base or core", "category": "academic"},
            {"word": "generate", "definition": "to produce or create something", "category": "business"},
            {"word": "implement", "definition": "to put a plan into action", "category": "business"},
            {"word": "indicate", "definition": "to show or point out", "category": "academic"},
            {"word": "interpret", "definition": "to explain the meaning of something", "category": "academic"},
            {"word": "involve", "definition": "to include as a necessary part", "category": "general"},
            {"word": "maintain", "definition": "to keep something in good condition", "category": "general"},
            {"word": "method", "definition": "a way of doing something", "category": "academic"},
            {"word": "objective", "definition": "a goal or aim", "category": "business"},
            {"word": "obtain", "definition": "to get or acquire something", "category": "general"},
            {"word": "opportunity", "definition": "a chance to do something", "category": "general"},
            {"word": "overcome", "definition": "to successfully deal with a problem", "category": "general"},
            {"word": "participate", "definition": "to take part in an activity", "category": "general"},
            {"word": "perspective", "definition": "a particular way of viewing something", "category": "academic"},
            {"word": "potential", "definition": "having the capacity to develop", "category": "general"},
            {"word": "previous", "definition": "existing or happening before", "category": "general"},
            {"word": "primary", "definition": "most important or main", "category": "academic"},
            {"word": "principle", "definition": "a basic truth or rule", "category": "academic"},
            {"word": "procedure", "definition": "a way of doing something with steps", "category": "business"},
            {"word": "relevant", "definition": "closely connected to what is being discussed", "category": "academic"},
            {"word": "require", "definition": "to need something", "category": "general"},
            {"word": "significant", "definition": "important or noticeable", "category": "academic"},
            {"word": "strategy", "definition": "a plan to achieve a goal", "category": "business"},
        ]
        print(f"✅ English vocabulary loaded: {len(self.vocabulary)} words")
    
    def get_vocabulary_list(self) -> List[str]:
        """
        Retourne la liste complète du vocabulaire formatée pour l'IA
        
        Returns:
            Liste formatée des mots avec définitions
        """
        vocab_formatted = []
        for item in self.vocabulary:
            if 'definition' in item:
                vocab_formatted.append(f"{item['word']}: {item['definition']}")
            elif 'english' in item:
                # Support ancien format chinois->anglais
                vocab_formatted.append(item['english'])
        return vocab_formatted
    
    def get_random_word(self) -> Dict[str, str]:
        """
        Retourne un mot aléatoire avec sa définition
        
        Returns:
            Dictionnaire avec word, definition, category
        """
        return random.choice(self.vocabulary)
    
    def get_random_words(self, count: int) -> List[Dict[str, str]]:
        """
        Retourne plusieurs mots aléatoires
        
        Args:
            count: Nombre de mots
        
        Returns:
            Liste de dictionnaires avec mots et définitions
        """
        return random.sample(self.vocabulary, min(count, len(self.vocabulary)))
    
    def find_word_by_name(self, word: str) -> Dict[str, str]:
        """
        Trouve un mot par son nom
        
        Args:
            word: Mot à rechercher
        
        Returns:
            Dictionnaire du mot ou None
        """
        for item in self.vocabulary:
            if 'word' in item and item['word'].lower() == word.lower():
                return item
            elif 'english' in item and item['english'].lower() == word.lower():
                return item
        return None
    
    def get_words_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        Retourne les mots d'une catégorie
        
        Args:
            category: Catégorie (general, business, academic)
        
        Returns:
            Liste de mots de cette catégorie
        """
        return [item for item in self.vocabulary if item.get('category') == category]
    
    def get_vocab_count(self) -> int:
        """Retourne le nombre de mots dans le vocabulaire"""
        return len(self.vocabulary)
    
    def scrape_and_add_words(self, count: int = 10, category: str = None) -> int:
        """
        Scrape et ajoute de nouveaux mots au vocabulaire
        
        Args:
            count: Nombre de mots à scraper
            category: Catégorie (general, business, academic) ou None pour aléatoire
        
        Returns:
            Nombre de mots ajoutés
        """
        if not self.scraper:
            print("⚠️ Scraper not initialized. Set auto_scrape=True")
            return 0
        
        try:
            print(f"🔍 Scraping {count} new words...")
            
            if category:
                new_words = self.scraper.get_words_by_category(category, count)
            else:
                new_words = self.scraper.scrape_common_words_list(count)
            
            # Éviter les doublons
            existing_words = {w['word'].lower() for w in self.vocabulary}
            unique_words = [w for w in new_words if w['word'].lower() not in existing_words]
            
            self.vocabulary.extend(unique_words)
            
            # Sauvegarder dans un fichier JSON
            self._save_to_json()
            
            print(f"✅ Added {len(unique_words)} new words ({len(new_words) - len(unique_words)} duplicates skipped)")
            return len(unique_words)
            
        except Exception as e:
            print(f"❌ Error scraping words: {e}")
            return 0
    
    def _save_to_json(self, filename: str = "data/vocabulary_scraped.json"):
        """Sauvegarde le vocabulaire dans un fichier JSON"""
        try:
            # Créer le dossier data si nécessaire
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Vocabulary saved to {filename}")
        except Exception as e:
            print(f"⚠️ Could not save vocabulary: {e}")
    
    def get_statistics(self) -> str:
        """
        Retourne les statistiques du vocabulaire
        
        Returns:
            Statistiques formatées
        """
        stats = []
        stats.append("📚 **Vocabulary Statistics**\n")
        stats.append(f"Total words: {len(self.vocabulary)}")
        
        if self.vocabulary:
            # Compter par catégorie
            categories = {}
            for word in self.vocabulary:
                cat = word.get('category', 'general')
                categories[cat] = categories.get(cat, 0) + 1
            
            stats.append("\n**By category:**")
            for cat, count in categories.items():
                stats.append(f"• {cat}: {count} words")
            
            # Quelques exemples
            stats.append("\n**Sample words:**")
            samples = random.sample(self.vocabulary, min(5, len(self.vocabulary)))
            for word in samples:
                if 'word' in word:
                    stats.append(f"• {word['word']}: {word.get('definition', 'N/A')}")
                elif 'english' in word:
                    stats.append(f"• {word.get('chinese', 'N/A')} - {word['english']}")
        
        return "\n".join(stats)
    
    def add_word(self, word: str, definition: str, category: str = "general"):
        """
        Ajoute un nouveau mot au vocabulaire
        
        Args:
            word: Mot anglais
            definition: Définition en anglais
            category: Catégorie (general, business, academic)
        """
        self.vocabulary.append({
            'word': word,
            'definition': definition,
            'category': category
        })
    
    def save_vocabulary(self, filename: str = "vocabulary.json"):
        """
        Sauvegarde le vocabulaire dans un fichier JSON
        
        Args:
            filename: Nom du fichier
        """
        filepath = Path("data") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Vocabulaire sauvegardé: {filepath}")
    
    def load_from_google_sheets(self, spreadsheet_id: str, sheet_name: str = "Sheet1"):
        """
        Charge le vocabulaire depuis Google Sheets (similaire au workflow n8n)
        Nécessite la configuration de l'API Google Sheets
        
        Args:
            spreadsheet_id: ID du Google Sheet
            sheet_name: Nom de la feuille
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Note: Nécessite la configuration OAuth2
            # Pour simplifier, on peut utiliser un CSV exporté depuis Google Sheets
            print("⚠️ Pour utiliser Google Sheets, exportez en CSV et chargez le fichier")
            print(f"   Ou implémentez l'authentification Google API")
            
        except ImportError:
            print("❌ google-api-python-client non installé")
            print("   Installez avec: pip install google-api-python-client google-auth")
