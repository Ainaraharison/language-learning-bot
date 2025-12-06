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
vocab_manager = VocabularyManager()
memory_manager = ConversationMemory()


class LanguageLearningBot:
    """Bot Telegram pour l'apprentissage de langue"""
    
    def __init__(self):
        self.client = ai_client
        self.vocab = vocab_manager
        self.memory = memory_manager
        self.model = MODEL_NAME
        self.provider = AI_PROVIDER
    
    def get_system_prompt(self, user_name: str, vocab_list: list) -> str:
        """
        Génère le prompt système pour l'agent
        
        Args:
            user_name: Prénom de l'utilisateur
            vocab_list: Liste de vocabulaire
        
        Returns:
            Prompt système
        """
        return f"""# Context
You are an AI-powered English tutor designed to help {user_name} learn and practice English vocabulary and grammar effectively.

# Role
Your primary role is to generate interactive exercises (MCQs, fill-in-the-blank, grammar exercises) and evaluate the user's responses.

# Available Vocabulary List
{vocab_list}

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
            # Récupérer le vocabulaire
            vocab_list = self.vocab.get_vocabulary_list()
            
            # Récupérer l'historique de conversation
            history = self.memory.get_conversation(user_id)
            
            # Construire les messages
            messages = [
                {
                    "role": "system",
                    "content": self.get_system_prompt(user_name, vocab_list)
                }
            ]
            
            # Ajouter l'historique
            messages.extend(history)
            
            # Ajouter le nouveau message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Appel à l'API OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /help - Aide"""
    help_text = """🆘 **Help & Commands**

**Basic Commands:**
/start - Welcome message
/practice - Start new practice session
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
