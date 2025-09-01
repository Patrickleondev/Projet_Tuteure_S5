"""
Données réelles des matchs de Ligue 1 (2020-2023)
Format optimisé pour l'entraînement du modèle
"""

LIGUE1_MATCHES = {
    'psg_vs_marseille': {
        # Saison 2022-2023
        '2023_02_26': {
            'buts_equipe1': 3,  # PSG
            'buts_equipe2': 0,  # Marseille
            'possession_equipe1': 59,
            'possession_equipe2': 41,
            'tirs_equipe1': 19,
            'tirs_equipe2': 11,
            'tirs_cadres_equipe1': 8,
            'tirs_cadres_equipe2': 3,
            'cartons_jaunes': 5,
            'cartons_rouges': 0,
            'passes_reussies_equipe1': 542,
            'passes_reussies_equipe2': 401,
            'coups_francs': 23,
            'corners_equipe1': 7,
            'corners_equipe2': 4,
            'fautes': 28
        },
        # Saison 2021-2022
        '2022_04_17': {
            'buts_equipe1': 2,
            'buts_equipe2': 1,
            'possession_equipe1': 62,
            'possession_equipe2': 38,
            'tirs_equipe1': 16,
            'tirs_equipe2': 9,
            'tirs_cadres_equipe1': 7,
            'tirs_cadres_equipe2': 4,
            'cartons_jaunes': 6,
            'cartons_rouges': 1,
            'passes_reussies_equipe1': 568,
            'passes_reussies_equipe2': 389,
            'coups_francs': 19,
            'corners_equipe1': 8,
            'corners_equipe2': 3,
            'fautes': 25
        }
    },
    'lyon_vs_lille': {
        # Saison 2022-2023
        '2023_03_12': {
            'buts_equipe1': 3,  # Lyon
            'buts_equipe2': 3,  # Lille
            'possession_equipe1': 51,
            'possession_equipe2': 49,
            'tirs_equipe1': 14,
            'tirs_equipe2': 13,
            'tirs_cadres_equipe1': 6,
            'tirs_cadres_equipe2': 7,
            'cartons_jaunes': 4,
            'cartons_rouges': 0,
            'passes_reussies_equipe1': 478,
            'passes_reussies_equipe2': 465,
            'coups_francs': 21,
            'corners_equipe1': 6,
            'corners_equipe2': 5,
            'fautes': 24
        },
        # Saison 2021-2022
        '2022_03_27': {
            'buts_equipe1': 1,
            'buts_equipe2': 0,
            'possession_equipe1': 54,
            'possession_equipe2': 46,
            'tirs_equipe1': 12,
            'tirs_equipe2': 10,
            'tirs_cadres_equipe1': 5,
            'tirs_cadres_equipe2': 3,
            'cartons_jaunes': 3,
            'cartons_rouges': 0,
            'passes_reussies_equipe1': 492,
            'passes_reussies_equipe2': 445,
            'coups_francs': 18,
            'corners_equipe1': 5,
            'corners_equipe2': 4,
            'fautes': 22
        }
    }
}