"""
Modèle de prédiction des matchs de football
"""
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class FootballMatchPredictor:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_columns = [
            # Statistiques de l'équipe à domicile
            'buts_marques_domicile_home',
            'buts_encaisses_domicile_home',
            'matchs_joues_home',
            'victoires_domicile_home',
            'points_par_match_home',
            
            # Statistiques de l'équipe à l'extérieur
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
    
    def prepare_features(self, df):
        """Préparation des features pour l'entraînement ou la prédiction"""
        # Sélection et mise à l'échelle des features
        X = df[self.feature_columns].copy()
        
        # Remplacement des valeurs manquantes par la moyenne
        X = X.fillna(X.mean())
        
        return X
    
    def train(self, train_df, valid_df=None):
        """Entraînement du modèle"""
        # Préparation des données d'entraînement
        X_train = self.prepare_features(train_df)
        y_train = train_df['resultat']
        
        # Mise à l'échelle des features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Entraînement du modèle
        self.model.fit(X_train_scaled, y_train)
        
        # Évaluation sur l'ensemble de validation si fourni
        if valid_df is not None:
            X_valid = self.prepare_features(valid_df)
            y_valid = valid_df['resultat']
            X_valid_scaled = self.scaler.transform(X_valid)
            
            valid_score = self.model.score(X_valid_scaled, y_valid)
            print(f"\nScore de validation: {valid_score:.4f}")
    
    def predict_proba(self, match_data):
        """Prédiction des probabilités pour un match"""
        X = self.prepare_features(match_data)
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    def get_feature_importance(self):
        """Retourne l'importance des features"""
        importance = self.model.feature_importances_
        return dict(zip(self.feature_columns, importance)) 