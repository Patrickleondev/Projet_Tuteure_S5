"""
Service de prédiction utilisant le modèle de régression linéaire
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import os

class RegressionPredictionService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
        
    def load_model(self):
        """Chargement du modèle de régression et du scaler"""
        try:
            # Chemin vers le modèle de régression - correction du chemin
            model_path = Path(__file__).parent.parent / 'models' / 'football_predictor.pkl'
            scaler_path = Path(__file__).parent.parent / 'models' / 'scaler_regression.pkl'
            
            if model_path.exists() and scaler_path.exists():
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                print("Modèle de régression chargé avec succès")
            else:
                print(f"Fichiers du modèle de régression non trouvés")
                print(f"Modèle attendu: {model_path}")
                print(f"Scaler attendu: {scaler_path}")
                self.model = None
                self.scaler = None
                
        except Exception as e:
            print(f"Erreur lors du chargement du modèle de régression: {str(e)}")
            self.model = None
            self.scaler = None
    
    def prepare_features(self, equipe_domicile, equipe_exterieur):
        """Préparation des features pour la prédiction"""
        try:
            # Chargement des données des équipes - correction du chemin
            data_dir = Path(__file__).parent.parent / 'FIP_DB'
            equipes_df = pd.read_csv(data_dir / 'equipes_par_championnat.csv')
            
            # Récupération des statistiques des équipes
            equipe_dom = equipes_df[equipes_df['Équipe'] == equipe_domicile]
            equipe_ext = equipes_df[equipes_df['Équipe'] == equipe_exterieur]
            
            if equipe_dom.empty or equipe_ext.empty:
                raise ValueError(f"Équipe(s) non trouvée(s): {equipe_domicile} ou {equipe_exterieur}")
            
            # Calcul des différences de statistiques
            diff_tirs = equipe_dom['Tirs Par Match'].iloc[0] - equipe_ext['Tirs Par Match'].iloc[0]
            diff_possession = equipe_dom['Possession Moyenne'].iloc[0] - equipe_ext['Possession Moyenne'].iloc[0]
            diff_passes = equipe_dom['Précision Passes'].iloc[0] - equipe_ext['Précision Passes'].iloc[0]
            
            # Valeurs par défaut pour les cartons (à améliorer avec des données réelles)
            cartons_jaunes = 2.5  # Moyenne par match
            cartons_rouges = 0.1  # Moyenne par match
            
            # Création du vecteur de features
            features = np.array([[
                diff_tirs,
                diff_possession,
                diff_passes,
                cartons_jaunes,
                cartons_rouges
            ]])
            
            return features
            
        except Exception as e:
            print(f"Erreur lors de la préparation des features: {str(e)}")
            return None
    
    def predict_goals(self, equipe_domicile, equipe_exterieur):
        """Prédiction du nombre de buts marqués par l'équipe domicile"""
        if not self.model or not self.scaler:
            return None
            
        try:
            # Préparation des features
            features = self.prepare_features(equipe_domicile, equipe_exterieur)
            if features is None:
                return None
            
            # Standardisation des features
            features_scaled = self.scaler.transform(features)
            
            # Prédiction
            goals_predicted = self.model.predict(features_scaled)[0]
            
            # S'assurer que la prédiction est positive
            goals_predicted = max(0, goals_predicted)
            
            return round(goals_predicted, 1)
            
        except Exception as e:
            print(f"Erreur lors de la prédiction: {str(e)}")
            return None
    
    def predict_match_result(self, equipe_domicile, equipe_exterieur):
        """Prédiction complète du résultat d'un match"""
        if not self.model or not self.scaler:
            return None
            
        try:
            # Prédiction des buts pour l'équipe domicile
            goals_home = self.predict_goals(equipe_domicile, equipe_exterieur)
            
            # Prédiction des buts pour l'équipe extérieur (inverser les équipes)
            goals_away = self.predict_goals(equipe_exterieur, equipe_domicile)
            
            if goals_home is None or goals_away is None:
                return None
            
            # Détermination du résultat
            if goals_home > goals_away:
                result = "Victoire domicile"
                winner = equipe_domicile
            elif goals_away > goals_home:
                result = "Victoire extérieur"
                winner = equipe_exterieur
            else:
                result = "Match nul"
                winner = "Nul"
            
            # Calcul des probabilités (approximation basée sur la différence de buts)
            goal_diff = abs(goals_home - goals_away)
            if goal_diff < 0.5:
                prob_home = 0.35
                prob_away = 0.35
                prob_draw = 0.30
            elif goals_home > goals_away:
                prob_home = 0.60
                prob_away = 0.20
                prob_draw = 0.20
            else:
                prob_home = 0.20
                prob_away = 0.60
                prob_draw = 0.20
            
            return {
                'equipe_domicile': equipe_domicile,
                'equipe_exterieur': equipe_exterieur,
                'buts_equipe1': goals_home,
                'buts_equipe2': goals_away,
                'resultat': result,
                'gagnant': winner,
                'probabilites': {
                    'victoire_domicile': prob_home,
                    'victoire_exterieur': prob_away,
                    'match_nul': prob_draw
                },
                'statistiques': {
                    'cartons_jaunes': 2.5,
                    'cartons_rouges': 0.1,
                    'passes_reussies_equipe1': 85.0,
                    'passes_reussies_equipe2': 82.0,
                    'coups_francs': 12.0,
                    'fautes': 15.0
                }
            }
            
        except Exception as e:
            print(f"Erreur lors de la prédiction du match: {str(e)}")
            return None 