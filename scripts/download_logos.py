"""
Script pour télécharger les logos des compétitions
"""
import os
import requests
from pathlib import Path

# URLs des logos (à remplacer par les vraies URLs)
COMPETITION_LOGOS = {
    'champions-league': 'https://example.com/champions-league.png',
    'premier-league': 'https://example.com/premier-league.png',
    'laliga': 'https://example.com/laliga.png',
    'bundesliga': 'https://example.com/bundesliga.png',
    'serie-a': 'https://example.com/serie-a.png',
    'ligue-1': 'https://example.com/ligue-1.png',
    'world-cup': 'https://example.com/world-cup.png',
    'euro': 'https://example.com/euro.png',
    'copa-america': 'https://example.com/copa-america.png'
}

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
    # Créer le dossier des logos s'il n'existe pas
    logo_dir = Path(__file__).parent.parent / 'static' / 'img' / 'competitions'
    logo_dir.mkdir(parents=True, exist_ok=True)
    
    # Télécharger chaque logo
    for comp_id, url in COMPETITION_LOGOS.items():
        filename = logo_dir / f"{comp_id}.png"
        download_logo(url, filename)

if __name__ == '__main__':
    main() 