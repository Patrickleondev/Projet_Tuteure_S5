"""
Analyseur de matchs et calculateur de tendances
"""
from typing import Dict, List, Tuple
import statistics
from datetime import datetime

def analyze_historical_matches(matches_data: Dict, team1: str, team2: str) -> Dict:
    """Analyse les tendances historiques entre deux équipes"""
    key = f"{team1}_vs_{team2}"
    matches = matches_data.get(key, {})
    
    if not matches:
        raise ValueError("Pas assez de données historiques pour ces équipes")
    
    stats = {
        'buts_moyenne_equipe1': [],
        'buts_moyenne_equipe2': [],
        'possession_moyenne_equipe1': [],
        'tirs_moyenne_equipe1': [],
        'tirs_moyenne_equipe2': [],
        'cartons_moyenne': []
    }
    
    for date, match in matches.items():
        stats['buts_moyenne_equipe1'].append(match['buts_equipe1'])
        stats['buts_moyenne_equipe2'].append(match['buts_equipe2'])
        stats['possession_moyenne_equipe1'].append(match['possession_equipe1'])
        stats['tirs_moyenne_equipe1'].append(match['tirs_equipe1'])
        stats['tirs_moyenne_equipe2'].append(match['tirs_equipe2'])
        stats['cartons_moyenne'].append(match['cartons_jaunes'] + match['cartons_rouges'])
    
    return {
        'buts_moy_equipe1': statistics.mean(stats['buts_moyenne_equipe1']),
        'buts_moy_equipe2': statistics.mean(stats['buts_moyenne_equipe2']),
        'possession_moy_equipe1': statistics.mean(stats['possession_moyenne_equipe1']),
        'tirs_moy_equipe1': statistics.mean(stats['tirs_moyenne_equipe1']),
        'tirs_moy_equipe2': statistics.mean(stats['tirs_moyenne_equipe2']),
        'cartons_moy': statistics.mean(stats['cartons_moyenne'])
    }