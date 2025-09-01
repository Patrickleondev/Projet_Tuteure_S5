import pandas as pd
import sys
from pathlib import Path
import importlib.util

# Ajout du chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import des modules de données
from data import (
    ligue1_stats,
    premier_league_stats,
    liga_stats,
    champions_league_stats,
    national_teams_stats
)

def load_module_from_path(path):
    """Charge un module Python à partir d'un chemin"""
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_discipline_data():
    """Création du fichier discipline_data.csv"""
    discipline_data = []
    
    # Données de la Ligue 1
    for team, stats in ligue1_stats.LIGUE1_STATS.items():
        discipline_data.append({
            'equipe': team,
            'competition': 'fr.1',  # Code de la Ligue 1
            'cartons_jaunes': stats.get('cartons_jaunes', 0),
            'cartons_rouges': stats.get('cartons_rouges', 0),
            'fautes_commises': stats.get('fautes_commises', 0),
            'fautes_subies': stats.get('fautes_subies', 0)
        })
    
    # Données de la Premier League
    for team, stats in premier_league_stats.PREMIER_LEAGUE_STATS.items():
        discipline_data.append({
            'equipe': team,
            'competition': 'en.1',  # Code de la Premier League
            'cartons_jaunes': stats.get('cartons_jaunes', 0),
            'cartons_rouges': stats.get('cartons_rouges', 0),
            'fautes_commises': stats.get('fautes_commises', 0),
            'fautes_subies': stats.get('fautes_subies', 0)
        })
    
    # Données de la Liga
    for team, stats in liga_stats.LIGA_STATS.items():
        discipline_data.append({
            'equipe': team,
            'competition': 'es.1',  # Code de la Liga
            'cartons_jaunes': stats.get('cartons_jaunes', 0),
            'cartons_rouges': stats.get('cartons_rouges', 0),
            'fautes_commises': stats.get('fautes_commises', 0),
            'fautes_subies': stats.get('fautes_subies', 0)
        })
    
    # Données de la Champions League
    for team, stats in champions_league_stats.CHAMPIONS_LEAGUE_STATS.items():
        discipline_data.append({
            'equipe': team,
            'competition': 'cl',  # Code de la Champions League
            'cartons_jaunes': stats.get('cartons_jaunes', 0),
            'cartons_rouges': stats.get('cartons_rouges', 0),
            'fautes_commises': stats.get('fautes_commises', 0),
            'fautes_subies': stats.get('fautes_subies', 0)
        })
    
    # Données des équipes nationales
    for team, stats in national_teams_stats.NATIONAL_TEAM_STATS.items():
        discipline_data.append({
            'equipe': team,
            'competition': 'int',  # Code pour les matchs internationaux
            'cartons_jaunes': stats.get('cartons_jaunes', 0),
            'cartons_rouges': stats.get('cartons_rouges', 0),
            'fautes_commises': stats.get('fautes_commises', 0),
            'fautes_subies': stats.get('fautes_subies', 0)
        })
    
    df = pd.DataFrame(discipline_data)
    return df

def create_jeu_data():
    """Création du fichier jeu_data.csv"""
    jeu_data = []
    
    # Données de la Ligue 1
    for team, stats in ligue1_stats.LIGUE1_STATS.items():
        jeu_data.append({
            'equipe': team,
            'competition': 'fr.1',  # Code de la Ligue 1
            'possession_moyenne': stats.get('possession_moyenne', 50),
            'passes_reussies': stats.get('passes_reussies', 0),
            'precision_passes': stats.get('precision_passes', 0),
            'tirs': stats.get('tirs_par_match', 0),
            'tirs_cadres': stats.get('tirs_cadres', 0),
            'corners': stats.get('corners', 0),
            'hors_jeu': stats.get('hors_jeu', 0)
        })
    
    # Données de la Premier League
    for team, stats in premier_league_stats.PREMIER_LEAGUE_STATS.items():
        jeu_data.append({
            'equipe': team,
            'competition': 'en.1',  # Code de la Premier League
            'possession_moyenne': stats.get('possession_moyenne', 50),
            'passes_reussies': stats.get('passes_reussies', 0),
            'precision_passes': stats.get('precision_passes', 0),
            'tirs': stats.get('tirs_par_match', 0),
            'tirs_cadres': stats.get('tirs_cadres', 0),
            'corners': stats.get('corners', 0),
            'hors_jeu': stats.get('hors_jeu', 0)
        })
    
    # Données de la Liga
    for team, stats in liga_stats.LIGA_STATS.items():
        jeu_data.append({
            'equipe': team,
            'competition': 'es.1',  # Code de la Liga
            'possession_moyenne': stats.get('possession_moyenne', 50),
            'passes_reussies': stats.get('passes_reussies', 0),
            'precision_passes': stats.get('precision_passes', 0),
            'tirs': stats.get('tirs_par_match', 0),
            'tirs_cadres': stats.get('tirs_cadres', 0),
            'corners': stats.get('corners', 0),
            'hors_jeu': stats.get('hors_jeu', 0)
        })
    
    # Données de la Champions League
    for team, stats in champions_league_stats.CHAMPIONS_LEAGUE_STATS.items():
        jeu_data.append({
            'equipe': team,
            'competition': 'cl',  # Code de la Champions League
            'possession_moyenne': stats.get('possession_moyenne', 50),
            'passes_reussies': stats.get('passes_reussies', 0),
            'precision_passes': stats.get('precision_passes', 0),
            'tirs': stats.get('tirs_par_match', 0),
            'tirs_cadres': stats.get('tirs_cadres', 0),
            'corners': stats.get('corners', 0),
            'hors_jeu': stats.get('hors_jeu', 0)
        })
    
    # Données des équipes nationales
    for team, stats in national_teams_stats.NATIONAL_TEAM_STATS.items():
        jeu_data.append({
            'equipe': team,
            'competition': 'int',  # Code pour les matchs internationaux
            'possession_moyenne': stats.get('possession_moyenne', 50),
            'passes_reussies': stats.get('passes_reussies', 0),
            'precision_passes': stats.get('precision_passes', 0),
            'tirs': stats.get('tirs_par_match', 0),
            'tirs_cadres': stats.get('tirs_cadres', 0),
            'corners': stats.get('corners', 0),
            'hors_jeu': stats.get('hors_jeu', 0)
        })
    
    df = pd.DataFrame(jeu_data)
    return df

def create_coups_de_pied_arretes_data():
    """Création du fichier coups_de_pied_arretes_data.csv"""
    cpa_data = []
    
    # Données de la Ligue 1
    for team, stats in ligue1_stats.LIGUE1_STATS.items():
        cpa_data.append({
            'equipe': team,
            'competition': 'fr.1',  # Code de la Ligue 1
            'penalties_marques': stats.get('penalties_marques', 0),
            'penalties_concedes': stats.get('penalties_concedes', 0),
            'coups_francs_marques': stats.get('coups_francs_marques', 0),
            'coups_francs_concedes': stats.get('coups_francs_concedes', 0)
        })
    
    # Données de la Premier League
    for team, stats in premier_league_stats.PREMIER_LEAGUE_STATS.items():
        cpa_data.append({
            'equipe': team,
            'competition': 'en.1',  # Code de la Premier League
            'penalties_marques': stats.get('penalties_marques', 0),
            'penalties_concedes': stats.get('penalties_concedes', 0),
            'coups_francs_marques': stats.get('coups_francs_marques', 0),
            'coups_francs_concedes': stats.get('coups_francs_concedes', 0)
        })
    
    # Données de la Liga
    for team, stats in liga_stats.LIGA_STATS.items():
        cpa_data.append({
            'equipe': team,
            'competition': 'es.1',  # Code de la Liga
            'penalties_marques': stats.get('penalties_marques', 0),
            'penalties_concedes': stats.get('penalties_concedes', 0),
            'coups_francs_marques': stats.get('coups_francs_marques', 0),
            'coups_francs_concedes': stats.get('coups_francs_concedes', 0)
        })
    
    # Données de la Champions League
    for team, stats in champions_league_stats.CHAMPIONS_LEAGUE_STATS.items():
        cpa_data.append({
            'equipe': team,
            'competition': 'cl',  # Code de la Champions League
            'penalties_marques': stats.get('penalties_marques', 0),
            'penalties_concedes': stats.get('penalties_concedes', 0),
            'coups_francs_marques': stats.get('coups_francs_marques', 0),
            'coups_francs_concedes': stats.get('coups_francs_concedes', 0)
        })
    
    # Données des équipes nationales
    for team, stats in national_teams_stats.NATIONAL_TEAM_STATS.items():
        cpa_data.append({
            'equipe': team,
            'competition': 'int',  # Code pour les matchs internationaux
            'penalties_marques': stats.get('penalties_marques', 0),
            'penalties_concedes': stats.get('penalties_concedes', 0),
            'coups_francs_marques': stats.get('coups_francs_marques', 0),
            'coups_francs_concedes': stats.get('coups_francs_concedes', 0)
        })
    
    df = pd.DataFrame(cpa_data)
    return df

def main():
    """Fonction principale"""
    print("Création des fichiers de données statistiques...")
    
    # Création du dossier de sortie s'il n'existe pas
    output_dir = project_root.parent / 'FIP_DB'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Création et sauvegarde des fichiers
    print("- Préparation des données de discipline...")
    discipline_df = create_discipline_data()
    discipline_df.to_csv(output_dir / 'discipline_data.csv', index=False)
    
    print("- Préparation des données de jeu...")
    jeu_df = create_jeu_data()
    jeu_df.to_csv(output_dir / 'jeu_data.csv', index=False)
    
    print("- Préparation des données de coups de pied arrêtés...")
    cpa_df = create_coups_de_pied_arretes_data()
    cpa_df.to_csv(output_dir / 'coups_de_pied_arretes_data.csv', index=False)
    
    print("\nFichiers CSV générés avec succès dans le dossier FIP_DB :")
    print("- discipline_data.csv")
    print("- jeu_data.csv")
    print("- coups_de_pied_arretes_data.csv")

if __name__ == '__main__':
    main() 