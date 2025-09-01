"""
Script pour déplacer et renommer les images des compétitions
"""
import os
import shutil
from pathlib import Path

def main():
    """Fonction principale"""
    project_dir = Path(__file__).parent.parent
    source_dir = project_dir / 'templates' / 'images'
    target_dir = project_dir / 'static' / 'img'
    
    # Créer les dossiers nécessaires
    competitions_dir = target_dir / 'competitions'
    competitions_dir.mkdir(parents=True, exist_ok=True)
    
    # Mapping des noms de fichiers
    competition_images = {
        'champions_league.webp': 'champions-league.png',
        'premier_league.webp': 'premier-league.png',
        'laliga.webp': 'laliga.png',
        'bundesliga.webp': 'bundesliga.png',
        'seriea.webp': 'serie-a.png',
        'ligue1.webp': 'ligue-1.png',
        'coupe_du_monde.webp': 'world-cup.png',
        'euro.webp': 'euro.png',
        'copa_america.webp': 'copa-america.png'
    }
    
    # Copier et renommer les images des compétitions
    for src_name, dst_name in competition_images.items():
        src_path = source_dir / src_name
        dst_path = competitions_dir / dst_name
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"Copié {src_name} vers {dst_name}")
    
    # Copier le logo du site
    logo_src = source_dir / 'Logo.jpg'
    if logo_src.exists():
        shutil.copy2(logo_src, target_dir / 'logo.png')
        print("Logo du site copié")

if __name__ == '__main__':
    main() 