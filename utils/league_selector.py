"""
Utilitaire de sélection de ligue et validation d'équipes
"""
from typing import Dict, Tuple
from data.ligue1_data import LIGUE1_MATCHES
from data.liga_data import LIGA_MATCHES
from data.premier_league_data import PREMIER_LEAGUE_MATCHES
from data.champions_league_data import CHAMPIONS_LEAGUE_MATCHES

LEAGUE_DATA = {
    'ligue1': LIGUE1_MATCHES,
    'liga': LIGA_MATCHES,
    'premier_league': PREMIER_LEAGUE_MATCHES,
    'champions_league': CHAMPIONS_LEAGUE_MATCHES
}

def get_team_league(team: str) -> str:
    """Détermine la ligue d'une équipe"""
    team = team.lower()
    
    ligue1_teams = ['psg', 'marseille', 'lyon', 'lille']
    liga_teams = ['real_madrid', 'barcelona', 'atletico_madrid', 'sevilla']
    premier_league_teams = ['manchester_city', 'arsenal', 'liverpool', 'manchester_united']
    champions_league_teams = [
        'real_madrid', 'manchester_city', 'bayern_munich', 'psg', 'barcelona',
        'liverpool', 'chelsea', 'juventus', 'inter_milan', 'milan',
        'dortmund', 'atletico_madrid', 'porto', 'benfica', 'ajax'
    ]
    
    if team in ligue1_teams:
        return 'ligue1'
    elif team in liga_teams:
        return 'liga'
    elif team in premier_league_teams:
        return 'premier_league'
    elif team in champions_league_teams:
        return 'champions_league'
    else:
        raise ValueError(f"Équipe non reconnue: {team}")

def get_matches_data(team1: str, team2: str) -> Tuple[Dict, str]:
    """Récupère les données de match pour deux équipes"""
    league1 = get_team_league(team1)
    league2 = get_team_league(team2)
    
    # Exception spéciale pour la Ligue des Champions
    if league1 == 'champions_league' or league2 == 'champions_league':
        return LEAGUE_DATA['champions_league'], 'champions_league'
    
    if league1 != league2:
        raise ValueError("Les équipes doivent être de la même ligue")
        
    return LEAGUE_DATA[league1], league1