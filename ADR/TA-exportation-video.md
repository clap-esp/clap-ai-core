# Exportation vidéo

## Contexte & Besoin

Bientôt, le bouton "Dérush" lancera le script app_derush.py qui retournera un JSON avec des timestamps des coupes suggérées. Ces données servent à alimenter la frise temporelle de l'UI. Il est nécessaire d'ajouter l'étape d'exportation de la version final de la vidéo dérushée après validation des coupes par l'utilisateur.

**Objectif** : Développer un script d'exportation

#### Le script utilise

Les coupes sélectionnées par l'utilisateur dans le fichier tmp/user_cuts.json

#### Le script prend en argument

- Le format d'export choisi (MP4, MOV, etc.)
- La taille de la vidéo (ex. : 16:9, 4:3, etc.)
- Le path de la vidéo en input
- Le path du dossier de destination pour l'export

#### Notes

Le choix est de laisser ffmpeg gérer le codec vidéo. Il qui prend un codec par défaut en fonction du format d'export choisi.
