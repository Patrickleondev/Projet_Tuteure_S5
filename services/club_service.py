"""
Service pour gérer les informations des clubs
"""
import pandas as pd
from pathlib import Path
import os

class ClubService:
    def __init__(self):
        self.clubs = {}
        self.team_mapping = self._load_team_mapping()
        self.load_clubs()
    
    def _load_team_mapping(self):
        """Charge le mapping entre les noms d'équipes et les IDs d'images"""
        mapping = {}
        try:
            mapping_file = Path(__file__).parent.parent / 'static' / 'img' / 'teams' / 'team_mapping.txt'
            with open(mapping_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        team_id, team_name = parts[0], parts[1]
                        mapping[team_name] = team_id
        except Exception as e:
            print(f"Erreur lors du chargement du mapping des équipes: {str(e)}")
        return mapping
    
    def load_clubs(self):
        """Charge les informations des clubs depuis les fichiers CSV"""
        try:
            # Chemin vers les fichiers de données
            data_dir = Path(__file__).parent.parent.parent.parent / 'FIP_DB'
            
            # Charger les données des équipes
            equipes_df = pd.read_csv(data_dir / 'equipes_data.csv')
            equipes_par_championnat_df = pd.read_csv(data_dir / 'equipes_par_championnat.csv')
            
            # Fusionner les données
            self.clubs_df = pd.merge(
                equipes_df,
                equipes_par_championnat_df,
                left_on='Équipe',
                right_on='Équipe',
                how='inner'
            )
            
        except Exception as e:
            print(f"Erreur lors du chargement des clubs: {str(e)}")
            self.clubs_df = pd.DataFrame()
    
    def get_clubs_by_competition(self, competition_id):
        """Récupère les clubs d'une compétition donnée"""
        try:
            if competition_id == 'all':
                clubs = self.clubs_df
            else:
                clubs = self.clubs_df[self.clubs_df['Championnat'] == competition_id]
            result = []
            for _, row in clubs.iterrows():
                team_id = self.team_mapping.get(row['Équipe'])
                logo_path = f'static/img/teams/{team_id}.png' if team_id else None
                if team_id and os.path.exists(logo_path):
                    logo = f'/static/img/teams/{team_id}.png'
                else:
                    logo = '/static/img/teams/default-team.svg'
                result.append({
                    'id': row['Équipe'],
                    'name': row['Équipe'],
                    'logo': logo,
                    'competition': row['Championnat'],
                    'ranking': row['Classement'] if 'Classement' in row else None,
                    'points': row['Points'] if 'Points' in row else None,
                    'form': self.get_team_form(row['Équipe']),
                    'stats': {
                        'matches_played': row['Matchs_joués'] if 'Matchs_joués' in row else 0,
                        'wins': row['Victoires'] if 'Victoires' in row else 0,
                        'draws': row['Nuls'] if 'Nuls' in row else 0,
                        'losses': row['Défaites'] if 'Défaites' in row else 0,
                        'goals_for': row['Buts_marqués'] if 'Buts_marqués' in row else 0,
                        'goals_against': row['Buts_encaissés'] if 'Buts_encaissés' in row else 0
                    }
                })
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des clubs: {str(e)}")
            return []
    
    def get_team_form(self, team_name):
        """Récupère la forme récente d'une équipe"""
        try:
            # Ici vous pouvez implémenter la logique pour récupérer
            # les 5 derniers résultats de l'équipe
            # Pour l'instant, on retourne une forme par défaut
            return "WDLWW"
        except Exception as e:
            print(f"Erreur lors de la récupération de la forme de l'équipe: {str(e)}")
            return "DDDDD"
    
    def get_team_details(self, team_id):
        """Récupère les détails d'une équipe spécifique"""
        try:
            team = self.clubs_df[self.clubs_df['Équipe'] == team_id].iloc[0]
            
            return {
                'id': team['Équipe'],
                'name': team['Équipe'],
                'logo': f"/static/img/teams/{team['Équipe'].lower().replace(' ', '-')}.png",
                'competition': team['Championnat'],
                'ranking': team['Classement'] if 'Classement' in team else None,
                'points': team['Points'] if 'Points' in team else None,
                'form': self.get_team_form(team['Équipe']),
                'stats': {
                    'matches_played': team['Matchs_joués'] if 'Matchs_joués' in team else 0,
                    'wins': team['Victoires'] if 'Victoires' in team else 0,
                    'draws': team['Nuls'] if 'Nuls' in team else 0,
                    'losses': team['Défaites'] if 'Défaites' in team else 0,
                    'goals_for': team['Buts_marqués'] if 'Buts_marqués' in team else 0,
                    'goals_against': team['Buts_encaissés'] if 'Buts_encaissés' in team else 0
                }
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération des détails de l'équipe: {str(e)}")
            return None 