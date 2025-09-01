from services.prediction_service import PredictionService
from services.match_service import MatchService

def test_prediction_system():
    # Initialiser les services
    prediction_service = PredictionService()
    match_service = MatchService()
    
    # Test avec deux équipes connues
    team1 = "Manchester City"
    team2 = "Real Madrid"
    
    try:
        # Tester la prédiction
        prediction = prediction_service.predict_match(team1, team2)
        print(f"\nPrédiction pour {team1} vs {team2}:")
        print(f"Probabilités: {prediction['predictions']}")
        print(f"Précision estimée: {prediction['accuracy']}%")
        
        # Tester les statistiques
        stats = prediction_service.get_match_stats(team1, team2)
        print("\nStatistiques du match:")
        print(f"Possession: {stats['possession']}")
        print(f"Tirs: {stats['shots']}")
        print(f"Passes: {stats['passes']}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Test du système de prédiction...")
    success = test_prediction_system()
    print(f"\nTest {'réussi' if success else 'échoué'}") 