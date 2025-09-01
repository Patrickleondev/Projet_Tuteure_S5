"""
Moteur de prédiction basé sur les données historiques et les statistiques d'équipe
"""
from typing import Dict, Tuple
import random
from data.team_stats import TEAM_STATS

def calculate_form_factor(team_stats: Dict) -> float:
    """Calcule un facteur de forme basé sur les statistiques globales"""
    return (
        team_stats['precision_passes'] * 0.3 +
        team_stats['duels_gagnes'] * 0.3 +
        (1 / team_stats['classement_moyen']) * 20 +
        team_stats['possession_moyenne'] * 0.2
    ) / 100

def predict_match_result(
    historical_analysis: Dict,
    team1: str,
    team2: str,
    team_stats: Dict = TEAM_STATS
) -> Tuple[Dict, float]:
    """
    Prédit le résultat du match en utilisant l'analyse historique
    et les statistiques générales des équipes
    """
    team1_form = calculate_form_factor(team_stats[team1])
    team2_form = calculate_form_factor(team_stats[team2])
    form_ratio = team1_form / team2_form

    # Ajustement des prédictions basé sur la forme
    buts_equipe1 = historical_analysis['buts_moy_equipe1'] * form_ratio
    buts_equipe2 = historical_analysis['buts_moy_equipe2'] / form_ratio

    # Ajout d'un facteur aléatoire contrôlé
    variance = 0.15
    buts_equipe1 *= random.uniform(1 - variance, 1 + variance)
    buts_equipe2 *= random.uniform(1 - variance, 1 + variance)

    predictions = {
        'buts_equipe1': round(buts_equipe1),
        'buts_equipe2': round(buts_equipe2),
        'possession_equipe1': round(historical_analysis['possession_moy_equipe1'] * form_ratio),
        'tirs_equipe1': round(historical_analysis['tirs_moy_equipe1'] * form_ratio),
        'tirs_equipe2': round(historical_analysis['tirs_moy_equipe2'] / form_ratio),
        'cartons_total': round(historical_analysis['cartons_moy'])
    }

    # Calcul de la précision basé sur la quantité de données et la variance
    precision = min(85, 70 + (team1_form + team2_form) * 10)

    return predictions, precision