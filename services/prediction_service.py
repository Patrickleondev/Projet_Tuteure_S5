"""
Service de prédiction des matchs
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import json
import os
from datetime import datetime, timedelta
import random
import unicodedata

from models.match_predictor import FootballMatchPredictor
from services.regression_service import RegressionPredictionService
from models.hybrid_model import HybridModel

class PredictionService:
    def __init__(self):
        self.model = None
        self.regression_service = RegressionPredictionService()
        self.load_model()
        self.competitions = self._load_competitions()
        self.teams = self._load_teams()
        
        # Charger les modèles
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        self.regression_model = joblib.load(os.path.join(models_dir, 'football_predictor.pkl'))
        
        # Tentative de chargement du modèle hybride
        hybrid_model_path = os.path.join(models_dir, 'hybrid_model.pkl')
        try:
            # Vérifier d'abord si TensorFlow est disponible
            try:
                import tensorflow
                self.hybrid_model = joblib.load(hybrid_model_path)
                print("Modèle hybride chargé avec succès.")
            except ImportError:
                print("TensorFlow non disponible. Création d'un nouveau modèle hybride sans réseau de neurones...")
                self.hybrid_model = HybridModel()
                print("Nouveau modèle hybride créé (GradientBoosting uniquement).")
        except FileNotFoundError:
            print("Modèle hybride non trouvé. Création d'un nouveau modèle...")
            self.hybrid_model = HybridModel()
            # Entraîner le modèle si nécessaire
            # self.hybrid_model.train(data)  # Décommenter et implémenter si nécessaire
            # Sauvegarder le nouveau modèle (uniquement si TensorFlow est disponible)
            try:
                import tensorflow
                joblib.dump(self.hybrid_model, hybrid_model_path)
                print("Nouveau modèle hybride créé et sauvegardé.")
            except ImportError:
                print("Nouveau modèle hybride créé (sauvegarde ignorée car TensorFlow n'est pas disponible).")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle hybride: {str(e)}")
            print("Création d'un nouveau modèle hybride...")
            self.hybrid_model = HybridModel()
        
        # Charger les données des équipes
        self.teams_data = self._load_teams_data()
    
    def _load_competitions(self):
        """Chargement des compétitions disponibles"""
        competitions = {
            'clubs': {
                'name': 'Clubs',
                'competitions': [
                    {
                        'id': 'cl',
                        'name': 'UEFA Champions League',
                        'logo': '/static/img/competitions/champions-league.png'
                    },
                    {
                        'id': 'en.1',
                        'name': 'Premier League',
                        'logo': '/static/img/competitions/premier-league.png'
                    },
                    {
                        'id': 'es.1',
                        'name': 'La Liga',
                        'logo': '/static/img/competitions/laliga.png'
                    },
                    {
                        'id': 'de.1',
                        'name': 'Bundesliga',
                        'logo': '/static/img/competitions/bundesliga.png'
                    },
                    {
                        'id': 'it.1',
                        'name': 'Serie A',
                        'logo': '/static/img/competitions/serie-a.png'
                    },
                    {
                        'id': 'fr.1',
                        'name': 'Ligue 1',
                        'logo': '/static/img/competitions/ligue-1.png'
                    }
                ]
            },
            'nations': {
                'name': 'Nations',
                'competitions': [
                    {
                        'id': 'world_cup',
                        'name': 'Coupe du Monde FIFA',
                        'logo': '/static/img/competitions/world-cup.png'
                    },
                    {
                        'id': 'euro',
                        'name': 'UEFA Euro',
                        'logo': '/static/img/competitions/euro.png'
                    },
                    {
                        'id': 'copa_america',
                        'name': 'Copa América',
                        'logo': '/static/img/competitions/copa-america.png'
                    }
                ]
            }
        }
        return competitions

    def _load_teams(self):
        """Chargement des équipes par compétition"""
        teams = {
            'cl': [  # Champions League - 40 équipes
                # Angleterre
                {'id': 'manchester-city', 'name': 'Manchester City', 'country': 'Angleterre'},
                {'id': 'manchester-united', 'name': 'Manchester United', 'country': 'Angleterre'},
                {'id': 'liverpool', 'name': 'Liverpool', 'country': 'Angleterre'},
                {'id': 'chelsea', 'name': 'Chelsea', 'country': 'Angleterre'},
                {'id': 'arsenal', 'name': 'Arsenal', 'country': 'Angleterre'},
                {'id': 'tottenham', 'name': 'Tottenham', 'country': 'Angleterre'},
                # Espagne
                {'id': 'real-madrid', 'name': 'Real Madrid', 'country': 'Espagne'},
                {'id': 'barcelona', 'name': 'Barcelona', 'country': 'Espagne'},
                {'id': 'atletico-madrid', 'name': 'Atlético Madrid', 'country': 'Espagne'},
                {'id': 'sevilla', 'name': 'Sevilla', 'country': 'Espagne'},
                {'id': 'valencia', 'name': 'Valencia', 'country': 'Espagne'},
                {'id': 'villarreal', 'name': 'Villarreal', 'country': 'Espagne'},
                # Allemagne
                {'id': 'bayern-munich', 'name': 'Bayern Munich', 'country': 'Allemagne'},
                {'id': 'borussia-dortmund', 'name': 'Borussia Dortmund', 'country': 'Allemagne'},
                {'id': 'rb-leipzig', 'name': 'RB Leipzig', 'country': 'Allemagne'},
                {'id': 'bayer-leverkusen', 'name': 'Bayer Leverkusen', 'country': 'Allemagne'},
                # Italie
                {'id': 'juventus', 'name': 'Juventus', 'country': 'Italie'},
                {'id': 'inter-milan', 'name': 'Inter Milan', 'country': 'Italie'},
                {'id': 'ac-milan', 'name': 'AC Milan', 'country': 'Italie'},
                {'id': 'napoli', 'name': 'Napoli', 'country': 'Italie'},
                {'id': 'roma', 'name': 'AS Roma', 'country': 'Italie'},
                {'id': 'lazio', 'name': 'Lazio', 'country': 'Italie'},
                # France
                {'id': 'psg', 'name': 'Paris Saint-Germain', 'country': 'France'},
                {'id': 'marseille', 'name': 'Olympique de Marseille', 'country': 'France'},
                {'id': 'lyon', 'name': 'Olympique Lyonnais', 'country': 'France'},
                {'id': 'monaco', 'name': 'AS Monaco', 'country': 'France'},
                # Portugal
                {'id': 'porto', 'name': 'FC Porto', 'country': 'Portugal'},
                {'id': 'benfica', 'name': 'Benfica', 'country': 'Portugal'},
                {'id': 'sporting-cp', 'name': 'Sporting CP', 'country': 'Portugal'},
                # Pays-Bas
                {'id': 'ajax', 'name': 'Ajax', 'country': 'Pays-Bas'},
                {'id': 'psv', 'name': 'PSV Eindhoven', 'country': 'Pays-Bas'},
                {'id': 'feyenoord', 'name': 'Feyenoord', 'country': 'Pays-Bas'},
                # Autres
                {'id': 'salzburg', 'name': 'RB Salzburg', 'country': 'Autriche'},
                {'id': 'shakhtar', 'name': 'Shakhtar Donetsk', 'country': 'Ukraine'},
                {'id': 'zenit', 'name': 'Zenit St. Petersburg', 'country': 'Russie'},
                {'id': 'porto', 'name': 'FC Porto', 'country': 'Portugal'},
                {'id': 'ajax', 'name': 'Ajax', 'country': 'Pays-Bas'},
                {'id': 'club-brugge', 'name': 'Club Brugge', 'country': 'Belgique'},
                {'id': 'galatasaray', 'name': 'Galatasaray', 'country': 'Turquie'},
                {'id': 'celtic', 'name': 'Celtic', 'country': 'Écosse'}
            ],
            'en.1': [  # Premier League - 20 équipes
                {'id': 'manchester-city', 'name': 'Manchester City'},
                {'id': 'manchester-united', 'name': 'Manchester United'},
                {'id': 'liverpool', 'name': 'Liverpool'},
                {'id': 'chelsea', 'name': 'Chelsea'},
                {'id': 'arsenal', 'name': 'Arsenal'},
                {'id': 'tottenham', 'name': 'Tottenham'},
                {'id': 'west-ham', 'name': 'West Ham'},
                {'id': 'leicester', 'name': 'Leicester City'},
                {'id': 'everton', 'name': 'Everton'},
                {'id': 'aston-villa', 'name': 'Aston Villa'},
                {'id': 'newcastle', 'name': 'Newcastle United'},
                {'id': 'wolves', 'name': 'Wolverhampton'},
                {'id': 'crystal-palace', 'name': 'Crystal Palace'},
                {'id': 'brighton', 'name': 'Brighton'},
                {'id': 'southampton', 'name': 'Southampton'},
                {'id': 'brentford', 'name': 'Brentford'},
                {'id': 'leeds', 'name': 'Leeds United'},
                {'id': 'burnley', 'name': 'Burnley'},
                {'id': 'watford', 'name': 'Watford'},
                {'id': 'norwich', 'name': 'Norwich City'}
            ],
            'es.1': [  # La Liga - 20 équipes
                {'id': 'real-madrid', 'name': 'Real Madrid'},
                {'id': 'barcelona', 'name': 'Barcelona'},
                {'id': 'atletico-madrid', 'name': 'Atlético Madrid'},
                {'id': 'sevilla', 'name': 'Sevilla'},
                {'id': 'real-betis', 'name': 'Real Betis'},
                {'id': 'real-sociedad', 'name': 'Real Sociedad'},
                {'id': 'villarreal', 'name': 'Villarreal'},
                {'id': 'athletic-bilbao', 'name': 'Athletic Bilbao'},
                {'id': 'valencia', 'name': 'Valencia'},
                {'id': 'osasuna', 'name': 'Osasuna'},
                {'id': 'celta-vigo', 'name': 'Celta Vigo'},
                {'id': 'espanyol', 'name': 'Espanyol'},
                {'id': 'rayo-vallecano', 'name': 'Rayo Vallecano'},
                {'id': 'elche', 'name': 'Elche'},
                {'id': 'getafe', 'name': 'Getafe'},
                {'id': 'mallorca', 'name': 'Mallorca'},
                {'id': 'cadiz', 'name': 'Cádiz'},
                {'id': 'granada', 'name': 'Granada'},
                {'id': 'levante', 'name': 'Levante'},
                {'id': 'alaves', 'name': 'Alavés'}
            ],
            'de.1': [  # Bundesliga - 20 équipes
                {'id': 'bayern-munich', 'name': 'Bayern Munich'},
                {'id': 'borussia-dortmund', 'name': 'Borussia Dortmund'},
                {'id': 'rb-leipzig', 'name': 'RB Leipzig'},
                {'id': 'bayer-leverkusen', 'name': 'Bayer Leverkusen'},
                {'id': 'hoffenheim', 'name': 'Hoffenheim'},
                {'id': 'freiburg', 'name': 'SC Freiburg'},
                {'id': 'union-berlin', 'name': 'Union Berlin'},
                {'id': 'koln', 'name': 'FC Köln'},
                {'id': 'mainz', 'name': 'Mainz 05'},
                {'id': 'monchengladbach', 'name': 'Borussia Mönchengladbach'},
                {'id': 'eintracht-frankfurt', 'name': 'Eintracht Frankfurt'},
                {'id': 'wolfsburg', 'name': 'VfL Wolfsburg'},
                {'id': 'bochum', 'name': 'VfL Bochum'},
                {'id': 'augsburg', 'name': 'FC Augsburg'},
                {'id': 'stuttgart', 'name': 'VfB Stuttgart'},
                {'id': 'hertha', 'name': 'Hertha BSC'},
                {'id': 'arminia', 'name': 'Arminia Bielefeld'},
                {'id': 'greuther-furth', 'name': 'Greuther Fürth'},
                {'id': 'schalke', 'name': 'Schalke 04'},
                {'id': 'werder-bremen', 'name': 'Werder Bremen'}
            ],
            'it.1': [  # Serie A - 20 équipes
                {'id': 'inter-milan', 'name': 'Inter Milan'},
                {'id': 'ac-milan', 'name': 'AC Milan'},
                {'id': 'napoli', 'name': 'Napoli'},
                {'id': 'juventus', 'name': 'Juventus'},
                {'id': 'roma', 'name': 'AS Roma'},
                {'id': 'lazio', 'name': 'Lazio'},
                {'id': 'atalanta', 'name': 'Atalanta'},
                {'id': 'fiorentina', 'name': 'Fiorentina'},
                {'id': 'verona', 'name': 'Hellas Verona'},
                {'id': 'torino', 'name': 'Torino'},
                {'id': 'sassuolo', 'name': 'Sassuolo'},
                {'id': 'udinese', 'name': 'Udinese'},
                {'id': 'bologna', 'name': 'Bologna'},
                {'id': 'empoli', 'name': 'Empoli'},
                {'id': 'sampdoria', 'name': 'Sampdoria'},
                {'id': 'spezia', 'name': 'Spezia'},
                {'id': 'cagliari', 'name': 'Cagliari'},
                {'id': 'venezia', 'name': 'Venezia'},
                {'id': 'genoa', 'name': 'Genoa'},
                {'id': 'salernitana', 'name': 'Salernitana'}
            ],
            'fr.1': [  # Ligue 1 - 20 équipes
                {'id': 'psg', 'name': 'Paris Saint-Germain'},
                {'id': 'marseille', 'name': 'Olympique de Marseille'},
                {'id': 'lyon', 'name': 'Olympique Lyonnais'},
                {'id': 'monaco', 'name': 'AS Monaco'},
                {'id': 'nice', 'name': 'OGC Nice'},
                {'id': 'rennes', 'name': 'Stade Rennais'},
                {'id': 'strasbourg', 'name': 'RC Strasbourg'},
                {'id': 'lens', 'name': 'RC Lens'},
                {'id': 'lille', 'name': 'LOSC Lille'},
                {'id': 'nantes', 'name': 'FC Nantes'},
                {'id': 'montpellier', 'name': 'Montpellier'},
                {'id': 'brest', 'name': 'Stade Brestois'},
                {'id': 'reims', 'name': 'Stade de Reims'},
                {'id': 'angers', 'name': 'Angers SCO'},
                {'id': 'troyes', 'name': 'ESTAC Troyes'},
                {'id': 'clermont', 'name': 'Clermont Foot'},
                {'id': 'lorient', 'name': 'FC Lorient'},
                {'id': 'saint-etienne', 'name': 'AS Saint-Étienne'},
                {'id': 'metz', 'name': 'FC Metz'},
                {'id': 'bordeaux', 'name': 'Girondins de Bordeaux'}
            ],
            'world_cup': [  # Coupe du Monde - 32 équipes
                # Europe
                {'id': 'france', 'name': 'France'},
                {'id': 'germany', 'name': 'Allemagne'},
                {'id': 'england', 'name': 'Angleterre'},
                {'id': 'spain', 'name': 'Espagne'},
                {'id': 'portugal', 'name': 'Portugal'},
                {'id': 'belgium', 'name': 'Belgique'},
                {'id': 'netherlands', 'name': 'Pays-Bas'},
                {'id': 'italy', 'name': 'Italie'},
                {'id': 'croatia', 'name': 'Croatie'},
                {'id': 'denmark', 'name': 'Danemark'},
                {'id': 'switzerland', 'name': 'Suisse'},
                {'id': 'poland', 'name': 'Pologne'},
                # Amérique du Sud
                {'id': 'brazil', 'name': 'Brésil'},
                {'id': 'argentina', 'name': 'Argentine'},
                {'id': 'uruguay', 'name': 'Uruguay'},
                {'id': 'colombia', 'name': 'Colombie'},
                {'id': 'chile', 'name': 'Chili'},
                # Afrique
                {'id': 'senegal', 'name': 'Sénégal'},
                {'id': 'morocco', 'name': 'Maroc'},
                {'id': 'tunisia', 'name': 'Tunisie'},
                {'id': 'cameroon', 'name': 'Cameroun'},
                {'id': 'ghana', 'name': 'Ghana'},
                # Asie
                {'id': 'japan', 'name': 'Japon'},
                {'id': 'south-korea', 'name': 'Corée du Sud'},
                {'id': 'iran', 'name': 'Iran'},
                {'id': 'saudi-arabia', 'name': 'Arabie Saoudite'},
                {'id': 'australia', 'name': 'Australie'},
                # Amérique du Nord et Centrale
                {'id': 'mexico', 'name': 'Mexique'},
                {'id': 'usa', 'name': 'États-Unis'},
                {'id': 'canada', 'name': 'Canada'},
                {'id': 'costa-rica', 'name': 'Costa Rica'},
                {'id': 'panama', 'name': 'Panama'}
            ],
            'euro': [  # Euro - 24 équipes
                {'id': 'france', 'name': 'France'},
                {'id': 'germany', 'name': 'Allemagne'},
                {'id': 'england', 'name': 'Angleterre'},
                {'id': 'spain', 'name': 'Espagne'},
                {'id': 'portugal', 'name': 'Portugal'},
                {'id': 'belgium', 'name': 'Belgique'},
                {'id': 'netherlands', 'name': 'Pays-Bas'},
                {'id': 'italy', 'name': 'Italie'},
                {'id': 'croatia', 'name': 'Croatie'},
                {'id': 'denmark', 'name': 'Danemark'},
                {'id': 'switzerland', 'name': 'Suisse'},
                {'id': 'poland', 'name': 'Pologne'},
                {'id': 'austria', 'name': 'Autriche'},
                {'id': 'ukraine', 'name': 'Ukraine'},
                {'id': 'turkey', 'name': 'Turquie'},
                {'id': 'russia', 'name': 'Russie'},
                {'id': 'wales', 'name': 'Pays de Galles'},
                {'id': 'scotland', 'name': 'Écosse'},
                {'id': 'czech-republic', 'name': 'République Tchèque'},
                {'id': 'sweden', 'name': 'Suède'},
                {'id': 'hungary', 'name': 'Hongrie'},
                {'id': 'slovakia', 'name': 'Slovaquie'},
                {'id': 'finland', 'name': 'Finlande'},
                {'id': 'north-macedonia', 'name': 'Macédoine du Nord'}
            ],
            'copa_america': [  # Copa América - 12 équipes
                {'id': 'brazil', 'name': 'Brésil'},
                {'id': 'argentina', 'name': 'Argentine'},
                {'id': 'uruguay', 'name': 'Uruguay'},
                {'id': 'colombia', 'name': 'Colombie'},
                {'id': 'chile', 'name': 'Chili'},
                {'id': 'peru', 'name': 'Pérou'},
                {'id': 'paraguay', 'name': 'Paraguay'},
                {'id': 'ecuador', 'name': 'Équateur'},
                {'id': 'venezuela', 'name': 'Venezuela'},
                {'id': 'bolivia', 'name': 'Bolivie'},
                {'id': 'qatar', 'name': 'Qatar'},
                {'id': 'japan', 'name': 'Japon'}
            ],
            'can': [  # Coupe d'Afrique des Nations - 24 équipes
                {'id': 'senegal', 'name': 'Sénégal'},
                {'id': 'morocco', 'name': 'Maroc'},
                {'id': 'tunisia', 'name': 'Tunisie'},
                {'id': 'cameroon', 'name': 'Cameroun'},
                {'id': 'ghana', 'name': 'Ghana'},
                {'id': 'nigeria', 'name': 'Nigeria'},
                {'id': 'egypt', 'name': 'Égypte'},
                {'id': 'ivory-coast', 'name': 'Côte d\'Ivoire'},
                {'id': 'algeria', 'name': 'Algérie'},
                {'id': 'mali', 'name': 'Mali'},
                {'id': 'burkina-faso', 'name': 'Burkina Faso'},
                {'id': 'dr-congo', 'name': 'RD Congo'},
                {'id': 'south-africa', 'name': 'Afrique du Sud'},
                {'id': 'zambia', 'name': 'Zambie'},
                {'id': 'guinea', 'name': 'Guinée'},
                {'id': 'gabon', 'name': 'Gabon'},
                {'id': 'cape-verde', 'name': 'Cap-Vert'},
                {'id': 'uganda', 'name': 'Ouganda'},
                {'id': 'benin', 'name': 'Bénin'},
                {'id': 'madagascar', 'name': 'Madagascar'},
                {'id': 'mauritania', 'name': 'Mauritanie'},
                {'id': 'namibia', 'name': 'Namibie'},
                {'id': 'mozambique', 'name': 'Mozambique'},
                {'id': 'tanzania', 'name': 'Tanzanie'},
                {'id': 'togo', 'name': 'Togo'}
            ],
            'club_world_cup': [  # Coupe du Monde des Clubs - 8 équipes
                {'id': 'real-madrid', 'name': 'Real Madrid', 'country': 'Espagne'},
                {'id': 'flamengo', 'name': 'Flamengo', 'country': 'Brésil'},
                {'id': 'wydad', 'name': 'Wydad AC', 'country': 'Maroc'},
                {'id': 'seattle', 'name': 'Seattle Sounders', 'country': 'États-Unis'},
                {'id': 'al-hilal', 'name': 'Al-Hilal', 'country': 'Arabie Saoudite'},
                {'id': 'al-ahly', 'name': 'Al-Ahly', 'country': 'Égypte'},
                {'id': 'auckland-city', 'name': 'Auckland City', 'country': 'Nouvelle-Zélande'},
                {'id': 'urawa', 'name': 'Urawa Red Diamonds', 'country': 'Japon'}
            ]
        }
        
        # Ajouter les logos pour chaque équipe
        for competition in teams:
            for team in teams[competition]:
                team['logo'] = f'/static/img/teams/{team["id"]}.png'
        
        return teams

    def load_model(self):
        """Chargement du modèle"""
        try:
            self.model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'football_predictor.pkl'))
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {str(e)}")
            self.model = None
    
    def prepare_match_data(self, equipe_domicile, equipe_exterieur, type_competition='clubs', competition=None):
        """Préparation des données pour un match"""
        # Chargement des statistiques des équipes
        data_dir = Path(__file__).parent.parent.parent / 'FIP_DB'
        teams_df = pd.read_csv(data_dir / 'equipes_data.csv')
        matches_df = pd.read_csv(data_dir / 'matchs_data.csv')
        discipline_df = pd.read_csv(data_dir / 'discipline_data.csv')
        jeu_df = pd.read_csv(data_dir / 'jeu_data.csv')
        cpa_df = pd.read_csv(data_dir / 'coups_de_pied_arretes_data.csv')
        
        # Vérification de l'existence des équipes
        equipes_manquantes = []
        if not teams_df['equipe'].str.contains(equipe_domicile, case=False).any():
            equipes_manquantes.append(equipe_domicile)
        if not teams_df['equipe'].str.contains(equipe_exterieur, case=False).any():
            equipes_manquantes.append(equipe_exterieur)
            
        if equipes_manquantes:
            raise ValueError(f"Équipe(s) non trouvée(s): {' ou '.join(equipes_manquantes)}")
        
        # Récupération des statistiques des équipes avec gestion de la casse
        equipe_dom = teams_df[teams_df['equipe'].str.contains(equipe_domicile, case=False)].iloc[0]
        equipe_ext = teams_df[teams_df['equipe'].str.contains(equipe_exterieur, case=False)].iloc[0]
        
        # Statistiques de discipline avec gestion de la casse
        discipline_dom = discipline_df[discipline_df['equipe'].str.contains(equipe_domicile, case=False)].iloc[0]
        discipline_ext = discipline_df[discipline_df['equipe'].str.contains(equipe_exterieur, case=False)].iloc[0]
        
        # Statistiques de jeu avec gestion de la casse
        jeu_dom = jeu_df[jeu_df['equipe'].str.contains(equipe_domicile, case=False)].iloc[0]
        jeu_ext = jeu_df[jeu_df['equipe'].str.contains(equipe_exterieur, case=False)].iloc[0]
        
        # Statistiques de coups de pied arrêtés avec gestion de la casse
        cpa_dom = cpa_df[cpa_df['equipe'].str.contains(equipe_domicile, case=False)].iloc[0]
        cpa_ext = cpa_df[cpa_df['equipe'].str.contains(equipe_exterieur, case=False)].iloc[0]
        
        # Création du DataFrame pour la prédiction
        match_data = pd.DataFrame({
            'equipe_domicile': [equipe_domicile],
            'equipe_exterieur': [equipe_exterieur],
            'buts_marques_domicile_home': [equipe_dom['buts_marques_domicile']],
            'buts_encaisses_domicile_home': [equipe_dom['buts_encaisses_domicile']],
            'matchs_joues_home': [equipe_dom['matchs_joues']],
            'victoires_domicile_home': [equipe_dom['victoires_domicile']],
            'points_par_match_home': [equipe_dom['points_par_match']],
            'buts_marques_exterieur_away': [equipe_ext['buts_marques_exterieur']],
            'buts_encaisses_exterieur_away': [equipe_ext['buts_encaisses_exterieur']],
            'matchs_joues_away': [equipe_ext['matchs_joues']],
            'victoires_exterieur_away': [equipe_ext['victoires_exterieur']],
            'points_par_match_away': [equipe_ext['points_par_match']],
            
            # Statistiques de discipline
            'cartons_jaunes_home': [discipline_dom['cartons_jaunes']],
            'cartons_rouges_home': [discipline_dom['cartons_rouges']],
            'fautes_commises_home': [discipline_dom['fautes_commises']],
            'fautes_subies_home': [discipline_dom['fautes_subies']],
            'cartons_jaunes_away': [discipline_ext['cartons_jaunes']],
            'cartons_rouges_away': [discipline_ext['cartons_rouges']],
            'fautes_commises_away': [discipline_ext['fautes_commises']],
            'fautes_subies_away': [discipline_ext['fautes_subies']],
            
            # Statistiques de jeu
            'possession_moyenne_home': [jeu_dom['possession_moyenne']],
            'passes_reussies_home': [jeu_dom['passes_reussies']],
            'precision_passes_home': [jeu_dom['precision_passes']],
            'tirs_home': [jeu_dom['tirs']],
            'tirs_cadres_home': [jeu_dom['tirs_cadres']],
            'corners_home': [jeu_dom['corners']],
            'hors_jeu_home': [jeu_dom['hors_jeu']],
            'possession_moyenne_away': [jeu_ext['possession_moyenne']],
            'passes_reussies_away': [jeu_ext['passes_reussies']],
            'precision_passes_away': [jeu_ext['precision_passes']],
            'tirs_away': [jeu_ext['tirs']],
            'tirs_cadres_away': [jeu_ext['tirs_cadres']],
            'corners_away': [jeu_ext['corners']],
            'hors_jeu_away': [jeu_ext['hors_jeu']],
            
            # Statistiques de coups de pied arrêtés
            'penalties_marques_home': [cpa_dom['penalties_marques']],
            'penalties_concedes_home': [cpa_dom['penalties_concedes']],
            'coups_francs_marques_home': [cpa_dom['coups_francs_marques']],
            'coups_francs_concedes_home': [cpa_dom['coups_francs_concedes']],
            'penalties_marques_away': [cpa_ext['penalties_marques']],
            'penalties_concedes_away': [cpa_ext['penalties_concedes']],
            'coups_francs_marques_away': [cpa_ext['coups_francs_marques']],
            'coups_francs_concedes_away': [cpa_ext['coups_francs_concedes']]
        })
        
        # Calcul des statistiques de forme récente
        recent_matches = matches_df[
            (matches_df['equipe_domicile'].isin([equipe_domicile, equipe_exterieur])) |
            (matches_df['equipe_exterieur'].isin([equipe_domicile, equipe_exterieur]))
        ].sort_values('date').tail(10)
        
        # Forme de l'équipe à domicile
        dom_matches = recent_matches[
            (recent_matches['equipe_domicile'] == equipe_domicile) |
            (recent_matches['equipe_exterieur'] == equipe_domicile)
        ].tail(5)
        
        match_data['forme_victoires_domicile'] = [
            len(dom_matches[
                ((dom_matches['equipe_domicile'] == equipe_domicile) & (dom_matches['score_domicile'] > dom_matches['score_exterieur'])) |
                ((dom_matches['equipe_exterieur'] == equipe_domicile) & (dom_matches['score_exterieur'] > dom_matches['score_domicile']))
            ]) / len(dom_matches) if len(dom_matches) > 0 else 0
        ]
        
        match_data['forme_nuls_domicile'] = [
            len(dom_matches[dom_matches['score_domicile'] == dom_matches['score_exterieur']]) / len(dom_matches)
            if len(dom_matches) > 0 else 0
        ]
        
        match_data['forme_defaites_domicile'] = [
            len(dom_matches[
                ((dom_matches['equipe_domicile'] == equipe_domicile) & (dom_matches['score_domicile'] < dom_matches['score_exterieur'])) |
                ((dom_matches['equipe_exterieur'] == equipe_domicile) & (dom_matches['score_exterieur'] < dom_matches['score_domicile']))
            ]) / len(dom_matches) if len(dom_matches) > 0 else 0
        ]
        
        # Forme de l'équipe à l'extérieur
        ext_matches = recent_matches[
            (recent_matches['equipe_domicile'] == equipe_exterieur) |
            (recent_matches['equipe_exterieur'] == equipe_exterieur)
        ].tail(5)
        
        match_data['forme_victoires_exterieur'] = [
            len(ext_matches[
                ((ext_matches['equipe_domicile'] == equipe_exterieur) & (ext_matches['score_domicile'] > ext_matches['score_exterieur'])) |
                ((ext_matches['equipe_exterieur'] == equipe_exterieur) & (ext_matches['score_exterieur'] > ext_matches['score_domicile']))
            ]) / len(ext_matches) if len(ext_matches) > 0 else 0
        ]
        
        match_data['forme_nuls_exterieur'] = [
            len(ext_matches[ext_matches['score_domicile'] == ext_matches['score_exterieur']]) / len(ext_matches)
            if len(ext_matches) > 0 else 0
        ]
        
        match_data['forme_defaites_exterieur'] = [
            len(ext_matches[
                ((ext_matches['equipe_domicile'] == equipe_exterieur) & (ext_matches['score_domicile'] < ext_matches['score_exterieur'])) |
                ((ext_matches['equipe_exterieur'] == equipe_exterieur) & (ext_matches['score_exterieur'] < ext_matches['score_domicile']))
            ]) / len(ext_matches) if len(ext_matches) > 0 else 0
        ]
        
        # Confrontations directes
        h2h_matches = matches_df[
            (matches_df['equipe_domicile'].isin([equipe_domicile, equipe_exterieur])) &
            (matches_df['equipe_exterieur'].isin([equipe_domicile, equipe_exterieur]))
        ].sort_values('date')
        
        if len(h2h_matches) > 0:
            match_data['h2h_victoires_domicile'] = [
                len(h2h_matches[
                    (h2h_matches['equipe_domicile'] == equipe_domicile) &
                    (h2h_matches['score_domicile'] > h2h_matches['score_exterieur'])
                ]) / len(h2h_matches)
            ]
            
            match_data['h2h_victoires_exterieur'] = [
                len(h2h_matches[
                    (h2h_matches['equipe_domicile'] == equipe_exterieur) &
                    (h2h_matches['score_domicile'] > h2h_matches['score_exterieur'])
                ]) / len(h2h_matches)
            ]
            
            match_data['h2h_nuls'] = [
                len(h2h_matches[h2h_matches['score_domicile'] == h2h_matches['score_exterieur']]) / len(h2h_matches)
            ]
            
            match_data['h2h_buts_domicile'] = [
                h2h_matches[h2h_matches['equipe_domicile'] == equipe_domicile]['score_domicile'].mean()
            ]
            
            match_data['h2h_buts_exterieur'] = [
                h2h_matches[h2h_matches['equipe_exterieur'] == equipe_exterieur]['score_exterieur'].mean()
            ]
        else:
            # Si pas de confrontations directes, on utilise des valeurs par défaut
            match_data['h2h_victoires_domicile'] = [0.33]
            match_data['h2h_victoires_exterieur'] = [0.33]
            match_data['h2h_nuls'] = [0.34]
            match_data['h2h_buts_domicile'] = [1.5]
            match_data['h2h_buts_exterieur'] = [1.0]
        
        return match_data
    
    def predict_match(self, equipe_domicile, equipe_exterieur, type_competition='clubs', competition=None):
        """Prédiction du résultat d'un match avec modèle hybride"""
        # Vérification de l'existence des équipes dans le mapping
        mapping_file = os.path.join('static', 'img', 'teams', 'team_mapping.txt')
        team_mapping = {}
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        team_id, team_name, comp = parts
                        team_mapping[team_name] = team_id
        if equipe_domicile not in team_mapping or equipe_exterieur not in team_mapping:
            return {'error': f"L'une des équipes n'existe pas dans le mapping. Veuillez vérifier les noms d'équipes."}
        # Vérification de l'existence dans les données
        home_key = self._normalize_name(equipe_domicile)
        away_key = self._normalize_name(equipe_exterieur)
        if home_key not in self.teams_data or away_key not in self.teams_data:
            return {'error': f"L'une des équipes n'a pas de données disponibles pour la prédiction."}
        # Essayer d'abord le modèle de régression
        regression_result = self.regression_service.predict_match_result(equipe_domicile, equipe_exterieur)
        if regression_result:
            # Utiliser le résultat du modèle de régression
            return {
                'victoire_domicile': regression_result['probabilites']['victoire_domicile'],
                'match_nul': regression_result['probabilites']['match_nul'],
                'victoire_exterieur': regression_result['probabilites']['victoire_exterieur'],
                'equipe_domicile': equipe_domicile,
                'equipe_exterieur': equipe_exterieur,
                'buts_equipe1': regression_result['buts_equipe1'],
                'buts_equipe2': regression_result['buts_equipe2'],
                'resultat': regression_result['resultat'],
                'gagnant': regression_result['gagnant'],
                'modele_utilise': 'Régression Linéaire',
                'statistiques': {
                    'domicile': {
                        'buts_marques': regression_result['buts_equipe1'],
                        'buts_encaisses': regression_result['buts_equipe2'],
                        'victoires': 0.5,  # Valeur par défaut
                        'points_par_match': 1.5,  # Valeur par défaut
                        'forme': {
                            'victoires': 0.33,
                            'nuls': 0.33,
                            'defaites': 0.34
                        },
                        'discipline': {
                            'cartons_jaunes': regression_result['statistiques']['cartons_jaunes'],
                            'cartons_rouges': regression_result['statistiques']['cartons_rouges'],
                            'fautes_commises': regression_result['statistiques']['fautes'],
                            'fautes_subies': regression_result['statistiques']['fautes']
                        },
                        'jeu': {
                            'possession_moyenne': 55.0,
                            'passes_reussies': regression_result['statistiques']['passes_reussies_equipe1'],
                            'precision_passes': 85.0,
                            'tirs': 12.0,
                            'tirs_cadres': 5.0,
                            'corners': 6.0,
                            'hors_jeu': 2.0
                        },
                        'coups_de_pied_arretes': {
                            'penalties_marques': 0.1,
                            'penalties_concedes': 0.1,
                            'coups_francs_marques': regression_result['statistiques']['coups_francs'],
                            'coups_francs_concedes': regression_result['statistiques']['coups_francs']
                        }
                    },
                    'exterieur': {
                        'buts_marques': regression_result['buts_equipe2'],
                        'buts_encaisses': regression_result['buts_equipe1'],
                        'victoires': 0.5,  # Valeur par défaut
                        'points_par_match': 1.5,  # Valeur par défaut
                        'forme': {
                            'victoires': 0.33,
                            'nuls': 0.33,
                            'defaites': 0.34
                        },
                        'discipline': {
                            'cartons_jaunes': regression_result['statistiques']['cartons_jaunes'],
                            'cartons_rouges': regression_result['statistiques']['cartons_rouges'],
                            'fautes_commises': regression_result['statistiques']['fautes'],
                            'fautes_subies': regression_result['statistiques']['fautes']
                        },
                        'jeu': {
                            'possession_moyenne': 45.0,
                            'passes_reussies': regression_result['statistiques']['passes_reussies_equipe2'],
                            'precision_passes': 80.0,
                            'tirs': 10.0,
                            'tirs_cadres': 4.0,
                            'corners': 5.0,
                            'hors_jeu': 1.5
                        },
                        'coups_de_pied_arretes': {
                            'penalties_marques': 0.1,
                            'penalties_concedes': 0.1,
                            'coups_francs_marques': regression_result['statistiques']['coups_francs'],
                            'coups_francs_concedes': regression_result['statistiques']['coups_francs']
                        }
                    },
                    'confrontations_directes': {
                        'victoires_domicile': 0.33,
                        'victoires_exterieur': 0.33,
                        'nuls': 0.34,
                        'buts_domicile': regression_result['buts_equipe1'],
                        'buts_exterieur': regression_result['buts_equipe2']
                    }
                }
            }
        # Si le modèle de régression échoue, essayer le modèle GradientBoosting
        if self.model is not None:
            try:
                # Préparation des données
                match_data = self.prepare_match_data(equipe_domicile, equipe_exterieur, type_competition, competition)
                # Prédiction
                probas = self.model.predict_proba(match_data)
                # Formatage du résultat
                return {
                    'home_win': float(probas[0][0]),
                    'draw': float(probas[0][1]),
                    'away_win': float(probas[0][2]),
                    'home_team': equipe_domicile,
                    'away_team': equipe_exterieur,
                    'model_used': 'GradientBoosting',
                    'statistics': {
                        'home': {
                            'goals_scored': float(match_data['buts_marques_domicile_home'].iloc[0]),
                            'goals_conceded': float(match_data['buts_encaisses_domicile_home'].iloc[0]),
                            'wins': float(match_data['victoires_domicile_home'].iloc[0]),
                            'points_per_match': float(match_data['points_par_match_home'].iloc[0]),
                            'form': {
                                'wins': float(match_data['forme_victoires_domicile'].iloc[0]),
                                'draws': float(match_data['forme_nuls_domicile'].iloc[0]),
                                'losses': float(match_data['forme_defaites_domicile'].iloc[0])
                            },
                            'discipline': {
                                'yellow_cards': float(match_data['cartons_jaunes_home'].iloc[0]),
                                'red_cards': float(match_data['cartons_rouges_home'].iloc[0]),
                                'fouls_committed': float(match_data['fautes_commises_home'].iloc[0]),
                                'fouls_suffered': float(match_data['fautes_subies_home'].iloc[0])
                            },
                            'play': {
                                'possession': float(match_data['possession_moyenne_home'].iloc[0]),
                                'passes_completed': float(match_data['passes_reussies_home'].iloc[0]),
                                'pass_accuracy': float(match_data['precision_passes_home'].iloc[0]),
                                'shots': float(match_data['tirs_home'].iloc[0]),
                                'shots_on_target': float(match_data['tirs_cadres_home'].iloc[0]),
                                'corners': float(match_data['corners_home'].iloc[0]),
                                'offsides': float(match_data['hors_jeu_home'].iloc[0])
                            },
                            'set_pieces': {
                                'penalties_scored': float(match_data['penalties_marques_home'].iloc[0]),
                                'penalties_conceded': float(match_data['penalties_concedes_home'].iloc[0]),
                                'free_kicks_scored': float(match_data['coups_francs_marques_home'].iloc[0]),
                                'free_kicks_conceded': float(match_data['coups_francs_concedes_home'].iloc[0])
                            }
                        },
                        'away': {
                            'goals_scored': float(match_data['buts_marques_exterieur_away'].iloc[0]),
                            'goals_conceded': float(match_data['buts_encaisses_exterieur_away'].iloc[0]),
                            'wins': float(match_data['victoires_exterieur_away'].iloc[0]),
                            'points_per_match': float(match_data['points_par_match_away'].iloc[0]),
                            'form': {
                                'wins': float(match_data['forme_victoires_exterieur'].iloc[0]),
                                'draws': float(match_data['forme_nuls_exterieur'].iloc[0]),
                                'losses': float(match_data['forme_defaites_exterieur'].iloc[0])
                            },
                            'discipline': {
                                'yellow_cards': float(match_data['cartons_jaunes_away'].iloc[0]),
                                'red_cards': float(match_data['cartons_rouges_away'].iloc[0]),
                                'fouls_committed': float(match_data['fautes_commises_away'].iloc[0]),
                                'fouls_suffered': float(match_data['fautes_subies_away'].iloc[0])
                            },
                            'play': {
                                'possession': float(match_data['possession_moyenne_away'].iloc[0]),
                                'passes_completed': float(match_data['passes_reussies_away'].iloc[0]),
                                'pass_accuracy': float(match_data['precision_passes_away'].iloc[0]),
                                'shots': float(match_data['tirs_away'].iloc[0]),
                                'shots_on_target': float(match_data['tirs_cadres_away'].iloc[0]),
                                'corners': float(match_data['corners_away'].iloc[0]),
                                'offsides': float(match_data['hors_jeu_away'].iloc[0])
                            },
                            'set_pieces': {
                                'penalties_scored': float(match_data['penalties_marques_away'].iloc[0]),
                                'penalties_conceded': float(match_data['penalties_concedes_away'].iloc[0]),
                                'free_kicks_scored': float(match_data['coups_francs_marques_away'].iloc[0]),
                                'free_kicks_conceded': float(match_data['coups_francs_concedes_away'].iloc[0])
                            }
                        },
                        'head_to_head': {
                            'home_wins': float(match_data['h2h_victoires_domicile'].iloc[0]),
                            'away_wins': float(match_data['h2h_victoires_exterieur'].iloc[0]),
                            'draws': float(match_data['h2h_nuls'].iloc[0]),
                            'home_goals': float(match_data['h2h_buts_domicile'].iloc[0]),
                            'away_goals': float(match_data['h2h_buts_exterieur'].iloc[0])
                        }
                    }
    }
            except Exception as e:
                return {
                    'error': f'Erreur lors de la prédiction: {str(e)}'
                }
        
        # Si aucun modèle ne fonctionne
        return {
            'error': 'Aucun modèle disponible pour la prédiction'
        }
    
    def get_available_teams(self):
        """Récupération de la liste des équipes disponibles"""
        try:
            data_dir = Path(__file__).parent.parent.parent / 'FIP_DB'
            teams_df = pd.read_csv(data_dir / 'equipes_data.csv')
            return teams_df['equipe'].tolist()
        except Exception as e:
            print(f"Erreur lors de la récupération des équipes: {str(e)}")
            return []

    # Mapping entre les IDs du frontend (COMPETITIONS) et les IDs internes utilisés dans self.teams
    COMPETITION_ID_MAP = {
        'champions_league': 'cl',
        'premier_league': 'en.1',
        'laliga': 'es.1',
        'bundesliga': 'de.1',
        'serie_a': 'it.1',
        'ligue_1': 'fr.1',
        # Ajouter d'autres mappings si besoin
    }

    def get_teams_by_competition(self, competition_id):
        """Récupère la liste des équipes pour une compétition donnée (en gérant le mapping d'ID)"""
        # Mapper l'ID du frontend vers l'ID interne si besoin
        mapped_id = self.COMPETITION_ID_MAP.get(competition_id, competition_id)
        if mapped_id in self.teams:
            teams = self.teams[mapped_id]
            # Charger le mapping des équipes
            team_mapping = {}
            mapping_file = os.path.join('static', 'img', 'teams', 'team_mapping.txt')
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) >= 3:
                            team_id, team_name, comp = parts
                            team_mapping[team_name] = team_id
            # Ajouter le chemin du logo pour chaque équipe
            for team in teams:
                team_name = team['name']
                team_id = team_mapping.get(team_name)
                logo_path = f'static/img/teams/{team_id}.png' if team_id else None
                if team_id and os.path.exists(logo_path):
                    team['logo'] = f'/static/img/teams/{team_id}.png'
                else:
                    team['logo'] = '/static/img/teams/default-team.svg'  # SVG par défaut
            return teams
        return []

    def get_available_competitions(self):
        """Récupération de la liste des compétitions disponibles"""
        return self.competitions

    def get_competition_details(self, competition_id):
        """Récupère les détails d'une compétition spécifique"""
        # Chercher dans les compétitions de clubs
        for comp in self.competitions['clubs']['competitions']:
            if comp['id'] == competition_id:
                teams = self.get_teams_by_competition(competition_id)
                return {
                    'id': comp['id'],
                    'name': comp['name'],
                    'logo': comp['logo'],
                    'type': 'clubs',
                    'teams': teams,
                    'team_count': len(teams)
                }
        
        # Chercher dans les compétitions de nations
        for comp in self.competitions['nations']['competitions']:
            if comp['id'] == competition_id:
                teams = self.get_teams_by_competition(competition_id)
                return {
                    'id': comp['id'],
                    'name': comp['name'],
                    'logo': comp['logo'],
                    'type': 'nations',
                    'teams': teams,
                    'team_count': len(teams)
                }
        
        # Si la compétition n'est pas trouvée
        return None

    def _normalize_name(self, name):
        # Normalise les noms pour matcher mapping <-> CSV (minuscule, sans accents, espaces/underscores)
        name = name.lower().replace(' ', '_').replace('-', '_')
        name = ''.join((c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn'))
        return name

    def _load_teams_data(self):
        """Charger les données des équipes depuis le CSV pour couvrir toutes les équipes du mapping"""
        data_dir = Path(__file__).parent.parent.parent / 'FIP_DB'
        csv_path = data_dir / 'equipes_data.csv'
        teams_data = {}
        try:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                # Normalisation du nom pour correspondre au mapping
                team_key = self._normalize_name(str(row['equipe']))
                teams_data[team_key] = {
                    'name': row['equipe'],
                    'competition': row['competition'],
                    'stats': {
                        'goals_scored_home': row.get('buts_marques_domicile', 0),
                        'goals_scored_away': row.get('buts_marques_exterieur', 0),
                        'goals_conceded_home': row.get('buts_encaisses_domicile', 0),
                        'goals_conceded_away': row.get('buts_encaisses_exterieur', 0),
                        'matches_played': row.get('matchs_joues', 0),
                        'wins_home': row.get('victoires_domicile', 0),
                        'wins_away': row.get('victoires_exterieur', 0),
                        'draws': row.get('nuls', 0),
                        'points_per_match': row.get('points_par_match', 0)
                    }
                }
        except Exception as e:
            print(f"Erreur lors du chargement des données d'équipes: {e}")
        return teams_data

    def get_match_stats(self, home_team, away_team):
        """Obtenir les statistiques du match"""
        try:
            home_data = self.teams_data[home_team]
            away_data = self.teams_data[away_team]
            
            return {
                'cards': {
                    'yellow': {
                        'home': home_data['stats']['yellow_cards'],
                        'away': away_data['stats']['yellow_cards']
                    },
                    'red': {
                        'home': home_data['stats']['red_cards'],
                        'away': away_data['stats']['red_cards']
                    }
                },
                'corners': {
                    'home': home_data['stats']['corners'],
                    'away': away_data['stats']['corners']
                },
                'offsides': {
                    'home': home_data['stats']['offsides'],
                    'away': away_data['stats']['offsides']
                },
                'fouls': {
                    'home': home_data['stats']['fouls'],
                    'away': away_data['stats']['fouls']
                }
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques: {str(e)}")
            return {}

    def get_team_info(self, team_id):
        """Obtenir les informations d'une équipe"""
        return self.teams_data.get(team_id)

    def get_upcoming_matches(self, competition_id):
        """Obtenir les matchs à venir pour une compétition (en gérant le mapping d'ID)"""
        mapped_id = self.COMPETITION_ID_MAP.get(competition_id, competition_id)
        upcoming_matches = []
        teams = self.get_teams_by_competition(competition_id)
        if len(teams) < 2:
            return []
        for i in range(min(5, len(teams) // 2)):
            available_teams = teams.copy()
            home_team = random.choice(available_teams)
            available_teams.remove(home_team)
            away_team = random.choice(available_teams)
            match_date = datetime.now() + timedelta(days=random.randint(1, 30))
            # S'assurer que home_team et away_team sont des dicts avec 'name' et 'logo' (toujours)
            upcoming_matches.append({
                'home_team': {
                    'name': home_team['name'],
                    'logo': home_team['logo']
                },
                'away_team': {
                    'name': away_team['name'],
                    'logo': away_team['logo']
                },
                'date': match_date.strftime('%d/%m/%Y'),
                'time': f"{random.randint(18, 21)}:00",
                'venue': "Stade Principal"
            })
        return upcoming_matches