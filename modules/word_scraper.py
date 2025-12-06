"""
Module pour scraper automatiquement des mots de vocabulaire depuis des dictionnaires en ligne
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordScraper:
    """Scraper pour extraire des mots de vocabulaire depuis des dictionnaires en ligne"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_merriam_webster_word_of_day(self) -> Optional[Dict[str, str]]:
        """
        Scrape le mot du jour de Merriam-Webster
        
        Returns:
            Dictionnaire avec word, definition, category
        """
        try:
            url = "https://www.merriam-webster.com/word-of-the-day"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le mot
            word_element = soup.find('h2', class_='word-header-txt')
            if not word_element:
                word_element = soup.find('h1')
            
            word = word_element.text.strip() if word_element else None
            
            # Extraire la définition
            definition_element = soup.find('div', class_='wod-definition-container')
            if not definition_element:
                definition_element = soup.find('p', class_='wod-intro')
            
            definition = None
            if definition_element:
                definition = definition_element.get_text(strip=True)
                # Nettoyer la définition
                definition = definition.split('.')[0] + '.'
                definition = definition[:200]  # Limiter la longueur
            
            if word and definition:
                logger.info(f"✅ Scraped from Merriam-Webster: {word}")
                return {
                    "word": word.lower(),
                    "definition": definition,
                    "category": "general"
                }
            
        except Exception as e:
            logger.error(f"❌ Error scraping Merriam-Webster: {e}")
        
        return None
    
    def scrape_free_dictionary(self, word: str) -> Optional[Dict[str, str]]:
        """
        Scrape la définition d'un mot depuis Free Dictionary API
        
        Args:
            word: Mot à rechercher
        
        Returns:
            Dictionnaire avec word, definition, category
        """
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                entry = data[0]
                
                # Extraire la première définition
                if 'meanings' in entry and len(entry['meanings']) > 0:
                    meaning = entry['meanings'][0]
                    
                    if 'definitions' in meaning and len(meaning['definitions']) > 0:
                        definition = meaning['definitions'][0]['definition']
                        
                        logger.info(f"✅ Scraped from Free Dictionary API: {word}")
                        return {
                            "word": word.lower(),
                            "definition": definition,
                            "category": "general"
                        }
            
        except Exception as e:
            logger.error(f"❌ Error scraping Free Dictionary API for '{word}': {e}")
        
        return None
    
    def scrape_oxford_learners(self, level: str = "intermediate") -> List[Dict[str, str]]:
        """
        Scrape des mots depuis Oxford Learner's Dictionaries
        
        Args:
            level: Niveau (beginner, intermediate, advanced)
        
        Returns:
            Liste de dictionnaires avec word, definition, category
        """
        words_list = []
        
        # Listes de mots par niveau (backup si le scraping échoue)
        word_lists = {
            "beginner": [
                "happy", "sad", "big", "small", "hot", "cold", "fast", "slow",
                "easy", "difficult", "strong", "weak", "clean", "dirty", "new", "old"
            ],
            "intermediate": [
                "achieve", "collaborate", "efficient", "flexible", "maintain",
                "objective", "relevant", "significant", "strategy", "innovative"
            ],
            "advanced": [
                "ameliorate", "paradigm", "ubiquitous", "exemplify", "juxtapose",
                "elucidate", "mitigate", "proliferate", "substantiate", "ambiguous"
            ]
        }
        
        selected_words = word_lists.get(level, word_lists["intermediate"])
        
        for word in selected_words[:10]:  # Limiter à 10 mots pour ne pas surcharger
            time.sleep(random.uniform(0.3, 0.8))  # Pause entre requêtes
            
            scraped_word = self.scrape_free_dictionary(word)
            if scraped_word:
                words_list.append(scraped_word)
        
        return words_list
    
    def scrape_common_words_list(self, count: int = 20) -> List[Dict[str, str]]:
        """
        Scrape une liste de mots courants en anglais
        
        Args:
            count: Nombre de mots à récupérer
        
        Returns:
            Liste de dictionnaires avec word, definition, category
        """
        words_list = []
        
        # Liste de mots académiques courants (Academic Word List)
        common_words = [
            "analyze", "approach", "area", "assess", "assume", "authority",
            "benefit", "concept", "consist", "constitute", "context", "contract",
            "create", "data", "define", "derive", "distribute", "economy",
            "environment", "establish", "estimate", "evaluate", "evident", "export",
            "factor", "finance", "formula", "function", "identify", "income",
            "indicate", "individual", "interpret", "involve", "issue", "labor",
            "legal", "legislate", "major", "method", "occur", "percent",
            "period", "policy", "principle", "proceed", "process", "require",
            "research", "respond", "role", "section", "sector", "significant",
            "similar", "source", "specific", "structure", "theory", "vary"
        ]
        
        # Mélanger et sélectionner
        selected = random.sample(common_words, min(count, len(common_words)))
        
        for word in selected:
            time.sleep(random.uniform(0.3, 0.8))  # Pause entre requêtes
            
            scraped_word = self.scrape_free_dictionary(word)
            if scraped_word:
                scraped_word['category'] = 'academic'  # Mots académiques
                words_list.append(scraped_word)
            
            if len(words_list) >= count:
                break
        
        logger.info(f"✅ Scraped {len(words_list)} words total")
        return words_list
    
    def get_words_by_category(self, category: str, count: int = 10) -> List[Dict[str, str]]:
        """
        Récupère des mots par catégorie
        
        Args:
            category: Catégorie (general, business, academic)
            count: Nombre de mots
        
        Returns:
            Liste de mots
        """
        category_words = {
            "general": [
                "happy", "create", "understand", "important", "different",
                "develop", "improve", "increase", "reduce", "provide"
            ],
            "business": [
                "revenue", "profit", "market", "invest", "strategy",
                "collaborate", "negotiate", "implement", "optimize", "stakeholder"
            ],
            "academic": [
                "analyze", "hypothesis", "methodology", "paradigm", "empirical",
                "synthesize", "correlation", "validate", "theory", "framework"
            ]
        }
        
        words = category_words.get(category, category_words["general"])
        words_list = []
        
        for word in random.sample(words, min(count, len(words))):
            time.sleep(random.uniform(0.3, 0.8))
            
            scraped_word = self.scrape_free_dictionary(word)
            if scraped_word:
                scraped_word['category'] = category
                words_list.append(scraped_word)
        
        return words_list


# Instance globale
scraper = WordScraper()


if __name__ == "__main__":
    # Test du scraper
    print("🔍 Testing word scraper...")
    
    # Test 1: Mot du jour
    print("\n1. Scraping word of the day...")
    word_of_day = scraper.scrape_merriam_webster_word_of_day()
    if word_of_day:
        print(f"   ✅ {word_of_day['word']}: {word_of_day['definition']}")
    
    # Test 2: Mot spécifique
    print("\n2. Scraping specific word 'achieve'...")
    specific_word = scraper.scrape_free_dictionary("achieve")
    if specific_word:
        print(f"   ✅ {specific_word['word']}: {specific_word['definition']}")
    
    # Test 3: Liste de mots
    print("\n3. Scraping list of common words...")
    words_list = scraper.scrape_common_words_list(5)
    print(f"   ✅ Scraped {len(words_list)} words")
    for w in words_list:
        print(f"   - {w['word']}: {w['definition'][:50]}...")
