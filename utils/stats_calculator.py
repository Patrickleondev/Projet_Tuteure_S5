"""
Utilitaires pour calculer les statistiques et les prédictions
"""
from typing import List, Dict, Tuple
import random

def calculate_average(numbers: List[float]) -> float:
    """Calcule la moyenne d'une liste de nombres"""
    return sum(numbers) / len(numbers) if numbers else 0

def add_random_variance(value: float, variance_percent: float = 0.15) -> float:
    """Ajoute une variance aléatoire à une valeur"""
    variance = value * variance_percent
    return value + random.uniform(-variance, variance)

def predict_match_stats(historical_data: Dict, team1: str, team2: str) -> Tuple[Dict, float]:
    """Prédit les statistiques du match"""
    try:
        # Vérifier les deux combinaisons possibles
        key = f"{team1.lower()}_vs_{team2.lower()}"
        reverse_key = f"{team2.lower()}_vs_{team1.lower()}"
        
        if key in historical_data:
            data = historical_data[key]
            reverse = False
        elif reverse_key in historical_data:
            data = historical_data[reverse_key]
            reverse = True
        else:
            return generate_default_prediction(), 70.0

        # Calcul des moyennes avec variance aléatoire
        buts_equipe1 = round(add_random_variance(calculate_average(
            data['buts_equipe1' if not reverse else 'buts_equipe2'])))
        buts_equipe2 = round(add_random_variance(calculate_average(
            data['buts_equipe2' if not reverse else 'buts_equipe1'])))

        # Calculer les probabilités basées sur les buts
        total_buts = buts_equipe1 + buts_equipe2
        if total_buts == 0:
            home_win = 33.33
            draw = 33.34
            away_win = 33.33
        else:
            home_win = (buts_equipe1 / total_buts) * 100
            away_win = (buts_equipe2 / total_buts) * 100
            draw = 100 - (home_win + away_win)

        predictions = {
            # Probabilités
            'home_win': round(home_win, 2),
            'draw': round(draw, 2),
            'away_win': round(away_win, 2),
            
            # Cartons
            'cards': {
                'yellow': {
                    'home': round(add_random_variance(calculate_average(
                data['cartons_jaunes']) / 2)),
                    'away': round(add_random_variance(calculate_average(
                        data['cartons_jaunes']) / 2))
                },
                'red': {
                    'home': round(add_random_variance(calculate_average(
                data['cartons_rouges']) / 2)),
                    'away': round(add_random_variance(calculate_average(
                        data['cartons_rouges']) / 2))
                }
            },
            
            # Coups de pied arrêtés
            'set_pieces': {
                'corners': {
                    'home': round(add_random_variance(calculate_average(
                data['coups_francs']) / 2)),
                    'away': round(add_random_variance(calculate_average(
                        data['coups_francs']) / 2))
                },
                'free_kicks': {
                    'home': round(add_random_variance(calculate_average(
                data['coups_francs']) / 2)),
                    'away': round(add_random_variance(calculate_average(
                        data['coups_francs']) / 2))
                }
            },
            
            # Fautes
            'fouls': {
                'home': round(add_random_variance(calculate_average(
                data['fautes']) / 2)),
                'away': round(add_random_variance(calculate_average(
                    data['fautes']) / 2))
            },
            
            # Passes
            'passes': {
                'home': round(add_random_variance(calculate_average(
                data['passes_reussies_equipe1' if not reverse else 'passes_reussies_equipe2']))),
                'away': round(add_random_variance(calculate_average(
                data['passes_reussies_equipe2' if not reverse else 'passes_reussies_equipe1'])))
            }
        }
        
        return predictions, 85.0

    except Exception as e:
        print(f"Erreur lors de la prédiction: {str(e)}")
        return generate_default_prediction(), 70.0

def generate_default_prediction() -> Dict:
    """Génère une prédiction par défaut quand il n'y a pas de données historiques"""
    return {
        'home_win': 33.33,
        'draw': 33.34,
        'away_win': 33.33,
        'cards': {
            'yellow': {'home': 2, 'away': 2},
            'red': {'home': 0, 'away': 0}
        },
        'set_pieces': {
            'corners': {'home': 5, 'away': 5},
            'free_kicks': {'home': 3, 'away': 3}
        },
        'fouls': {'home': 10, 'away': 10},
        'passes': {'home': 450, 'away': 450}
    }