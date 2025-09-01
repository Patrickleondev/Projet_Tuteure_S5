# Football Insight Predictor

## Description

Football Insight Predictor est une application web de prédiction de matchs de football utilisant l'intelligence artificielle. L'application analyse les statistiques historiques des équipes pour prédire les résultats de matchs, les scores et diverses statistiques détaillées.

## Fonctionnalités

- **Prédiction de matchs** : Prédiction des scores et résultats de matchs
- **Statistiques détaillées** : Affichage organisé des statistiques par catégories :
  - Discipline (cartons jaunes, rouges, fautes)
  - Coups de pied arrêtés (corners, coups francs)
  - Statistiques générales (possession, tirs, passes)
- **Support multi-ligues** : Champions League, Ligue 1, Premier League, La Liga, Serie A
- **Interface moderne** : Design responsive avec Tailwind CSS

## Technologies utilisées

- **Backend** : Pylthon, Flask
- **Frontend** : JavaScript, HTML5, CSS3, Tailwind CSS
- **IA/ML** : Modèles de prédiction hybrides
- **Base de données** : CSV pour les données historiques

## Structure du projet

```
Football_Insight_Predictor/
├── project/
│   ├── src/
│   │   └── js/
│   │       ├── components/
│   │       │   ├── TeamSelector.js
│   │       │   ├── DetailedMatchStats.js
│   │       │   └── MatchStats.js
│   │       ├── services/
│   │       └── config/
│   ├── templates/
│   │   └── predictions.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── data/
│   ├── models/
│   └── services/
├── DATASETS/
└── FIP_DB/
```

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/Patrickleondev/Projet_Tuteure_S5.git
cd Projet_Tuteure_S5
```

2. Installer les dépendances Python :
```bash
cd Football_Insight_Predictor/project
pip install -r requirements.txt
```

3. Lancer l'application :
```bash
python app.py
```

## Utilisation

1. Ouvrir l'application dans un navigateur
2. Sélectionner une compétition
3. Choisir deux équipes
4. Cliquer sur "Prédire le résultat"
5. Consulter les prédictions et statistiques détaillées

## Auteurs

- Patrick Leon

## Licence

MIT License

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request. 
