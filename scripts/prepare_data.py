"""
Script de préparation des données pour l'entraînement
"""
import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys

# Ajout du chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def standardize_team_name(name):
    """Standardise le nom d'une équipe"""
    # Dictionnaire de correspondance
    team_mapping = {
        'Bayern München': 'bayern_munich',
        'Borussia Dortmund': 'dortmund',
        'Paris Saint-Germain': 'psg',
        'Olympique Marseille': 'marseille',
        'Real Madrid': 'real_madrid',
        'Barcelona': 'barcelona',
        'Atlético Madrid': 'atletico_madrid',
        'Manchester City': 'manchester_city',
        'Arsenal': 'arsenal',
        'Liverpool': 'liverpool',
        'Manchester United': 'manchester_united',
        'Chelsea': 'chelsea',
        'Juventus': 'juventus',
        'Inter': 'inter_milan',
        'AC Milan': 'milan',
        'FC Porto': 'porto',
        'Benfica': 'benfica',
        'Ajax': 'ajax'
    }
    
    # Nettoyage du nom
    clean_name = name.strip()
    
    # Retourne le nom standardisé s'il existe, sinon le nom original
    return team_mapping.get(clean_name, clean_name.lower().replace(' ', '_'))

def load_league_data(league_dir):
    """Charge les données d'une ligue pour une saison"""
    all_matches = []
    
    # Parcours des fichiers CSV
    for csv_file in league_dir.glob('*.csv'):
        df = pd.read_csv(csv_file)
        
        # Standardisation des colonnes
        if 'Team 1' in df.columns:
            df = df.rename(columns={
                'Team 1': 'equipe_domicile',
                'Team 2': 'equipe_exterieur',
                'FT': 'score'
            })
        
        # Standardisation des noms d'équipes
        df['equipe_domicile'] = df['equipe_domicile'].apply(standardize_team_name)
        df['equipe_exterieur'] = df['equipe_exterieur'].apply(standardize_team_name)
        
        # Nettoyage des scores
        df = df.dropna(subset=['score'])  # Suppression des lignes sans score
        
        try:
            # Extraction des scores avec gestion des erreurs
            scores = df['score'].str.split('-', expand=True)
            scores = scores.apply(pd.to_numeric, errors='coerce')
            df['score_domicile'] = scores[0]
            df['score_exterieur'] = scores[1]
            
            # Suppression des lignes avec des scores invalides
            df = df.dropna(subset=['score_domicile', 'score_exterieur'])
            df['score_domicile'] = df['score_domicile'].astype(int)
            df['score_exterieur'] = df['score_exterieur'].astype(int)
            
            # Ajout de la date et de la compétition
            season = league_dir.parent.name
            competition = csv_file.stem
            df['date'] = pd.to_datetime(df['Date'])
            df['competition'] = competition
            df['saison'] = season
            
            all_matches.append(df)
            
        except Exception as e:
            print(f"Erreur lors du traitement de {csv_file}: {str(e)}")
            continue
    
    return pd.concat(all_matches) if all_matches else None

def prepare_team_stats(matches_df):
    """Prépare les statistiques des équipes"""
    team_stats = []
    
    # Grouper les matchs par équipe et compétition
    for competition in matches_df['competition'].unique():
        competition_matches = matches_df[matches_df['competition'] == competition]
        
        # Statistiques pour les équipes à domicile
        home_stats = competition_matches.groupby('equipe_domicile').agg({
            'score_domicile': ['sum', 'count'],
            'score_exterieur': 'sum'
        }).reset_index()
        
        # Renommer les colonnes après l'agrégation
        home_stats.columns = ['equipe_domicile', 'buts_marques_domicile', 'matchs_joues', 'buts_encaisses_domicile']
        home_stats['competition'] = competition
        
        # Statistiques pour les équipes à l'extérieur
        away_stats = competition_matches.groupby('equipe_exterieur').agg({
            'score_exterieur': 'sum',
            'score_domicile': 'sum'
        }).reset_index()
        
        # Renommer les colonnes
        away_stats.columns = ['equipe_exterieur', 'buts_marques_exterieur', 'buts_encaisses_exterieur']
        
        # Calcul des victoires
        home_wins = competition_matches[competition_matches['score_domicile'] > competition_matches['score_exterieur']].groupby('equipe_domicile').size().reset_index(name='victoires_domicile')
        away_wins = competition_matches[competition_matches['score_domicile'] < competition_matches['score_exterieur']].groupby('equipe_exterieur').size().reset_index(name='victoires_exterieur')
        draws_home = competition_matches[competition_matches['score_domicile'] == competition_matches['score_exterieur']].groupby('equipe_domicile').size().reset_index(name='nuls_domicile')
        draws_away = competition_matches[competition_matches['score_domicile'] == competition_matches['score_exterieur']].groupby('equipe_exterieur').size().reset_index(name='nuls_exterieur')
        
        # Fusion des statistiques domicile et extérieur
        team_stats_competition = home_stats.merge(
            away_stats,
            left_on='equipe_domicile',
            right_on='equipe_exterieur',
            how='outer'
        )
        
        # Fusion avec les victoires et nuls
        team_stats_competition = team_stats_competition.merge(
            home_wins,
            on='equipe_domicile',
            how='left'
        )
        team_stats_competition = team_stats_competition.merge(
            away_wins,
            on='equipe_exterieur',
            how='left'
        )
        team_stats_competition = team_stats_competition.merge(
            draws_home,
            on='equipe_domicile',
            how='left'
        )
        team_stats_competition = team_stats_competition.merge(
            draws_away,
            on='equipe_exterieur',
            how='left'
        )
        
        # Remplacement des NaN par 0
        team_stats_competition = team_stats_competition.fillna(0)
        
        # Calcul des nuls totaux
        team_stats_competition['nuls'] = team_stats_competition['nuls_domicile'] + team_stats_competition['nuls_exterieur']
        
        # Utiliser equipe_domicile comme nom d'équipe final
        team_stats_competition['equipe'] = team_stats_competition['equipe_domicile'].combine_first(team_stats_competition['equipe_exterieur'])
        
        # Calcul des points par match
        team_stats_competition['points_par_match'] = (
            (team_stats_competition['victoires_domicile'] + team_stats_competition['victoires_exterieur']) * 3 +
            team_stats_competition['nuls']
        ) / team_stats_competition['matchs_joues']
        
        # Sélection des colonnes finales
        final_columns = [
            'equipe',
            'competition',
            'buts_marques_domicile',
            'buts_marques_exterieur',
            'buts_encaisses_domicile',
            'buts_encaisses_exterieur',
            'matchs_joues',
            'victoires_domicile',
            'victoires_exterieur',
            'nuls',
            'points_par_match'
        ]
        team_stats_competition = team_stats_competition[final_columns]
        
        team_stats.append(team_stats_competition)
    
    # Concaténation de toutes les statistiques
    return pd.concat(team_stats, ignore_index=True)

def main():
    """Fonction principale"""
    # Chargement des données
    data_dir = project_root.parent / 'FIP_DB'
    data_dir.mkdir(exist_ok=True)
    
    # Chargement et préparation des données des matchs
    matches_df = load_all_matches()
    
    # Standardisation des codes de compétition
    competition_mapping = {
        'de.1': 'de.1',  # Bundesliga
        'de.2': 'de.2',
        'de.3': 'de.3',
        'en.1': 'en.1',  # Premier League
        'en.2': 'en.2',
        'en.3': 'en.3',
        'en.4': 'en.4',
        'en.5': 'en.5',
        'eng.1': 'en.1',
        'eng.2': 'en.2',
        'eng.3': 'en.3',
        'eng.4': 'en.4',
        'eng.5': 'en.5',
        'eng.cup': 'en.cup',
        'es.1': 'es.1',  # La Liga
        'es.2': 'es.2',
        '0': 'unknown'
    }
    matches_df['competition'] = matches_df['competition'].map(competition_mapping)
    
    # Filtrer pour ne garder que les matchs des premières divisions
    matches_df = matches_df[matches_df['competition'].isin(['de.1', 'en.1', 'es.1'])]
    
    print(f"\nTotal des matchs après filtrage: {len(matches_df)}")
    print("\nCalcul des statistiques par équipe...")
    
    # Préparation des statistiques des équipes
    team_stats_df = prepare_team_stats(matches_df)
    
    # Sauvegarde des fichiers
    print("\nSauvegarde des données...")
    matches_df.to_csv(data_dir / 'matchs_data.csv', index=False)
    team_stats_df.to_csv(data_dir / 'equipes_data.csv', index=False)
    
    print("\nPréparation des données terminée!")
    print(f"Fichiers sauvegardés dans {data_dir}")

def load_all_matches():
    """Charge tous les matchs des différentes sources"""
    matches = []
    
    # Chargement des données de la Bundesliga
    print("Traitement de deutschland-master...")
    bundesliga_dir = project_root.parent.parent / 'DATASETS' / 'deutschland-master' / 'deutschland-master'
    matches.extend(load_matches_from_directory(bundesliga_dir, 'de.1'))
    
    # Chargement des données de la Premier League
    print("Traitement de england-master...")
    england_dir = project_root.parent.parent / 'DATASETS' / 'england-master' / 'england-master'
    matches.extend(load_matches_from_directory(england_dir, 'en.1'))
    
    # Chargement des données de la Liga
    print("Traitement de espana-master...")
    spain_dir = project_root.parent.parent / 'DATASETS' / 'espana-master' / 'espana-master'
    matches.extend(load_matches_from_directory(spain_dir, 'es.1'))
    
    # Création du DataFrame
    matches_df = pd.DataFrame(matches)
    
    print(f"\nTotal des matchs: {len(matches_df)}")
    print("\nCalcul des statistiques par équipe...")
    
    return matches_df

def load_matches_from_directory(directory, competition_code):
    """Charge les matchs d'un répertoire"""
    matches = []
    
    # Parcours des dossiers par décennie
    for decade_dir in sorted(directory.glob('[0-9]*s')):
        # Parcours des dossiers par saison
        for season_dir in sorted(decade_dir.glob('[0-9]*-*')):
            season = season_dir.name
            
            # Parcours des fichiers CSV
            for csv_file in season_dir.glob('*.csv'):
                try:
                    # Lecture du fichier CSV
                    df = pd.read_csv(csv_file, encoding='utf-8')
                    
                    # Vérification du format du fichier
                    if not all(col in df.columns for col in ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']):
                        continue
                    
                    # Extraction des matchs
                    for _, row in df.iterrows():
                        match = {
                            'date': row['Date'],
                            'equipe_domicile': row['HomeTeam'],
                            'equipe_exterieur': row['AwayTeam'],
                            'score_domicile': row['FTHG'],
                            'score_exterieur': row['FTAG'],
                            'competition': competition_code,
                            'saison': season
                        }
                        matches.append(match)
                    
                    print(f"  - Saison {season}: {len(df)} matchs")
                    
                except Exception as e:
                    print(f"Erreur lors du traitement de {csv_file}: {e}")
    
    return matches

if __name__ == "__main__":
    main() 