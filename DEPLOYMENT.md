# 🚀 Guide de Déploiement - Bot Telegram d'Apprentissage d'Anglais

## 📋 Fichiers de déploiement créés

- ✅ `Procfile` - Pour Railway/Heroku
- ✅ `runtime.txt` - Version Python
- ✅ `Dockerfile` - Pour Docker
- ✅ `docker-compose.yml` - Orchestration Docker

## 🎯 Quelle option choisir ?

| Option | Difficulté | Coût | Recommandé pour |
|--------|-----------|------|-----------------|
| **Railway** | ⭐ Facile | Gratuit ($5/mois) | Débutants |
| **Heroku** | ⭐⭐ Moyen | Gratuit | Développeurs |
| **PythonAnywhere** | ⭐ Facile | Gratuit | Simple |
| **VPS** | ⭐⭐⭐ Difficile | $4-6/mois | Contrôle total |
| **Docker** | ⭐⭐⭐ Difficile | Varie | Portable |

---

## 1️⃣ Railway.app (RECOMMANDÉ)

### ✅ Avantages :
- $5 de crédit gratuit/mois
- Déploiement en 3 clics
- Auto-redémarrage
- Logs en temps réel

### 📝 Étapes :

#### A. Préparer Git

```powershell
cd "E:\Professionnal Legend\project_perso\language_learning_agent"

git init
git add .
git commit -m "Initial commit"
```

#### B. Créer un repo GitHub

1. Allez sur [github.com](https://github.com) → **New repository**
2. Nom: `language-learning-bot`
3. **Ne cochez rien** (pas de README, .gitignore, etc.)
4. Cliquez **"Create repository"**

#### C. Push vers GitHub

```powershell
git remote add origin https://github.com/VOTRE-USERNAME/language-learning-bot.git
git branch -M main
git push -u origin main
```

#### D. Déployer sur Railway

1. Allez sur [railway.app](https://railway.app)
2. **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Connectez GitHub et sélectionnez votre repo
4. Railway détecte automatiquement Python ✅

#### E. Configurer les variables

Dans Railway → **Variables** → Ajoutez :

```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_votre_clé_ici
MODEL_NAME=llama-3.3-70b-versatile
TELEGRAM_BOT_TOKEN=votre_token_telegram
```

#### F. Vérifier le déploiement

**Deployments** → Voir les logs :
```
✅ English vocabulary loaded: 50 words
🤖 Using Groq AI (FREE)
✅ Bot is running!
```

### 💰 Coût : **GRATUIT** ($5 crédit/mois = suffisant)

---

## 2️⃣ Heroku (Alternative gratuite)

### 📝 Étapes :

#### A. Installer Heroku CLI

```powershell
winget install Heroku.HerokuCLI
```

#### B. Login et créer

```powershell
heroku login
heroku create language-learning-bot
```

#### C. Configurer les variables

```powershell
heroku config:set AI_PROVIDER=groq
heroku config:set GROQ_API_KEY=gsk_votre_clé
heroku config:set MODEL_NAME=llama-3.3-70b-versatile
heroku config:set TELEGRAM_BOT_TOKEN=votre_token
```

#### D. Déployer

```powershell
git push heroku main
```

#### E. Vérifier

```powershell
heroku logs --tail
```

### 💰 Coût : **GRATUIT** (550h/mois avec vérification CB)

---

## 3️⃣ PythonAnywhere (Super simple)

### 📝 Étapes :

#### A. Créer un compte

1. [pythonanywhere.com](https://www.pythonanywhere.com) → **Sign up**
2. Choisissez **Beginner** (gratuit)

#### B. Uploader les fichiers

1. **Files** → Créez `language_bot/`
2. Uploadez tous vos fichiers `.py`, `requirements.txt`, etc.
3. Créez `.env` avec vos clés

#### C. Installer les dépendances

**Consoles** → **Bash** :

```bash
cd ~/language_bot
pip3 install --user -r requirements.txt
```

#### D. Lancer le bot

**Tasks** → **Create a new scheduled task** :

```bash
cd ~/language_bot && python3 telegram_bot.py
```

**Note :** Gratuit mais pas "always-on". Pour always-on: $5/mois

### 💰 Coût : **GRATUIT** (limité) ou **$5/mois** (always-on)

---

## 4️⃣ Docker (Si vous connaissez Docker)

### 📝 Build et Run :

```powershell
# Build l'image
docker build -t language-bot .

# Run le container
docker run -d --env-file .env --name language-bot language-bot

# Ou avec docker-compose
docker-compose up -d
```

### Voir les logs :

```powershell
docker logs -f language-bot
```

---

## 5️⃣ VPS (Digital Ocean, Linode, etc.)

### Pour les avancés qui veulent un contrôle total

#### A. Créer un Droplet

1. [digitalocean.com](https://www.digitalocean.com) → **Create Droplet**
2. Ubuntu 22.04, $4/mois

#### B. Se connecter

```powershell
ssh root@votre_ip
```

#### C. Installer

```bash
apt update && apt upgrade -y
apt install python3-pip git -y

git clone https://github.com/votre-username/language-bot.git
cd language-bot

pip3 install -r requirements.txt
```

#### D. Créer un service systemd

```bash
nano /etc/systemd/system/telegram-bot.service
```

Contenu :
```ini
[Unit]
Description=Language Learning Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/language-bot
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Démarrer :
```bash
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

### 💰 Coût : **$4-6/mois**

---

## ✅ Ma recommandation

### Pour vous : **Railway.app**

**Pourquoi ?**
1. ✅ Le plus simple (3 clics)
2. ✅ Gratuit ($5 crédit = largement suffisant)
3. ✅ Auto-redémarrage si crash
4. ✅ Logs en temps réel
5. ✅ Pas besoin de serveur

### Prêt à déployer sur Railway ?

```powershell
# 1. Init Git
git init
git add .
git commit -m "Initial commit"

# 2. Push sur GitHub (créez d'abord le repo sur github.com)
git remote add origin https://github.com/VOTRE-USERNAME/language-bot.git
git push -u origin main

# 3. Allez sur railway.app et déployez depuis GitHub
# 4. Ajoutez vos variables d'environnement
# 5. C'est tout ! ✅
```

Besoin d'aide pour déployer ?
