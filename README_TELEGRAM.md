# 🤖 Bot Telegram d'Apprentissage de Langue

Un bot Telegram intelligent pour pratiquer le vocabulaire avec des questions à choix multiples (MCQ), identique au workflow n8n mais en Python pur.

## 🌟 Fonctionnalités

- 📱 **Interface Telegram** - Apprenez directement depuis votre téléphone
- 🎯 **Questions MCQ** - Questions à choix multiples interactives
- 🧠 **Mémoire de conversation** - Le bot se souvient de votre historique par chat ID
- 📚 **Vocabulaire personnalisable** - Utilisez votre propre liste de mots
- ✅ **Feedback instantané** - Corrections et encouragements en temps réel
- 📊 **Suivi de progrès** - Statistiques de votre apprentissage

## 🎮 Commandes Disponibles

```
/start - Message de bienvenue
/practice - Démarrer une nouvelle session d'exercices
/vocab - Voir les statistiques du vocabulaire
/progress - Voir vos progrès
/clear - Effacer l'historique de conversation
/help - Afficher l'aide
```

## 🚀 Installation

### Étape 1: Installer les dépendances

```powershell
cd "e:\Professionnal Legend\project_perso\language_learning_agent"

# Activer l'environnement virtuel (si créé)
.\venv\Scripts\Activate.ps1

# Installer les nouvelles dépendances
pip install -r requirements.txt
```

### Étape 2: Créer un Bot Telegram

1. **Ouvrez Telegram** et cherchez `@BotFather`
2. **Envoyez** `/newbot`
3. **Suivez les instructions** :
   - Donnez un nom à votre bot (ex: "My Language Tutor")
   - Donnez un username (doit finir par "bot", ex: "mylanguage_tutor_bot")
4. **Copiez le token** que BotFather vous donne

Exemple de token : `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Étape 3: Configurer le fichier .env

Éditez votre fichier `.env` et ajoutez le token Telegram :

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-votre-clé-ici

# Telegram Bot Token (NOUVEAU)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Modèle
MODEL_NAME=gpt-4o-mini
```

### Étape 4: Lancer le Bot

```powershell
python telegram_bot.py
```

Vous devriez voir :
```
🤖 Starting Language Learning Telegram Bot...
📱 Model: gpt-4o-mini
📚 Vocabulary loaded: 40 words
✅ Bot is running! Press Ctrl+C to stop.
```

## 📱 Utilisation

### 1. Démarrer une conversation

Ouvrez Telegram et cherchez votre bot par son username. Envoyez `/start`.

```
Vous: /start

Bot: 👋 Hello! Welcome to your AI Language Tutor!

🎯 What I can do:
- Generate vocabulary MCQ questions
- Track your progress
- Provide instant feedback
- Help you learn efficiently

Ready to practice? Just send me any message or use /practice to begin!
```

### 2. Pratiquer avec des MCQ

```
Vous: /practice

Bot: What is the correct translation for "仓库"?
A) transportation
B) warehouse
C) contract
D) bid

Vous: B

Bot: Great job! ✅ warehouse means 仓库.

What is the correct translation for "运输"?
A) invoice
B) supplier
C) transportation
D) customer
```

### 3. Voir vos statistiques

```
Vous: /vocab

Bot: 📚 Vocabulary Statistics

Total words: 40

Sample words:
• 仓库 - warehouse
• 运输 - transportation
• 合同 - contract
```

## 📚 Personnaliser le Vocabulaire

### Option 1: Fichier JSON

Créez `data/vocabulary.json` :

```json
[
  {"chinese": "你好", "english": "hello"},
  {"chinese": "谢谢", "english": "thank you"},
  {"chinese": "再见", "english": "goodbye"}
]
```

Puis dans `.env` :
```bash
VOCABULARY_FILE=./data/vocabulary.json
```

### Option 2: Fichier CSV

Créez `data/vocabulary.csv` :

```csv
chinese,english
你好,hello
谢谢,thank you
再见,goodbye
```

Puis dans `.env` :
```bash
VOCABULARY_FILE=./data/vocabulary.csv
```

### Option 3: Exporter depuis Google Sheets

1. Ouvrez votre Google Sheet de vocabulaire
2. **Fichier** → **Télécharger** → **CSV**
3. Sauvegardez dans `data/vocabulary.csv`
4. Configurez dans `.env`

Format attendu :
- **Colonne 1** : `chinese` ou `initialText` (mot source)
- **Colonne 2** : `english` ou `translatedText` (traduction)

## 🎯 Format des Questions MCQ

Le bot génère automatiquement des questions comme :

```
What is the correct translation for "[mot chinois]"?
A) option 1
B) option 2 [correcte]
C) option 3
D) option 4

Répondez avec A, B, C ou D
```

## 🧠 Système de Mémoire

### Mémoire par utilisateur
- Chaque utilisateur (chat_id) a sa propre mémoire
- L'historique est conservé entre les sessions
- Maximum 20 messages gardés en mémoire (configurable)

### Stockage
```
data/
  conversations/
    user_123456789.json    # Conversation de l'utilisateur
    backups/
      user_123456789_20231206_143022.json  # Sauvegardes
```

### Effacer l'historique
```
/clear
```

## 🔧 Configuration Avancée

### Modifier le module `telegram_bot.py`

Personnalisez le prompt système dans la méthode `get_system_prompt()` :

```python
def get_system_prompt(self, user_name: str, vocab_list: list) -> str:
    return f"""# Context
You are an AI-powered language tutor...
    
# Personnalisez ici
- Changez le format des questions
- Ajoutez des explications grammaticales
- Modifiez le style de feedback
"""
```

### Changer la taille de la mémoire

Dans `telegram_bot.py` :
```python
# Par défaut : 20 messages
memory_manager = ConversationMemory(max_messages=20)

# Pour plus de contexte :
memory_manager = ConversationMemory(max_messages=50)
```

## 📊 Différences avec le workflow n8n

| Fonctionnalité | Workflow n8n | Bot Python |
|---|---|---|
| Trigger Telegram | ✅ | ✅ |
| Mémoire par chat_id | ✅ | ✅ |
| OpenAI GPT | ✅ | ✅ |
| Google Sheets | ✅ | ⚠️ Export CSV |
| Questions MCQ | ✅ | ✅ |
| Feedback instantané | ✅ | ✅ |
| Interface graphique | ✅ n8n | ❌ Code |
| Personnalisation | ⚠️ Limitée | ✅ Totale |
| Coût | Hébergement n8n | Gratuit (local) |

## 🐛 Dépannage

### "TELEGRAM_BOT_TOKEN non trouvée"
**Solution :** Vérifiez votre fichier `.env` et assurez-vous d'avoir ajouté le token.

### "Bot ne répond pas"
**Solutions :**
1. Vérifiez que le bot est en cours d'exécution
2. Vérifiez votre connexion internet
3. Testez avec `/start`
4. Vérifiez les logs dans le terminal

### "Invalid token"
**Solution :** Obtenez un nouveau token depuis @BotFather

### "Quota exceeded" (OpenAI)
**Solution :** Vérifiez votre crédit OpenAI sur platform.openai.com

### Bot lent à répondre
**Solutions :**
- Utilisez `gpt-4o-mini` au lieu de `gpt-4o`
- Réduisez `MAX_TOKENS` dans `.env`
- Réduisez la taille du vocabulaire

## 💰 Coûts

### OpenAI API
Avec `gpt-4o-mini` :
- **Question MCQ** : ~$0.001 - $0.003
- **100 questions** : ~$0.10 - $0.30
- **Session quotidienne (20 questions)** : ~$0.02 - $0.06

### Telegram Bot
**Gratuit !** Pas de coût d'hébergement si vous exécutez localement.

## 🚀 Déploiement en Production

### Option 1: Serveur local (24/7)

Gardez votre ordinateur allumé ou utilisez un Raspberry Pi :
```powershell
python telegram_bot.py
```

### Option 2: Hébergement Cloud

**PythonAnywhere (Gratuit)** :
1. Créez un compte sur pythonanywhere.com
2. Uploadez votre code
3. Configurez une "Always-On Task"

**Heroku** :
```bash
# Créer Procfile
echo "worker: python telegram_bot.py" > Procfile

# Déployer
heroku create
git push heroku main
heroku ps:scale worker=1
```

**Railway.app** :
1. Connectez votre repo GitHub
2. Railway détecte automatiquement Python
3. Ajoutez vos variables d'environnement
4. Déployez

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "telegram_bot.py"]
```

```bash
docker build -t language-bot .
docker run -d --env-file .env language-bot
```

## 🎓 Exemples d'Utilisation

### Apprentissage intensif
```
Utilisateur: /practice
[20-30 questions consécutives]
Utilisateur: /progress
```

### Session rapide
```
Utilisateur: Salut!
Bot: [Génère une question]
Utilisateur: B
Bot: [Feedback + nouvelle question]
Utilisateur: C
Bot: [Feedback + nouvelle question]
```

### Révision ciblée
Ajoutez seulement les mots difficiles dans `vocabulary.json` et pratiquez.

## 📞 Support

- **Problème technique ?** Consultez la section Dépannage
- **Question sur Telegram ?** Consultez [telegram.org/faq](https://telegram.org/faq)
- **OpenAI API ?** [platform.openai.com/docs](https://platform.openai.com/docs)

## 🔄 Mises à jour futures

- [ ] Support audio pour la prononciation
- [ ] Images pour le vocabulaire visuel
- [ ] Flashcards avec répétition espacée
- [ ] Graphiques de progression
- [ ] Support multi-langues (pas seulement chinois→anglais)
- [ ] Intégration Google Sheets native
- [ ] Mode quiz avec timer
- [ ] Classements entre utilisateurs

## 📝 Notes importantes

1. **Token Telegram** : Gardez-le SECRET. Ne le partagez jamais.
2. **OpenAI API Key** : Idem, gardez-la privée.
3. **Fichier .env** : N'ajoutez JAMAIS ce fichier à Git.
4. **Vocabulaire** : Plus de mots = plus de variété dans les questions.

## 🎉 Comparaison : n8n vs Python

**Avantages du Bot Python :**
- ✅ Gratuit à héberger localement
- ✅ Contrôle total du code
- ✅ Pas de limite de workflows
- ✅ Facile à modifier et étendre
- ✅ Aucune interface graphique nécessaire

**Avantages du workflow n8n :**
- ✅ Interface visuelle
- ✅ Glisser-déposer
- ✅ Intégrations natives (Google Sheets, etc.)
- ✅ Pas de code nécessaire

**Choisissez Python si :**
- Vous êtes à l'aise avec le code
- Vous voulez un contrôle total
- Vous voulez héberger gratuitement
- Vous voulez personnaliser en profondeur

---

**Bon apprentissage avec votre bot Telegram ! 🚀📱**

Pour toute question, référez-vous au `README.md` principal ou consultez le code source.
