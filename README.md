# 🤖 Agent IA d'Apprentissage de Langue

Un agent intelligent en Python pour apprendre une langue étrangère de manière interactive, avec conversations, exercices, corrections et suivi de progrès.

## ✨ Fonctionnalités

### 💬 Conversations Interactives
- Dialogues naturels avec l'IA dans la langue cible
- Choix de sujets variés (voyage, nourriture, travail, etc.)
- Adaptation au niveau de l'apprenant (A1 à C1)
- Corrections en temps réel

### 📝 Exercices Variés
1. **Vocabulaire** - Apprentissage de nouveaux mots et expressions
2. **Grammaire** - Points grammaticaux adaptés au niveau
3. **Conjugaison** - Pratique des temps et verbes
4. **Compréhension** - Textes avec questions
5. **Traduction** - Exercices bidirectionnels

### 🎯 Corrections et Feedback
- Analyse détaillée des erreurs
- Explications grammaticales claires
- Suggestions d'amélioration
- Encouragements personnalisés

### 📊 Suivi de Progrès
- Statistiques d'apprentissage
- Historique des sessions
- Temps de pratique
- Mots appris

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Une clé API OpenAI

### Étapes d'installation

1. **Cloner ou télécharger le projet**
```powershell
cd "e:\Professionnal Legend\project_perso\language_learning_agent"
```

2. **Créer un environnement virtuel (recommandé)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Installer les dépendances**
```powershell
pip install -r requirements.txt
```

4. **Configurer la clé API**

Créez un fichier `.env` à la racine du projet:
```powershell
Copy-Item .env.example .env
```

Éditez le fichier `.env` et ajoutez votre clé API OpenAI:
```
OPENAI_API_KEY=sk-votre-clé-api-ici
```

> 🔑 **Obtenir une clé API OpenAI:**
> 1. Créez un compte sur [OpenAI](https://platform.openai.com/)
> 2. Allez dans [API Keys](https://platform.openai.com/api-keys)
> 3. Cliquez sur "Create new secret key"
> 4. Copiez la clé dans votre fichier `.env`

## 🎮 Utilisation

### Lancer l'agent

```powershell
python main.py
```

### Menu principal

```
1. 💬 Conversation libre    - Discutez naturellement sur un sujet
2. 📝 Exercices ciblés      - Pratiquez vocabulaire, grammaire, etc.
3. 🎯 Corrections           - Obtenez des corrections détaillées
4. 📊 Voir mes progrès      - Consultez vos statistiques
5. ⚙️  Changer de niveau    - Ajustez la difficulté (A1-C1)
6. 🚪 Quitter
```

### Exemples d'utilisation

#### Conversation libre
```
🎯 Votre choix: 1
💬 Mode Conversation
Choisissez un sujet: voyage et tourisme

🤖 Assistant: Hello! I love talking about travel. Have you visited any interesting places recently?
Vous: Yes, I went to Paris last month
🤖 Assistant: That's wonderful! What did you enjoy most about Paris?
...
```

#### Exercice de vocabulaire
```
🎯 Votre choix: 2
Type d'exercice: 1

📚 Exercice de Vocabulaire
Thème: La maison

1. living room - salon
2. bedroom - chambre
3. kitchen - cuisine
...
```

## 📁 Structure du Projet

```
language_learning_agent/
├── main.py                 # Point d'entrée principal
├── config.py              # Configuration et prompts système
├── requirements.txt       # Dépendances Python
├── .env                   # Configuration (à créer)
├── .env.example          # Exemple de configuration
├── README.md             # Documentation
│
├── modules/              # Modules de l'agent
│   ├── __init__.py
│   ├── conversation.py   # Gestion des conversations
│   ├── exercises.py      # Génération d'exercices
│   └── progress_tracker.py # Suivi des progrès
│
└── data/                 # Données générées (créé automatiquement)
    ├── progress/         # Statistiques utilisateur
    └── conversations/    # Historique des conversations
```

## ⚙️ Configuration Avancée

### Paramètres disponibles dans `.env`

```bash
# Modèle IA (plus puissant = meilleur mais plus cher)
MODEL_NAME=gpt-4o-mini       # Économique
# MODEL_NAME=gpt-4o          # Plus puissant
# MODEL_NAME=gpt-4-turbo     # Le plus puissant

# Créativité des réponses (0.0 = stricte, 2.0 = très créative)
TEMPERATURE=0.7

# Longueur maximale des réponses
MAX_TOKENS=1000

# Niveau par défaut
DEFAULT_LEVEL=B1
```

### Niveaux disponibles

- **A1** - Débutant (200-500 mots)
- **A2** - Élémentaire (500-1000 mots)
- **B1** - Intermédiaire (1000-2000 mots) ⭐ Par défaut
- **B2** - Intermédiaire avancé (2000-4000 mots)
- **C1** - Avancé (4000-8000 mots)

### Langues supportées

- 🇬🇧 Anglais
- 🇪🇸 Espagnol
- 🇩🇪 Allemand
- 🇮🇹 Italien
- 🇵🇹 Portugais
- 🇯🇵 Japonais
- 🇨🇳 Chinois

## 💡 Conseils d'utilisation

### Pour progresser rapidement
1. **Pratiquez régulièrement** - 15-30 minutes par jour
2. **Variez les activités** - Alternez conversations et exercices
3. **N'ayez pas peur des erreurs** - Elles sont essentielles pour apprendre
4. **Demandez des corrections** - Utilisez le feedback pour vous améliorer
5. **Suivez vos progrès** - Consultez vos statistiques régulièrement

### Commandes utiles en conversation
- Tapez `menu` pour revenir au menu
- Posez des questions avec `?` pour obtenir de l'aide
- Demandez des explications en français quand nécessaire

## 🔧 Dépannage

### Problème: "OPENAI_API_KEY non trouvée"
**Solution:** Vérifiez que le fichier `.env` existe et contient votre clé API.

### Problème: "Module not found"
**Solution:** Installez les dépendances:
```powershell
pip install -r requirements.txt
```

### Problème: Erreur API OpenAI
**Solutions:**
- Vérifiez votre connexion internet
- Vérifiez que votre clé API est valide
- Vérifiez votre crédit OpenAI sur [platform.openai.com](https://platform.openai.com/usage)

### Problème: L'agent ne répond pas en français
**Solution:** L'agent répond dans la langue cible. Pour des explications en français, demandez explicitement ou utilisez la fonction de correction.

## 💰 Coûts

L'agent utilise l'API OpenAI qui est payante. Coûts approximatifs avec `gpt-4o-mini`:

- **Conversation (30 min):** ~$0.01 - $0.05
- **Exercice complet:** ~$0.005 - $0.02
- **Correction de texte:** ~$0.002 - $0.01

> 💡 **Astuce:** Commencez avec `gpt-4o-mini` pour économiser. Passez à `gpt-4o` pour des réponses plus naturelles.

## 🤝 Contribution

N'hésitez pas à améliorer ce projet! Suggestions d'améliorations:

- [ ] Interface graphique (Streamlit/Gradio)
- [ ] Reconnaissance vocale
- [ ] Synthèse vocale pour la prononciation
- [ ] Flashcards avec répétition espacée
- [ ] Mode hors ligne avec modèles locaux
- [ ] Application mobile
- [ ] Support d'images pour le vocabulaire

## 📝 Licence

Ce projet est libre d'utilisation pour un usage personnel et éducatif.

## 🙋 Support

Pour toute question ou problème:
1. Consultez d'abord ce README
2. Vérifiez la section Dépannage
3. Consultez la [documentation OpenAI](https://platform.openai.com/docs)

## 🎓 Ressources Complémentaires

Pour compléter votre apprentissage:
- [Duolingo](https://www.duolingo.com/) - Vocabulaire et grammaire de base
- [Anki](https://apps.ankiweb.net/) - Flashcards avec répétition espacée
- [Language Exchange](https://www.tandem.net/) - Conversation avec des natifs
- [YouTube](https://www.youtube.com/) - Immersion dans la langue cible

---

**Bon apprentissage! 🚀**
