# 🚀 Guide de Déploiement du Bot Telegram

## Option 1 : Railway.app (RECOMMANDÉ) ⭐

### Avantages :
- ✅ **$5 de crédit gratuit** par mois
- ✅ Déploiement en **3 clics**
- ✅ Redémarrage automatique
- ✅ Logs en temps réel
- ✅ Variables d'environnement sécurisées

### Étapes :

#### 1. Préparer le projet

Fichiers créés automatiquement :
- ✅ `Procfile` - Commande de démarrage
- ✅ `runtime.txt` - Version Python
- ✅ `requirements.txt` - Déjà présent

#### 2. Initialiser Git (si pas déjà fait)

```powershell
# Dans votre dossier
cd "E:\Professionnal Legend\project_perso\language_learning_agent"

# Initialiser git
git init

# Ajouter les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Language Learning Bot"
```

#### 3. Créer un compte Railway

1. Allez sur [railway.app](https://railway.app)
2. Cliquez **"Start a New Project"**
3. Connectez-vous avec **GitHub**

#### 4. Déployer depuis GitHub

**Option A - Via GitHub (recommandé)** :

```powershell
# Créer un repo GitHub
# Allez sur github.com → New repository

# Ajouter le remote
git remote add origin https://github.com/votre-username/language-bot.git

# Push
git branch -M main
git push -u origin main
```

Sur Railway :
1. **"New Project"** → **"Deploy from GitHub repo"**
2. Sélectionnez votre repo
3. Railway détecte automatiquement Python

**Option B - Via CLI Railway** :

```powershell
# Installer Railway CLI
npm i -g @railway/cli

# Login
railway login

# Créer un projet
railway init

# Déployer
railway up
```

#### 5. Configurer les variables d'environnement

Sur Railway.app :
1. Allez dans votre projet
2. Cliquez sur **"Variables"**
3. Ajoutez :

```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_votre_clé_ici
MODEL_NAME=llama-3.3-70b-versatile
TELEGRAM_BOT_TOKEN=votre_token_telegram
```

4. Cliquez **"Deploy"**

#### 6. Vérifier le déploiement

1. Allez dans **"Deployments"**
2. Cliquez sur le dernier déploiement
3. Regardez les logs :

```
✅ English vocabulary loaded: 50 words
🤖 Using Groq AI (FREE)
✅ Bot is running!
```

### Coût :
- **Gratuit** : $5 de crédit/mois (suffisant pour ce bot)
- Si dépassement : ~$0.01/heure

---

## Option 2 : Heroku (Classique)

### Avantages :
- ✅ Gratuit avec vérification
- ✅ Bien documenté
- ✅ Facile à utiliser

### Étapes :

#### 1. Installer Heroku CLI

```powershell
# Windows
winget install Heroku.HerokuCLI

# Ou téléchargez sur heroku.com/install
```

#### 2. Login et créer l'app

```powershell
# Login
heroku login

# Créer l'app
heroku create language-learning-bot

# Ajouter le buildpack Python
heroku buildpacks:set heroku/python
```

#### 3. Configurer les variables

```powershell
heroku config:set AI_PROVIDER=groq
heroku config:set GROQ_API_KEY=gsk_votre_clé_ici
heroku config:set MODEL_NAME=llama-3.3-70b-versatile
heroku config:set TELEGRAM_BOT_TOKEN=votre_token
```

#### 4. Déployer

```powershell
git push heroku main
```

#### 5. Vérifier

```powershell
heroku logs --tail
```

### Coût :
- **Gratuit** : 550 heures/mois (suffisant)
- Nécessite une carte bancaire pour vérification

---

## Option 3 : PythonAnywhere (Simple)

### Avantages :
- ✅ Interface web simple
- ✅ Pas de Git requis
- ✅ Gratuit permanent

### Étapes :

#### 1. Créer un compte

1. Allez sur [pythonanywhere.com](https://www.pythonanywhere.com)
2. Créez un compte **Beginner** (gratuit)

#### 2. Uploader les fichiers

1. Dans **"Files"**, créez un dossier `language_bot`
2. Uploadez tous vos fichiers Python
3. Uploadez `requirements.txt`

#### 3. Installer les dépendances

Dans **"Consoles"** → **"Bash"** :

```bash
cd language_bot
pip3 install --user -r requirements.txt
```

#### 4. Configurer les variables

Créez un fichier `.env` directement sur PythonAnywhere avec vos clés.

#### 5. Créer une "Always-On Task"

1. Allez dans **"Tasks"**
2. Créez une nouvelle tâche :

```bash
cd ~/language_bot && python3 telegram_bot.py
```

3. Définissez l'heure de démarrage

**Note** : Le plan gratuit n'a pas "Always-On", le bot s'arrêtera après 3 mois d'inactivité.

### Coût :
- **Gratuit** : Limité mais suffisant
- **$5/mois** : Always-On illimité

---

## Option 4 : VPS (Digital Ocean, Linode, etc.)

### Avantages :
- ✅ Contrôle total
- ✅ Performances garanties
- ✅ Peut héberger plusieurs apps

### Étapes rapides :

#### 1. Créer un Droplet

1. [Digital Ocean](https://www.digitalocean.com) → Create Droplet
2. Choisissez **Ubuntu 22.04**
3. Taille : $4/mois (suffisant)

#### 2. Se connecter en SSH

```powershell
ssh root@votre_ip
```

#### 3. Installer les dépendances

```bash
# Mettre à jour
apt update && apt upgrade -y

# Installer Python et pip
apt install python3-pip python3-venv git -y

# Cloner votre repo (ou upload les fichiers)
git clone https://github.com/votre-username/language-bot.git
cd language-bot

# Installer les packages
pip3 install -r requirements.txt
```

#### 4. Configurer les variables

```bash
nano .env
# Ajoutez vos variables
```

#### 5. Lancer avec systemd (auto-restart)

```bash
# Créer un service
nano /etc/systemd/system/telegram-bot.service
```

Contenu :
```ini
[Unit]
Description=Language Learning Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/language-bot
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Démarrer :
```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot

# Vérifier
systemctl status telegram-bot
```

### Coût :
- **$4-6/mois** pour un petit VPS

---

## Option 5 : Docker (Portable)

### Si vous voulez conteneuriser :

<function_calls>
<invoke name="create_file">
<parameter name="content">FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "telegram_bot.py"]
