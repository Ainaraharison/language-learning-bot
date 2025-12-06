"""
Bot Telegram pour l'apprentissage de langue avec exercices MCQ
Similaire au workflow n8n mais en Python pur
"""

import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from modules.vocabulary_manager import VocabularyManager
from modules.conversation_memory import ConversationMemory

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # groq ou openai
MODEL_NAME = os.getenv("MODEL_NAME")

# Vérifications
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_BOT_TOKEN non trouvée dans .env")

# Initialisation du client IA selon le provider
ai_client = None
if AI_PROVIDER.lower() == "groq":
    if not GROQ_API_KEY:
        raise ValueError("⚠️ GROQ_API_KEY non trouvée dans .env. Obtenez-en une gratuite sur https://console.groq.com/keys")
    from groq import Groq
    ai_client = Groq(api_key=GROQ_API_KEY)
    if not MODEL_NAME:
        MODEL_NAME = "llama-3.3-70b-versatile"  # Modèle gratuit Groq
    print(f"🤖 Using Groq AI (FREE) - Model: {MODEL_NAME}")
else:
    if not OPENAI_API_KEY:
        raise ValueError("⚠️ OPENAI_API_KEY non trouvée dans .env")
    from openai import OpenAI
    ai_client = OpenAI(api_key=OPENAI_API_KEY)
    if not MODEL_NAME:
        MODEL_NAME = "gpt-4o-mini"
    print(f"🤖 Using OpenAI - Model: {MODEL_NAME}")

# Initialisation des managers
# AUTO_SCRAPE=True pour activer le scraping automatique de vocabulaire
AUTO_SCRAPE = os.getenv("AUTO_SCRAPE", "false").lower() == "true"
vocab_manager = VocabularyManager(auto_scrape=AUTO_SCRAPE)
memory_manager = ConversationMemory()


class LanguageLearningBot:
    """Bot Telegram pour l'apprentissage de langue"""
    
    def __init__(self):
        self.client = ai_client
        self.vocab = vocab_manager
        self.memory = memory_manager
        self.model = MODEL_NAME
        self.provider = AI_PROVIDER
        self.user_levels = {}  # Stocker le niveau par utilisateur
    
    def get_user_level(self, user_id: int) -> str:
        """Retourne le niveau de l'utilisateur (par défaut: beginner)"""
        return self.user_levels.get(user_id, "beginner")
    
    def set_user_level(self, user_id: int, level: str):
        """Change le niveau de l'utilisateur"""
        self.user_levels[user_id] = level
    
    def get_system_prompt(self, user_name: str, vocab_count: int, level: str = "beginner") -> str:
        """
        Génère le prompt système pour l'agent
        
        Args:
            user_name: Prénom de l'utilisateur
            vocab_count: Nombre de mots dans le vocabulaire
            level: Niveau de difficulté (beginner, intermediate, advanced)
        
        Returns:
            Prompt système
        """
        level_descriptions = {
            "beginner": "Use simple vocabulary and basic grammar. Explain clearly.",
            "intermediate": "Use moderate vocabulary and varied grammar structures.",
            "advanced": "Use complex vocabulary, idioms, and advanced grammar."
        }
        
        level_desc = level_descriptions.get(level, level_descriptions["beginner"])
        
        return f"""# Context
You are an AI-powered English tutor designed to help {user_name} learn and practice English vocabulary and grammar effectively.

# Student Level: {level.upper()}
{level_desc}

# Role
Your primary role is to generate interactive exercises (MCQs, fill-in-the-blank, grammar exercises) and evaluate the user's responses.

# Vocabulary
You have access to {vocab_count} vocabulary words covering general, business, and academic topics.

# Types of Exercises

## 1. Vocabulary MCQ
- Give a **definition in English** and provide 4 word choices
- Example:
  "What word means 'a place where goods are stored'?"
  A) warehouse
  B) transport
  C) contract
  D) delivery

## 2. Grammar Exercise
- Present a sentence with a grammar mistake or a fill-in-the-blank
- Example:
  "She ____ to the store yesterday."
  A) go
  B) goes
  C) went
  D) going

## 3. Usage Exercise
- Ask to use a word correctly in a sentence
- Provide 4 sentence choices with only one correct usage

# Rules for Exercise Generation
1. **Vary the exercise types** - Don't always do the same type
2. **Use the vocabulary list** when possible, but can introduce new related words
3. **Do NOT mark the correct answer with ✅** in the question
4. Ask the user to respond with **A, B, C, or D**
5. **Adapt difficulty** based on user performance

# Format Example
"Choose the correct word to complete the sentence:
'The company needs a new ____ for storage.'
A) delivery
B) warehouse
C) contract
D) transport"

# Evaluating User Responses
1. **Wait for the user's answer**. Do NOT assume correctness
2. If **CORRECT**:
   - "Great job! ✅ The correct answer is [Answer]."
   - Provide a brief explanation or usage example
3. If **INCORRECT**:
   - "Not quite! ❌ The correct answer is [Answer]."
   - Explain why it's correct and why their choice was wrong
4. If **INVALID** (not A/B/C/D):
   - "Please respond with A, B, C, or D."

# After Each Answer
- Always generate a **NEW question** automatically
- Vary between vocabulary, grammar, and usage exercises
- Make learning engaging and progressive

# Behavior & Tone
- Be encouraging and supportive
- Explain clearly in simple English
- Celebrate progress
- Make corrections constructive, not discouraging
- Keep responses concise but informative
"""
    
    async def get_ai_response(self, user_id: int, user_name: str, message: str) -> str:
        """
        Obtient une réponse de l'IA avec mémoire de conversation
        
        Args:
            user_id: ID Telegram de l'utilisateur
            user_name: Nom de l'utilisateur
            message: Message de l'utilisateur
        
        Returns:
            Réponse de l'IA
        """
        try:
            # Récupérer le nombre de mots dans le vocabulaire
            vocab_count = self.vocab.get_vocab_count()
            
            # Récupérer le niveau de l'utilisateur
            user_level = self.get_user_level(user_id)
            
            # Récupérer l'historique de conversation
            history = self.memory.get_conversation(user_id)
            
            # Construire les messages
            messages = [
                {
                    "role": "system",
                    "content": self.get_system_prompt(user_name, vocab_count, user_level)
                }
            ]
            
            # Ajouter l'historique
            messages.extend(history)
            
            # Ajouter le nouveau message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Appel à l'API (Groq/OpenAI) de manière asynchrone
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
            )
            
            assistant_message = response.choices[0].message.content
            
            # Sauvegarder dans la mémoire
            self.memory.add_message(user_id, "user", message)
            self.memory.add_message(user_id, "assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {e}")
            return "❌ Désolé, une erreur s'est produite. Réessayez."


# Instance globale du bot
bot = LanguageLearningBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /start - Accueil"""
    user = update.effective_user
    user_name = user.first_name or "there"
    
    welcome_message = f"""👋 Hello {user_name}! Welcome to your AI Language Tutor!

🎯 **What I can do:**
- Generate vocabulary MCQ questions
- Track your progress
- Provide instant feedback
- Help you learn efficiently

📚 **Available Commands:**
/start - Show this welcome message
/practice - Start a new practice session
/level - Change difficulty level (beginner/intermediate/advanced)
/vocab - View vocabulary statistics
/progress - View your learning progress
/clear - Clear conversation history
/help - Get help

**Ready to practice?** Just send me any message or use /practice to begin!
"""
    
    await update.message.reply_text(welcome_message)


async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /practice - Démarrer une session"""
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name or "there"
    
    # Réinitialiser la conversation pour une nouvelle session
    memory_manager.clear_conversation(user_id)
    
    # Générer la première question
    initial_message = "Generate a new MCQ question for me to practice."
    response = await bot.get_ai_response(user_id, user_name, initial_message)
    
    await update.message.reply_text(response)


async def vocab_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /vocab - Statistiques du vocabulaire"""
    stats = vocab_manager.get_statistics()
    await update.message.reply_text(stats)


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /progress - Progrès de l'utilisateur"""
    user_id = update.effective_user.id
    
    # Récupérer les statistiques de la mémoire
    conversation_count = memory_manager.get_message_count(user_id)
    
    progress_message = f"""📊 **Your Learning Progress**

💬 Messages exchanged: {conversation_count}
🎯 Practice sessions: Active

Keep practicing to improve your vocabulary! 🚀
"""
    
    await update.message.reply_text(progress_message)


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /clear - Effacer l'historique"""
    user_id = update.effective_user.id
    memory_manager.clear_conversation(user_id)
    
    await update.message.reply_text("✅ Conversation history cleared! Start fresh with /practice")


async def level_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /level - Changer le niveau"""
    user_id = update.effective_user.id
    current_level = bot.get_user_level(user_id)
    
    level_message = f"""📊 **Change Your Learning Level**

Current level: **{current_level.upper()}**

Choose your level:
1️⃣ /level_beginner - Simple vocabulary, basic grammar
2️⃣ /level_intermediate - Moderate vocabulary, varied grammar
3️⃣ /level_advanced - Complex vocabulary, idioms, advanced grammar

💡 Tip: Start with beginner if you're unsure!
"""
    
    await update.message.reply_text(level_message)


async def set_level_beginner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change niveau à débutant"""
    user_id = update.effective_user.id
    bot.set_user_level(user_id, "beginner")
    memory_manager.clear_conversation(user_id)
    await update.message.reply_text("✅ Level set to BEGINNER! Let's start with basics. Use /practice to begin!")


async def set_level_intermediate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change niveau à intermédiaire"""
    user_id = update.effective_user.id
    bot.set_user_level(user_id, "intermediate")
    memory_manager.clear_conversation(user_id)
    await update.message.reply_text("✅ Level set to INTERMEDIATE! Ready for more challenges. Use /practice!")


async def set_level_advanced(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change niveau à avancé"""
    user_id = update.effective_user.id
    bot.set_user_level(user_id, "advanced")
    memory_manager.clear_conversation(user_id)
    await update.message.reply_text("✅ Level set to ADVANCED! Let's tackle complex English. Use /practice!")


async def scrape_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /scrape - Scraper de nouveaux mots"""
    if not vocab_manager.auto_scrape:
        await update.message.reply_text("❌ Auto-scraping is disabled. Set AUTO_SCRAPE=true in .env to enable it.")
        return
    
    await update.message.reply_text("🔍 Scraping new vocabulary words from online dictionaries... Please wait.")
    
    # Scraper 15 nouveaux mots
    added = vocab_manager.scrape_and_add_words(count=15)
    
    if added > 0:
        total = vocab_manager.get_vocab_count()
        await update.message.reply_text(
            f"✅ Successfully added {added} new words!\n\n"
            f"📚 Total vocabulary: {total} words\n\n"
            f"Use /vocab to see statistics or /practice to start learning!"
        )
    else:
        await update.message.reply_text("❌ Could not scrape new words. Please try again later.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /help - Aide"""
    help_text = """🆘 **Help & Commands**

**Basic Commands:**
/start - Welcome message
/practice - Start new practice session
/level - Change difficulty level
/scrape - Scrape new vocabulary words (if enabled)
/vocab - Vocabulary statistics
/progress - Your learning progress
/clear - Clear conversation history
/help - Show this help

**How to Use:**
1. Use /practice to start
2. Answer MCQ questions with A, B, C, or D
3. Get instant feedback
4. Keep practicing!

**Tips:**
- Answer with just the letter (A, B, C, or D)
- New questions appear automatically after feedback
- Use /clear if you want to start fresh

Need more help? Just ask me anything! 💬
"""
    
    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère tous les messages texte"""
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name or "there"
    message = update.message.text
    
    # Afficher un indicateur de "typing..."
    await update.message.chat.send_action("typing")
    
    # Obtenir la réponse de l'IA
    response = await bot.get_ai_response(user_id, user_name, message)
    
    # Envoyer la réponse
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les erreurs"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again or use /help for assistance."
        )


def main():
    """Point d'entrée principal du bot"""
    
    print("🤖 Starting Language Learning Telegram Bot...")
    print(f"📱 Model: {MODEL_NAME}")
    print(f"📚 Vocabulary loaded: {vocab_manager.get_vocab_count()} words")
    print("✅ Bot is running! Press Ctrl+C to stop.\n")
    
    # Créer l'application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Ajouter les handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("practice", practice))
    application.add_handler(CommandHandler("level", level_command))
    application.add_handler(CommandHandler("level_beginner", set_level_beginner))
    application.add_handler(CommandHandler("level_intermediate", set_level_intermediate))
    application.add_handler(CommandHandler("level_advanced", set_level_advanced))
    application.add_handler(CommandHandler("scrape", scrape_words))
    application.add_handler(CommandHandler("vocab", vocab_stats))
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CommandHandler("clear", clear_history))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handler pour tous les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handler d'erreurs
    application.add_error_handler(error_handler)
    
    # Démarrer le bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
