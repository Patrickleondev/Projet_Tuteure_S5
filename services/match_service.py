"""
Service de gestion des matchs et prédictions
"""
from utils.stats_calculator import predict_match_stats
from utils.league_selector import get_matches_data
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class MatchService:
    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_DATA_API_KEY')
        self.base_url = 'https://api.football-data.org/v4'
        self.competitions = {
            'CL': 'CL',    # Champions League
            'PL': 'PL',    # Premier League
            'BL1': 'BL1',  # Bundesliga
            'SA': 'SA',    # Serie A
            'PD': 'PD',    # La Liga
            'FL1': 'FL1',  # Ligue 1
        }

    def get_upcoming_matches(self, competition_id='all'):
        """Récupère les matchs à venir pour une compétition donnée"""
        try:
            # Si 'all', récupérer les matchs de toutes les compétitions
            if competition_id == 'all':
                all_matches = []
                for comp_id in self.competitions.values():
                    matches = self._get_matches_for_competition(comp_id)
                    all_matches.extend(matches)
                return all_matches
            else:
                return self._get_matches_for_competition(competition_id)
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs: {str(e)}")
            return []

    def _get_matches_for_competition(self, competition_id):
        """Récupère les matchs pour une compétition spécifique"""
        try:
            # Calculer la date de début (aujourd'hui) et la date de fin (dans 30 jours)
            today = datetime.now().strftime('%Y-%m-%d')
            end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            url = f"{self.base_url}/competitions/{competition_id}/matches"
            headers = {'X-Auth-Token': self.api_key}
            params = {
                'dateFrom': today,
                'dateTo': end_date,
                'status': 'SCHEDULED'
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            matches = []
            for match in data['matches']:
                matches.append({
                    'id': match['id'],
                    'competition': match['competition']['name'],
                    'competition_id': competition_id,
                    'home_team': match['homeTeam']['name'],
                    'home_team_id': match['homeTeam']['id'],
                    'home_team_logo': f"/static/img/teams/{match['homeTeam']['id']}.png",
                    'away_team': match['awayTeam']['name'],
                    'away_team_id': match['awayTeam']['id'],
                    'away_team_logo': f"/static/img/teams/{match['awayTeam']['id']}.png",
                    'date': match['utcDate'],
                    'status': match['status'],
                    'stage': match['stage'],
                    'group': match.get('group', None)
                })
            return matches
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs pour {competition_id}: {str(e)}")
            return []

    def get_match_details(self, match_id):
        """Récupère les détails d'un match spécifique"""
        try:
            url = f"{self.base_url}/matches/{match_id}"
            headers = {'X-Auth-Token': self.api_key}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            match = response.json()
            
            return {
                'id': match['id'],
                'competition': match['competition']['name'],
                'home_team': match['homeTeam']['name'],
                'home_team_id': match['homeTeam']['id'],
                'home_team_logo': f"/static/img/teams/{match['homeTeam']['id']}.png",
                'away_team': match['awayTeam']['name'],
                'away_team_id': match['awayTeam']['id'],
                'away_team_logo': f"/static/img/teams/{match['awayTeam']['id']}.png",
                'date': match['utcDate'],
                'status': match['status'],
                'stage': match['stage'],
                'group': match.get('group', None),
                'odds': match.get('odds', None)
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération des détails du match {match_id}: {str(e)}")
            return None

def get_match_predictions(team1: str, team2: str):
    """Obtient les prédictions pour un match"""
    try:
        # Validation des équipes
        if not team1 or not team2:
            raise ValueError("Les noms des équipes sont requis")

        if team1 == team2:
            raise ValueError("Les équipes doivent être différentes")

        # Récupération des données historiques
        matches_data, league = get_matches_data(team1, team2)
        
        # Calcul des prédictions
        predictions, accuracy = predict_match_stats(matches_data, team1, team2)
        
        return {
            'status': 'success',
            'predictions': predictions,
            'accuracy': accuracy
        }
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(f"Erreur lors de la prédiction: {str(e)}")