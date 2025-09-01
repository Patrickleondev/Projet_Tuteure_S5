# Documentation du Modèle de Prédiction Football Insight Predictor

## Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du modèle](#architecture-du-modèle)
3. [Sources de données](#sources-de-données)
4. [Features et prétraitement](#features-et-prétraitement)
5. [Modèles de prédiction](#modèles-de-prédiction)
6. [Processus de prédiction](#processus-de-prédiction)
7. [Évaluation et performances](#évaluation-et-performances)

## Vue d'ensemble

Le Football Insight Predictor (FIP) est un système de prédiction de matchs de football qui utilise une approche hybride combinant plusieurs modèles de machine learning. Le système est conçu pour prédire les résultats des matchs de football dans différentes compétitions, notamment :
- UEFA Champions League
- Principales ligues européennes (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)
- Compétitions internationales (Coupe du Monde, Euro, Copa América)

## Architecture du modèle

Le système utilise une architecture à trois niveaux de modèles :

1. **Modèle de régression linéaire** (`RegressionPredictionService`)
   - Prédit le nombre de buts pour chaque équipe
   - Utilise des statistiques de base et des différentiels entre équipes

2. **Modèle GradientBoosting** (`FootballMatchPredictor`)
   - Prédit les probabilités de victoire/nul/défaite
   - Utilise un ensemble plus large de features

3. **Modèle Hybride** (`HybridModel`)
   - Combine les prédictions des deux modèles précédents
   - Utilise TensorFlow pour l'apprentissage profond

## Sources de données

Les données proviennent de plusieurs sources stockées dans le répertoire `FIP_DB` :

1. **equipes_data.csv**
   - Statistiques générales des équipes
   - Performances à domicile et à l'extérieur
   - Nombre de matchs joués, victoires, etc.

2. **matchs_data.csv**
   - Historique des confrontations
   - Résultats des matchs précédents
   - Scores et statistiques de match

3. **discipline_data.csv**
   - Cartons jaunes et rouges
   - Fautes commises et subies

4. **jeu_data.csv**
   - Statistiques de possession
   - Passes réussies
   - Tirs et tirs cadrés

5. **coups_de_pied_arretes_data.csv**
   - Penalties
   - Coups francs
   - Corners

## Features et prétraitement

### Features principales utilisées par le modèle GradientBoosting :

```python
feature_columns = [
    # Statistiques domicile
    'buts_marques_domicile_home',
    'buts_encaisses_domicile_home',
    'matchs_joues_home',
    'victoires_domicile_home',
    'points_par_match_home',
    
    # Statistiques extérieur
    'buts_marques_exterieur_away',
    'buts_encaisses_exterieur_away',
    'matchs_joues_away',
    'victoires_exterieur_away',
    'points_par_match_away',
    
    # Forme récente
    'forme_victoires_domicile',
    'forme_nuls_domicile',
    'forme_defaites_domicile',
    'forme_victoires_exterieur',
    'forme_nuls_exterieur',
    'forme_defaites_exterieur',
    
    # Confrontations directes
    'h2h_victoires_domicile',
    'h2h_victoires_exterieur',
    'h2h_nuls',
    'h2h_buts_domicile',
    'h2h_buts_exterieur'
]
```

### Prétraitement des données :

1. **Standardisation**
   - Utilisation de `StandardScaler` pour normaliser les features
   - Mise à l'échelle des valeurs numériques

2. **Gestion des valeurs manquantes**
   - Remplacement par la moyenne pour les features numériques
   - Utilisation de valeurs par défaut pour les statistiques manquantes

3. **Feature engineering**
   - Calcul des différentiels entre équipes
   - Agrégation des statistiques récentes
   - Calcul des moyennes glissantes

## Modèles de prédiction

### 1. Modèle de régression linéaire
- **Objectif** : Prédire le nombre de buts
- **Features** : 
  - Différentiel de tirs
  - Différentiel de possession
  - Différentiel de passes
  - Statistiques de cartons
- **Sortie** : Nombre de buts prédits pour chaque équipe

### 2. GradientBoosting Classifier
- **Paramètres** :
  ```python
  GradientBoostingClassifier(
      n_estimators=100,
      learning_rate=0.1,
      max_depth=5,
      random_state=42
  )
  ```
- **Features** : 21 features principales (listées ci-dessus)
- **Sortie** : Probabilités pour victoire/nul/défaite

### 3. Modèle Hybride (TensorFlow)
- **Architecture** :
  - Couche d'entrée : 128 neurones (relu)
  - Couche cachée 1 : 64 neurones (relu)
  - Couche cachée 2 : 32 neurones (relu)
  - Couche de sortie : 3 neurones (softmax)
- **Optimisation** : Adam
- **Fonction de perte** : Categorical crossentropy

## Processus de prédiction

1. **Collecte des données**
   - Récupération des statistiques des équipes
   - Calcul des features récentes
   - Préparation des données d'entrée

2. **Prédiction multi-modèle**
   - Prédiction du nombre de buts (régression)
   - Prédiction des probabilités (GradientBoosting)
   - Combinaison des prédictions (modèle hybride)

3. **Post-traitement**
   - Ajustement des probabilités
   - Calcul des statistiques additionnelles
   - Formatage des résultats

## Évaluation et performances

### Métriques d'évaluation
- Accuracy pour la classification des résultats
- MAE/MSE pour la prédiction des buts
- Log-loss pour les probabilités

### Validation
- Validation croisée sur les données historiques
- Ensemble de test séparé pour l'évaluation finale
- Monitoring des performances en production

### Limites actuelles
- Dépendance aux données historiques récentes
- Sensibilité aux changements de forme des équipes
- Difficulté à prédire les événements rares

## Utilisation en production

Le système est déployé comme un service web Flask qui :
1. Charge les modèles au démarrage
2. Maintient les données en mémoire pour des prédictions rapides
3. Met à jour régulièrement les statistiques des équipes
4. Fournit des API REST pour les prédictions

Pour utiliser le système :
```python
prediction_service = PredictionService()
resultat = prediction_service.predict_match(
    equipe_domicile="Manchester City",
    equipe_exterieur="Real Madrid",
    type_competition="clubs",
    competition="cl"
)
``` 