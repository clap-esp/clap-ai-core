# CLAP AI CORE

Bienvenue dans le projet `clap-ai-core` ! Ce dépôt contient le noyau d'intelligence artificielle pour Clap, un logiciel innovant de dérushage intelligent.

### Structure du projet

```
clap-ai-core/
│
├── data/
│   └── ...  # Contient les datasets utilisés pour l'entraînement ou l'évaluation des modèles
├── models/
│   └── ...  # Contient les modèles fine tuned, disponibles pour l'api
├── main.ipynb  # Notebook Jupyter pour exécuter et tester le code
└── requirements.txt  # Liste des lib nécessaires pour exécuter le projet
```

## Prérequis

- Python ≥ 3.11
- install git lfs\* on your machine -> https://git-lfs.com/

> \* Filtre les \*.h5 pour les stocker sur un server lsf

## Setup

...🚧
Kernel : choose Python 3.x

```bash
# lauch Virtual Env
cd /back/API
python -m venv env
source env/Scripts/activate

# Install Dependencies
pip install -r requirements.txt

# Start Project
python app.py
```

...🚧

### Contribuer

-> Guide de [contribution](CONTRIBUTING.md)

## Configuration des secrets

Dupliquez le fichier `env.example` et renommez la copie en `.env`  
Ce fichier contient les secrets (ex clé d'API). Il ne doit jamais être push sur le repo.

## Fonctionnalités

🚧 en construction ...

1. Module Speech to Text
2. Module NLP (Natural Language Processing)

## Architerture

🚧
