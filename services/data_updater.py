"""
Service de mise à jour des données en temps réel
"""
import requests
from datetime import datetime, timedelta
import os

def get_football_api_key():
    return os.getenv('FOOTBALL_API_KEY', 'a94df8a9e61045e1988098eeece5a492')

def update_match_data():
    """Met à jour les données des matchs en temps réel"""
    api_key = get_football_api_key()
    headers = {'X-Auth-Token': api_key}
    
    # API Football-data.org pour les matchs à venir
    base_url = 'https://api.football-data.org/v4/matches'
    
    # Dates pour les 7 prochains jours
    today = datetime.now()
    next_week = today + timedelta(days=7)
    
    params = {
        'dateFrom': today.strftime('%Y-%m-%d'),
        'dateTo': next_week.strftime('%Y-%m-%d'),
        'status': 'SCHEDULED'
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            matches = response.json().get('matches', [])
            return format_upcoming_matches(matches)
    except Exception as e:
        print(f"Erreur lors de la mise à jour des matchs: {e}")
        return []

def format_upcoming_matches(matches):
    """Formate les matchs pour l'affichage"""
    formatted_matches = []
    for match in matches:
        formatted_matches.append({
            'competition': match.get('competition', {}).get('name', ''),
            'date': match.get('utcDate', ''),
            'homeTeam': match.get('homeTeam', {}).get('name', ''),
            'awayTeam': match.get('awayTeam', {}).get('name', ''),
            'status': match.get('status', '')
        })
    return formatted_matches