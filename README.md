# CLAP AI CORE

Bienvenue dans le projet `clap-ai-core` ! Ce dépôt contient le noyau d'intelligence artificielle pour Clap, un logiciel innovant de dérushage intelligent.

### Structure du projet

```
clap-ai-core/
│
├── API/
│   └── ...  # Application + methods
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

```bash
# ativer le virtual env à la racine du projet
python -m venv env
source env/Scripts/activate

# installer les lib
pip install -r requirements.txt

# deactivate env
deactivate

# API scripts
cd API
# first, launch the transcription
python app_transcription.py
# launch the derush process
python app_derush.py
# launch the traduction
python app_translate.py

# for dev, use test_dev_<scripts>
# for test the functions one by one and debug log
python test_dev_transcription.py
python test_dev_derush.py

```

**Pour executer un fichier \*.ipynb**  
-> choisir le Kernel env(Python 3.11.x) -> env/Scripts/python.exe

### Contribuer

-> Guide de [contribution](CONTRIBUTING.md)

## Configuration des secrets

Dupliquez le fichier `env.example` et renommez la copie en `.env`  
Ce fichier contient les secrets (ex clé d'API). Il ne doit jamais être push sur le repo.

## Fonctionnalités

1. Speech to Text
2. NER
🚧 en construction ...

## Architerture

Le script app.py génère un fichier final_format.json disponible pour l'UI

## Dataset

-> Documentation about [datasets](./data/README.md)
