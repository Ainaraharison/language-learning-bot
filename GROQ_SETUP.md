# 🆓 Configuration Groq (100% GRATUIT)

## 🎉 Pourquoi Groq ?

- ✅ **100% GRATUIT** - 14,400 requêtes par jour
- ⚡ **Ultra rapide** - 10x plus rapide qu'OpenAI
- 🚀 **Aucune carte bancaire** requise
- 🧠 **Modèles puissants** - Llama 3.3 70B, Mixtral, etc.

## 📝 Étapes d'installation

### 1️⃣ Obtenir une clé API Groq (2 minutes)

1. Allez sur [console.groq.com](https://console.groq.com)
2. Cliquez sur **"Sign Up"** ou **"Sign In"**
3. Connectez-vous avec Google, GitHub ou Email
4. Allez dans **"API Keys"** dans le menu
5. Cliquez sur **"Create API Key"**
6. Donnez un nom (ex: "Language Learning Bot")
7. **Copiez la clé** (commence par `gsk_...`)

### 2️⃣ Configurer le bot

```powershell
# Copiez le fichier d'exemple
Copy-Item .env.example .env

# Éditez le fichier .env
notepad .env
```

### 3️⃣ Remplir .env

```bash
# Provider (ne changez pas)
AI_PROVIDER=groq

# Votre clé Groq (OBLIGATOIRE)
GROQ_API_KEY=gsk_votre_clé_ici

# Modèle recommandé
MODEL_NAME=llama-3.3-70b-versatile

# Votre token Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4️⃣ Lancer le bot

```powershell
python telegram_bot.py
```

Vous devriez voir :
```
🤖 Using Groq AI (FREE) - Model: llama-3.3-70b-versatile
📱 Model: llama-3.3-70b-versatile
📚 Vocabulary loaded: 40 words
✅ Bot is running! Press Ctrl+C to stop.
```

## 🎯 Modèles Groq disponibles

### Recommandé pour l'apprentissage :

```bash
# Meilleur équilibre qualité/vitesse (RECOMMANDÉ)
MODEL_NAME=llama-3.3-70b-versatile

# Très rapide, bonne qualité
MODEL_NAME=llama3-70b-8192

# Excellent pour le raisonnement
MODEL_NAME=mixtral-8x7b-32768

# Ultra rapide (moins précis)
MODEL_NAME=llama3-8b-8192
```

### Limites gratuites :

| Modèle | Requêtes/jour | Tokens/minute |
|--------|---------------|---------------|
| llama-3.3-70b | 14,400 | 6,000 |
| mixtral-8x7b | 14,400 | 5,000 |
| llama3-70b | 14,400 | 6,000 |

**C'est largement suffisant pour apprendre !**

## 🔄 Basculer entre Groq et OpenAI

### Utiliser Groq (gratuit) :
```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk_votre_clé_ici
MODEL_NAME=llama-3.3-70b-versatile
```

### Utiliser OpenAI (payant) :
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-votre_clé_ici
MODEL_NAME=gpt-4o-mini
```

## ✅ Vérifier que ça fonctionne

### Test rapide :

```powershell
# Lancer le bot
python telegram_bot.py

# Vous devriez voir :
# 🤖 Using Groq AI (FREE) - Model: llama-3.3-70b-versatile
```

### Sur Telegram :

```
Vous: /start
Bot: 👋 Hello! Welcome to your AI Language Tutor!

Vous: /practice
Bot: What is the correct translation for "仓库"?
     A) transportation
     B) warehouse
     C) contract
     D) bid
```

## 🐛 Dépannage

### "GROQ_API_KEY non trouvée"
**Solution :** Vérifiez votre fichier `.env`
```bash
# Assurez-vous d'avoir :
AI_PROVIDER=groq
GROQ_API_KEY=gsk_...
```

### "Invalid API Key"
**Solutions :**
1. Vérifiez que vous avez copié toute la clé
2. Créez une nouvelle clé sur console.groq.com
3. Vérifiez qu'il n'y a pas d'espaces avant/après

### "Rate limit exceeded"
**Solution :** Vous avez atteint 14,400 requêtes/jour
- Attendez 24h pour le reset
- Ou créez un nouveau compte Groq (gratuit)

### Bot lent
**Solution :** Groq est normalement très rapide
- Vérifiez votre connexion internet
- Essayez `llama3-8b-8192` (plus rapide)

## 💰 Comparaison des coûts

### Groq (ce que vous utilisez maintenant)
- **Prix :** 🆓 GRATUIT
- **Limite :** 14,400 requêtes/jour
- **Coût pour 1000 questions :** $0.00

### OpenAI GPT-4o-mini
- **Prix :** ~$0.15 / 1M input tokens
- **Coût pour 1000 questions :** ~$0.30-0.50
- **Carte bancaire :** Obligatoire

### OpenAI GPT-4o
- **Prix :** ~$2.50 / 1M input tokens
- **Coût pour 1000 questions :** ~$5-8
- **Carte bancaire :** Obligatoire

## 📊 Performance comparée

| Critère | Groq | OpenAI |
|---------|------|--------|
| Vitesse | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ |
| Qualité | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Prix | 🆓 Gratuit | 💰 Payant |
| Setup | ✅ Facile | ⚠️ Carte requise |
| Pour apprendre | ✅ Parfait | ✅ Excellent |

**Verdict : Groq est parfait pour apprendre !**

## 🎓 Conseils d'utilisation

### Optimiser vos requêtes :
```bash
# Modèle rapide pour beaucoup de questions
MODEL_NAME=llama3-8b-8192

# Modèle intelligent pour qualité maximale
MODEL_NAME=llama-3.3-70b-versatile
```

### Économiser des requêtes :
- Utilisez `/clear` pour réinitialiser la mémoire
- Pratiquez par sessions courtes (10-20 questions)
- Le bot utilise déjà une mémoire optimisée (20 messages max)

## 🚀 Aller plus loin

### Support multi-providers :
Le bot supporte maintenant :
- ✅ Groq (gratuit)
- ✅ OpenAI (payant)
- 🔜 Ollama (local, à venir)
- 🔜 Anthropic Claude (à venir)

### Ajouter d'autres providers :
Modifiez `telegram_bot.py` pour ajouter d'autres IA !

## 🆘 Support

**Problème avec Groq ?**
- Documentation : [console.groq.com/docs](https://console.groq.com/docs)
- Status : [status.groq.com](https://status.groq.com)
- Créer une nouvelle clé : [console.groq.com/keys](https://console.groq.com/keys)

**Tout fonctionne ?**
Commencez à pratiquer avec `/practice` sur Telegram ! 🎉

---

**Résumé :**
1. Obtenez une clé sur [console.groq.com/keys](https://console.groq.com/keys)
2. Ajoutez-la dans `.env`
3. Lancez `python telegram_bot.py`
4. Pratiquez gratuitement ! 🚀
