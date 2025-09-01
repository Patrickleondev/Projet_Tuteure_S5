"""
Sélecteur de compétitions nationales
"""
from typing import Dict, Tuple
from data.euro_data import EURO_MATCHES
from data.world_cup_data import WORLD_CUP_MATCHES
from data.copa_america_data import COPA_AMERICA_MATCHES

NATIONAL_COMPETITIONS = {
    'euro': EURO_MATCHES,
    'world_cup': WORLD_CUP_MATCHES,
    'copa_america': COPA_AMERICA_MATCHES
}

def get_national_team_competition(team1: str, team2: str) -> Tuple[Dict, str]:
    """Détermine la compétition nationale pour deux équipes"""
    european_teams = ['france', 'allemagne', 'espagne', 'italie', 'angleterre', 'portugal', 'belgique', 'pays_bas', 'croatie', 'danemark']
    south_american_teams = ['argentine', 'bresil', 'uruguay', 'colombie', 'chili', 'perou', 'paraguay', 'equateur', 'venezuela', 'bolivie']
    
    team1, team2 = team1.lower(), team2.lower()
    
    if team1 in european_teams and team2 in european_teams:
        return EURO_MATCHES, 'euro'
    elif team1 in south_american_teams and team2 in south_american_teams:
        return COPA_AMERICA_MATCHES, 'copa_america'
    else:
        return WORLD_CUP_MATCHES, 'world_cup'