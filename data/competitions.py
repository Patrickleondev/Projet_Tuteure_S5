"""
Configuration des compétitions disponibles
"""

COMPETITIONS = {
    "clubs": [
        {
            "id": "champions_league",
            "name": "UEFA Champions League",
            "image": "champions-league.png",
            "country": "Europe",
            "type": "Club"
        },
        {
            "id": "premier_league",
            "name": "Premier League",
            "image": "premier-league.png",
            "country": "Angleterre",
            "type": "Club"
        },
        {
            "id": "laliga",
            "name": "LaLiga",
            "image": "laliga.png",
            "country": "Espagne",
            "type": "Club"
        },
        {
            "id": "bundesliga",
            "name": "Bundesliga",
            "image": "bundesliga.png",
            "country": "Allemagne",
            "type": "Club"
        },
        {
            "id": "serie_a",
            "name": "Serie A",
            "image": "serie-a.png",
            "country": "Italie",
            "type": "Club"
        },
        {
            "id": "ligue_1",
            "name": "Ligue 1",
            "image": "ligue-1.png",
            "country": "France",
            "type": "Club"
        },
        {
            "id": "club_world_cup",
            "name": "Coupe du Monde des Clubs",
            "image": "club-world-cup.webp",
            "country": "International",
            "type": "Club"
        }
    ],
    "nations": [
        {
            "id": "world_cup",
            "name": "Coupe du Monde FIFA",
            "image": "world-cup.png",
            "type": "International"
        },
        {
            "id": "euro",
            "name": "UEFA Euro",
            "image": "euro.png",
            "type": "International"
        },
        {
            "id": "copa_america",
            "name": "Copa América",
            "image": "copa-america.png",
            "type": "International"
        },
        {
            "id": "can",
            "name": "Coupe d'Afrique des Nations",
            "image": "can.webp",
            "type": "International"
        }
    ]
} 