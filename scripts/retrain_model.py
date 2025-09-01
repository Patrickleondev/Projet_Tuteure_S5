import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import sys

# Ajout du chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def load_data():
    """Chargement et préparation des données"""
    data_dir = project_root.parent / 'FIP_DB'
    
    # Chargement des différents fichiers
    print("\nChargement des fichiers CSV...")
    matches_df = pd.read_csv(data_dir / 'matchs_data.csv')
    teams_df = pd.read_csv(data_dir / 'equipes_data.csv')
    discipline_df = pd.read_csv(data_dir / 'discipline_data.csv')
    jeu_df = pd.read_csv(data_dir / 'jeu_data.csv')
    cpa_df = pd.read_csv(data_dir / 'coups_de_pied_arretes_data.csv')
    
    print(f"Nombre de matchs : {len(matches_df)}")
    print(f"Nombre d'équipes : {len(teams_df)}")
    print(f"Nombre d'équipes (discipline) : {len(discipline_df)}")
    print(f"Nombre d'équipes (jeu) : {len(jeu_df)}")
    print(f"Nombre d'équipes (CPA) : {len(cpa_df)}")
    
    # Standardisation des codes de compétition
    competition_mapping = {
        'Ligue 1': 'fr.1',
        'Premier League': 'en.1',
        'La Liga': 'es.1',
        'Champions League': 'cl',
        'World Cup': 'int',
        'Euro': 'int',
        'Copa America': 'int'
    }
    matches_df['competition'] = matches_df['competition'].map(competition_mapping)
    
    # Fusion des données de base
    print("\nFusion des données de base...")
    data = matches_df.merge(
        teams_df,
        left_on=['equipe_domicile', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('', '_home')
    )
    print(f"Après fusion équipes domicile : {len(data)}")
    
    data = data.merge(
        teams_df,
        left_on=['equipe_exterieur', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('_home', '_away')
    )
    print(f"Après fusion équipes extérieur : {len(data)}")
    
    # Suppression des colonnes redondantes
    columns_to_drop = [col for col in data.columns if col.endswith(('_home', '_away')) and col.startswith('equipe')]
    data = data.drop(columns_to_drop, axis=1)
    
    # Fusion avec les données de discipline
    print("\nFusion des données de discipline...")
    data = data.merge(
        discipline_df,
        left_on=['equipe_domicile', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('', '_discipline_home')
    )
    print(f"Après fusion discipline domicile : {len(data)}")
    
    data = data.merge(
        discipline_df,
        left_on=['equipe_exterieur', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('_discipline_home', '_discipline_away')
    )
    print(f"Après fusion discipline extérieur : {len(data)}")
    
    # Fusion avec les données de jeu
    print("\nFusion des données de jeu...")
    data = data.merge(
        jeu_df,
        left_on=['equipe_domicile', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('', '_jeu_home')
    )
    print(f"Après fusion jeu domicile : {len(data)}")
    
    data = data.merge(
        jeu_df,
        left_on=['equipe_exterieur', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('_jeu_home', '_jeu_away')
    )
    print(f"Après fusion jeu extérieur : {len(data)}")
    
    # Fusion avec les données de coups de pied arrêtés
    print("\nFusion des données de coups de pied arrêtés...")
    data = data.merge(
        cpa_df,
        left_on=['equipe_domicile', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('', '_cpa_home')
    )
    print(f"Après fusion CPA domicile : {len(data)}")
    
    data = data.merge(
        cpa_df,
        left_on=['equipe_exterieur', 'competition'],
        right_on=['equipe', 'competition'],
        suffixes=('_cpa_home', '_cpa_away')
    )
    print(f"Après fusion CPA extérieur : {len(data)}")
    
    # Suppression des colonnes redondantes finales
    columns_to_drop = [col for col in data.columns if col.endswith(('_home', '_away')) and col.startswith('equipe')]
    data = data.drop(columns_to_drop, axis=1)
    
    # Création de la variable cible
    data['resultat'] = np.where(
        data['score_domicile'] > data['score_exterieur'],
        'victoire_domicile',
        np.where(
            data['score_domicile'] < data['score_exterieur'],
            'victoire_exterieur',
            'match_nul'
        )
    )
    
    print(f"\nNombre final de lignes : {len(data)}")
    print(f"Nombre de colonnes : {len(data.columns)}")
    print("\nColonnes disponibles :")
    print(data.columns.tolist())
    
    return data

def prepare_features(data):
    """Préparation des features pour l'entraînement"""
    features = [
        # Statistiques générales
        'buts_marques_domicile_home', 'buts_encaisses_domicile_home',
        'buts_marques_exterieur_away', 'buts_encaisses_exterieur_away',
        'points_par_match_home', 'points_par_match_away',
        
        # Statistiques de discipline
        'cartons_jaunes_discipline_home', 'cartons_rouges_discipline_home',
        'fautes_commises_discipline_home', 'fautes_subies_discipline_home',
        'cartons_jaunes_discipline_away', 'cartons_rouges_discipline_away',
        'fautes_commises_discipline_away', 'fautes_subies_discipline_away',
        
        # Statistiques de jeu
        'possession_moyenne_jeu_home', 'passes_reussies_jeu_home',
        'precision_passes_jeu_home', 'tirs_jeu_home', 'tirs_cadres_jeu_home',
        'corners_jeu_home', 'hors_jeu_jeu_home',
        'possession_moyenne_jeu_away', 'passes_reussies_jeu_away',
        'precision_passes_jeu_away', 'tirs_jeu_away', 'tirs_cadres_jeu_away',
        'corners_jeu_away', 'hors_jeu_jeu_away',
        
        # Statistiques de coups de pied arrêtés
        'penalties_marques_cpa_home', 'penalties_concedes_cpa_home',
        'coups_francs_marques_cpa_home', 'coups_francs_concedes_cpa_home',
        'penalties_marques_cpa_away', 'penalties_concedes_cpa_away',
        'coups_francs_marques_cpa_away', 'coups_francs_concedes_cpa_away'
    ]
    
    X = data[features]
    y = data['resultat']
    
    return X, y

def train_model(X, y):
    """Entraînement du modèle"""
    # Division des données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Standardisation des features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entraînement du modèle
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Évaluation du modèle
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"Score d'entraînement : {train_score:.4f}")
    print(f"Score de test : {test_score:.4f}")
    
    return model, scaler

def save_model(model, scaler):
    """Sauvegarde du modèle et du scaler"""
    models_dir = project_root / 'models'
    models_dir.mkdir(exist_ok=True)
    
    joblib.dump(model, models_dir / 'football_predictor.pkl')
    joblib.dump(scaler, models_dir / 'scaler.pkl')
    
    print("\nModèle et scaler sauvegardés avec succès dans le dossier 'models'")

def main():
    """Fonction principale"""
    print("Chargement des données...")
    data = load_data()
    
    print("\nPréparation des features...")
    X, y = prepare_features(data)
    
    print("\nEntraînement du modèle...")
    model, scaler = train_model(X, y)
    
    print("\nSauvegarde du modèle...")
    save_model(model, scaler)

if __name__ == '__main__':
    main() 