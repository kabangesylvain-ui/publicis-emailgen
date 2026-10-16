# ✉️ Publicis — Générateur d'emails marketing

> **Outil IA** pour générer des emails marketing **personnalisés** automatiquement (500 emails en 5 minutes au lieu de 3 jours).

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2:3b-black)](https://ollama.ai/)
[![Pixabay](https://img.shields.io/badge/API-Pixabay-2ECC71)](https://pixabay.com/api/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table des matières

- [🎯 Objectif](#-objectif)
- [📊 Résultats](#-résultats)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Stack technique](#️-stack-technique)
- [🚀 Installation](#-installation)
- [🎬 Utilisation](#-utilisation)
- [📁 Structure du projet](#-structure-du-projet)
- [👤 Auteur](#-auteur)

---

## 🎯 Objectif

Automatiser la **création d'emails marketing personnalisés** pour l'équipe marketing de Publicis (client agroalimentaire).

**Problème** : 50 000 emails/mois, 3 jours pour 10 variantes → **trop long et peu personnalisé**.

**Solution** : Un outil IA qui génère **500 emails personnalisés en 5 minutes**.

---

## 📊 Résultats

### Impact business

| Indicateur | Avant | Après |
|---|---|---|
| **Temps de création** | 3 jours | **5 minutes** |
| **Variantes générées** | 10 | **500** |
| **Personnalisation** | Standard | **100 % individuelle** |
| **Images** | Aucune | **Générées automatiquement** |

### Fonctionnalités

- ✅ **Génération de texte** personnalisé (LLM local)
- ✅ **Ton adapté** (tutoiement/vouvoiement selon l'âge)
- ✅ **Offres ciblées** (premium/fidélité/standard)
- ✅ **Images produits** (Pixabay API)
- ✅ **Interface Streamlit** avec 4 thèmes
- ✅ **Export CSV** pour les campagnes

---

## 🏗️ Architecture

```
┌──────────────────┐
│  Profil client   │  ← 500 clients simulés
└────────┬─────────┘
         ↓
┌──────────────────────────────┐
│  Prompt engineering          │  ← Ton + Offre adaptés
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│  LLM (Ollama + llama3.2:3b)  │  ← Génération texte
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│  Image (Pixabay API)         │  ← Image produit
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│  Interface Streamlit         │  ← Affichage + Export
└──────────────────────────────┘
```

---

## 🛠️ Stack technique

| Catégorie | Technologies |
|---|---|
| **Langage** | Python 3.11 |
| **LLM local** | Ollama + `llama3.2:3b` |
| **Images** | Pixabay API |
| **Interface** | Streamlit |
| **Data** | pandas |
| **Sérialisation** | CSV, joblib |

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- [Ollama](https://ollama.ai/download) installé
- Clé API [Pixabay](https://pixabay.com/api/docs/) (gratuite)

### 1. Cloner le repo

```bash
git clone https://github.com/kabangesylvain-ui/publicis-emailgen.git
cd publicis-emailgen
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger le modèle LLM

```bash
ollama pull llama3.2:3b
```

### 5. Configurer Pixabay

Crée un fichier `.env` :

```
PIXABAY_API_KEY=ta_cle_pixabay_ici
```

### 6. Générer le dataset

```bash
python src/generate_dataset.py
```

### 7. Télécharger les images

```bash
python src/image_generator.py
```

---

## 🎬 Utilisation

### Lancer l'interface

```bash
streamlit run app.py --server.port 8502
```

→ Ouvre **http://localhost:8502**

### Étapes

1. **Choisir un thème** (🌸 Purple, 🌊 Ocean, 🌅 Sunset, 🌲 Forest)
2. **Sélectionner un client** dans la liste
3. **Choisir un produit**
4. **Cliquer sur "🚀 Générer l'email"**
5. **Voir le résultat** : sujet + corps + image
6. **Télécharger en CSV**

---

## 📁 Structure du projet

```
publicis-emailgen/
│
├── 📁 src/                          # Code source
│   ├── generate_dataset.py          # Création du dataset
│   ├── prompts.py                   # Prompts et fonctions
│   ├── email_generator.py           # Générateur d'emails
│   └── image_generator.py           # Générateur d'images
│
├── 📁 data/                         # Données
│   ├── clients.csv                  # 500 clients
│   └── historique_campagnes.csv     # 50 campagnes
│
├── 📁 output/                       # Résultats
│   ├── emails_generes.csv
│   └── images/                      # Images produits
│
├── 📁 assets/                       # Ressources
│   └── images/                      # Captures README
│
├── 📄 app.py                        # Interface Streamlit
├── 📄 requirements.txt              # Dépendances
├── 📄 .env                          # Clés API (non versionné)
├── 📄 .gitignore
├── 📄 README.md                     # Ce fichier
└── 📄 RAPPORT.md                    # Analyse détaillée
```

---

## 🎓 Compétences mobilisées

- ✅ **IA Générative** : génération de texte avec LLM
- ✅ **Prompt engineering** : ton, offre, contexte
- ✅ **API REST** : Pixabay pour les images
- ✅ **Streamlit** : interface web interactive
- ✅ **Gestion de projet** : Git, structure modulaire

---

## 📄 License

MIT License.

---

## 👤 Auteur

**Sylvain Kabange**

🎓 M2 Data Science — Horizon University  
📧 kabange.sylvain@horizon-university.tn  
🔗 [GitHub @kabangesylvain-ui](https://github.com/kabangesylvain-ui)

---

⭐ **Si ce projet vous a plu, n'hésitez pas à lui donner une étoile !**