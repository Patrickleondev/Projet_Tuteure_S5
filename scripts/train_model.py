"""
Script d'entraînement du modèle de prédiction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib
import os
import sys
from pathlib import Path

# Ajout du répertoire parent au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from models.match_predictor import FootballMatchPredictor

def load_and_prepare_data():
    """Chargement et préparation des données"""
    # Chargement des données
    data_dir = project_root.parent / 'FIP_DB'
    matches_df = pd.read_csv(data_dir / 'matchs_data.csv')
    teams_df = pd.read_csv(data_dir / 'equipes_data.csv')
    
    # Fusion avec les statistiques de l'équipe à domicile
    df = matches_df.merge(
        teams_df,
        left_on='equipe_domicile',
        right_on='equipe',
        how='left',
        suffixes=('', '_home')
    )
    
    # Fusion avec les statistiques de l'équipe à l'extérieur
    df = df.merge(
        teams_df,
        left_on='equipe_exterieur',
        right_on='equipe',
        how='left',
        suffixes=('_home', '_away')
    )
    
    # Création des features de forme récente
    df = add_recent_form_features(df)
    
    # Création des features de confrontations directes
    df = add_head_to_head_features(df)
    
    # Création de la variable cible (0: victoire domicile, 1: nul, 2: victoire extérieur)
    df['resultat'] = np.where(df['score_domicile'] > df['score_exterieur'], 0,
                    np.where(df['score_domicile'] == df['score_exterieur'], 1, 2))
    
    return df

def add_recent_form_features(df):
    """Ajout des features de forme récente"""
    def calculate_form(group, n_matches=5):
        group = group.sort_values('date')
        group['victoires'] = (group['score_domicile'] > group['score_exterieur']).rolling(n_matches, min_periods=1).mean()
        group['nuls'] = (group['score_domicile'] == group['score_exterieur']).rolling(n_matches, min_periods=1).mean()
        group['defaites'] = (group['score_domicile'] < group['score_exterieur']).rolling(n_matches, min_periods=1).mean()
        return group
    
    # Calcul pour les équipes à domicile
    form_home = df.groupby('equipe_domicile').apply(calculate_form).reset_index(drop=True)
    df['forme_victoires_domicile'] = form_home['victoires']
    df['forme_nuls_domicile'] = form_home['nuls']
    df['forme_defaites_domicile'] = form_home['defaites']
    
    # Calcul pour les équipes à l'extérieur
    form_away = df.groupby('equipe_exterieur').apply(calculate_form).reset_index(drop=True)
    df['forme_victoires_exterieur'] = form_away['victoires']
    df['forme_nuls_exterieur'] = form_away['nuls']
    df['forme_defaites_exterieur'] = form_away['defaites']
    
    return df

def add_head_to_head_features(df):
    """Ajout des features de confrontations directes"""
    def calculate_h2h(group):
        group = group.sort_values('date')
        group['h2h_victoires_domicile'] = (group['score_domicile'] > group['score_exterieur']).expanding().mean()
        group['h2h_victoires_exterieur'] = (group['score_domicile'] < group['score_exterieur']).expanding().mean()
        group['h2h_nuls'] = (group['score_domicile'] == group['score_exterieur']).expanding().mean()
        group['h2h_buts_domicile'] = group['score_domicile'].expanding().mean()
        group['h2h_buts_exterieur'] = group['score_exterieur'].expanding().mean()
        return group
    
    h2h = df.groupby(['equipe_domicile', 'equipe_exterieur']).apply(calculate_h2h).reset_index(drop=True)
    
    # Ajout des features H2H
    for col in ['h2h_victoires_domicile', 'h2h_victoires_exterieur', 'h2h_nuls',
                'h2h_buts_domicile', 'h2h_buts_exterieur']:
        df[col] = h2h[col]
    
    return df

def train_model():
    """Entraînement du modèle"""
    try:
        print("Chargement et préparation des données...")
        df = load_and_prepare_data()
        
        print("\nDimensions des données:", df.shape)
        print("\nColonnes disponibles:", df.columns.tolist())
        
        print("\nSplit des données...")
        train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['resultat'])
        
        print("\nDistribution de la variable cible:")
        print(df['resultat'].value_counts(normalize=True))
        
        print("\nInitialisation et entraînement du modèle...")
        model = FootballMatchPredictor()
        model.train(train_df, valid_df)
        
        print("\nSauvegarde du modèle...")
        model_dir = project_root / 'models'
        model_dir.mkdir(exist_ok=True)
        model_path = model_dir / 'football_predictor.pkl'
        joblib.dump(model, model_path)
        print(f"Modèle sauvegardé dans {model_path}")
        
        # Affichage des features les plus importantes
        print("\nFeatures les plus importantes:")
        for feature, importance in model.get_feature_importance().items():
            print(f"{feature}: {importance:.4f}")
            
        print("\nEntraînement terminé avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'entraînement: {str(e)}")
        import traceback
        print("\nTraceback complet:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    train_model() 