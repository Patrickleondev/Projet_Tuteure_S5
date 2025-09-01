"""
Statistiques des équipes nationales (2020-2023)
Données enrichies avec les performances en compétitions majeures
"""

NATIONAL_TEAM_STATS = {
    'france': {
        'classement_fifa': 2,
        'buts_marques_moy': 2.4,
        'buts_encaisses_moy': 0.8,
        'clean_sheets_pourcentage': 45,
        'possession_moyenne': 58,
        'precision_passes': 88,
        'duels_gagnes': 53,
        'tirs_par_match': 15.2,
        'derniere_competition': {
            'nom': 'Coupe du Monde 2022',
            'resultat': 'Finaliste',
            'buts_marques': 16,
            'buts_encaisses': 8
        },
        'joueurs_cles': ['Mbappé', 'Griezmann', 'Tchouaméni'],
        'style_jeu': 'Possession et contre-attaques rapides'
    },
    'bresil': {
        'classement_fifa': 3,
        'buts_marques_moy': 2.6,
        'buts_encaisses_moy': 0.7,
        'clean_sheets_pourcentage': 50,
        'possession_moyenne': 62,
        'precision_passes': 89,
        'duels_gagnes': 54,
        'tirs_par_match': 16.5,
        'derniere_competition': {
            'nom': 'Copa America 2021',
            'resultat': 'Finaliste',
            'buts_marques': 12,
            'buts_encaisses': 3
        },
        'joueurs_cles': ['Neymar', 'Casemiro', 'Marquinhos'],
        'style_jeu': 'Jeu offensif et technique'
    },
    'argentine': {
        'classement_fifa': 1,
        'buts_marques_moy': 2.5,
        'buts_encaisses_moy': 0.6,
        'clean_sheets_pourcentage': 55,
        'possession_moyenne': 60,
        'precision_passes': 87,
        'duels_gagnes': 52,
        'tirs_par_match': 14.8,
        'derniere_competition': {
            'nom': 'Coupe du Monde 2022',
            'resultat': 'Vainqueur',
            'buts_marques': 15,
            'buts_encaisses': 8
        },
        'joueurs_cles': ['Messi', 'Martinez', 'Di Maria'],
        'style_jeu': 'Possession et pressing haut'
    },
    'allemagne': {
        'classement_fifa': 15,
        'buts_marques_moy': 2.2,
        'buts_encaisses_moy': 1.1,
        'clean_sheets_pourcentage': 40,
        'possession_moyenne': 65,
        'precision_passes': 90,
        'duels_gagnes': 51,
        'tirs_par_match': 15.5,
        'derniere_competition': {
            'nom': 'Coupe du Monde 2022',
            'resultat': 'Phase de groupes',
            'buts_marques': 6,
            'buts_encaisses': 5
        },
        'joueurs_cles': ['Kimmich', 'Gündogan', 'Müller'],
        'style_jeu': 'Possession et pressing collectif'
    },
    'espagne': {
        'classement_fifa': 8,
        'buts_marques_moy': 2.1,
        'buts_encaisses_moy': 0.9,
        'clean_sheets_pourcentage': 42,
        'possession_moyenne': 70,
        'precision_passes': 91,
        'duels_gagnes': 50,
        'tirs_par_match': 14.2,
        'derniere_competition': {
            'nom': 'Coupe du Monde 2022',
            'resultat': 'Huitièmes de finale',
            'buts_marques': 9,
            'buts_encaisses': 3
        },
        'joueurs_cles': ['Pedri', 'Gavi', 'Morata'],
        'style_jeu': 'Tiki-taka et pressing haut'
    }
}

def get_team_form(team_id: str, last_n_matches: int = 5) -> float:
    """
    Calcule la forme d'une équipe basée sur ses derniers matchs
    Retourne une note sur 10
    """
    if team_id not in NATIONAL_TEAM_STATS:
        raise ValueError(f"Équipe {team_id} non trouvée")
    
    team = NATIONAL_TEAM_STATS[team_id]
    
    # Facteurs de forme
    form_factors = {
        'buts_marques': team['buts_marques_moy'] * 2,
        'clean_sheets': team['clean_sheets_pourcentage'] / 10,
        'possession': team['possession_moyenne'] / 10,
        'derniere_competition': _evaluate_competition_performance(team['derniere_competition'])
    }
    
    return min(sum(form_factors.values()), 10)

def _evaluate_competition_performance(competition: dict) -> float:
    """
    Évalue la performance lors de la dernière compétition majeure
    Retourne une note sur 3
    """
    result_scores = {
        'Vainqueur': 3.0,
        'Finaliste': 2.5,
        'Demi-finaliste': 2.0,
        'Quart de finale': 1.5,
        'Huitièmes de finale': 1.0,
        'Phase de groupes': 0.5
    }
    
    return result_scores.get(competition['resultat'], 0.0)

def get_head_to_head_stats(team1_id: str, team2_id: str) -> dict:
    """
    Analyse les confrontations directes entre deux équipes
    """
    # À implémenter avec les données historiques
    pass