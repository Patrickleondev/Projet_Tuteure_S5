"""
Script pour télécharger les logos des équipes depuis football-data.org
"""
import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = Path(__file__).parent.parent / '.env'
print(f"Recherche du fichier .env dans : {env_path}")
load_dotenv(env_path)

# Clé API football-data.org
API_KEY = os.getenv('FOOTBALL_DATA_API_KEY')
if not API_KEY:
    raise ValueError("Erreur: La clé API FOOTBALL_DATA_API_KEY n'est pas définie dans le fichier .env")
else:
    print("Clé API trouvée !")

def get_competition_teams(competition_id):
    """Récupère les équipes d'une compétition depuis l'API"""
    url = f'https://api.football-data.org/v4/competitions/{competition_id}/teams'
    headers = {'X-Auth-Token': API_KEY}
    
    try:
        print(f"\nRécupération des équipes pour la compétition {competition_id}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        teams = response.json()['teams']
        print(f"Nombre d'équipes trouvées : {len(teams)}")
        return teams
    except Exception as e:
        print(f"Erreur lors de la récupération des équipes pour la compétition {competition_id}: {str(e)}")
        return []

def download_logo(url, filename):
    """Télécharge un logo depuis l'URL donnée"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
            
        print(f"Logo téléchargé avec succès: {filename}")
        
    except Exception as e:
        print(f"Erreur lors du téléchargement de {filename}: {str(e)}")

def main():
    """Fonction principale"""
    # Créer les dossiers pour les logos s'ils n'existent pas
    project_dir = Path(__file__).parent.parent
    logos_dir = project_dir / 'static' / 'img' / 'teams'
    print(f"\nCréation du dossier logos : {logos_dir}")
    logos_dir.mkdir(parents=True, exist_ok=True)
    
    # Dictionnaire des compétitions avec leurs IDs football-data.org
    competitions = {
        'CL': 'CL',    # Champions League
        'PL': 'PL',    # Premier League
        'BL1': 'BL1',  # Bundesliga
        'SA': 'SA',    # Serie A
        'PD': 'PD',    # La Liga
        'FL1': 'FL1',  # Ligue 1
    }
    
    # Télécharger les logos pour chaque compétition
    for comp_code, comp_id in competitions.items():
        print(f"\nRécupération des logos pour {comp_code}...")
        teams = get_competition_teams(comp_id)
        
        for team in teams:
            team_id = team['id']
            team_name = team['name']
            logo_url = team.get('crest')  # Dans l'API v4, c'est 'crest' au lieu de 'crestUrl'
            
            if logo_url:
                # Nettoyer le nom de l'équipe pour le nom de fichier
                filename = logos_dir / f"{team_id}.png"
                
                # Télécharger le logo
                download_logo(logo_url, filename)
                
                # Créer un fichier de mapping des IDs aux noms
                with open(logos_dir / 'team_mapping.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{team_id},{team_name},{comp_code}\n")

if __name__ == '__main__':
    main() 