"""
Football Insight Predictor (FIP)
Programme principal
"""
from data.matches_data import HISTORICAL_DATA
from utils.stats_calculator import predict_match_stats

def print_predictions(team1: str, team2: str, predictions: dict, accuracy: float):
    """Affiche les prédictions de manière formatée"""
    print("\n=== Prédictions du Match ===")
    print(f"{team1.upper()} vs {team2.upper()}\n")
    print(f"Score prédit: {team1}: {predictions['buts_equipe1']} - {team2}: {predictions['buts_equipe2']}")
    print(f"\nStatistiques prédites:")
    print(f"- Cartons jaunes: {predictions['cartons_jaunes']}")
    print(f"- Cartons rouges: {predictions['cartons_rouges']}")
    print(f"- Passes réussies {team1}: {predictions['passes_reussies_equipe1']}")
    print(f"- Passes réussies {team2}: {predictions['passes_reussies_equipe2']}")
    print(f"- Coups-francs: {predictions['coups_francs']}")
    print(f"- Fautes: {predictions['fautes']}")
    print(f"\nDegré de précision: {accuracy:.1f}%")

def main():
    print("=== Football Insight Predictor (FIP) ===")
    print("\nÉquipes disponibles pour la prédiction:")
    print("- PSG")
    print("- Marseille")
    print("- Lyon")
    print("- Lille")
    
    while True:
        team1 = input("\nEntrez le nom de la première équipe: ").strip().lower()
        team2 = input("Entrez le nom de la deuxième équipe: ").strip().lower()

        try:
            predictions, accuracy = predict_match_stats(HISTORICAL_DATA, team1, team2)
            print_predictions(team1, team2, predictions, accuracy)
        except ValueError as e:
            print(f"\nErreur: {e}")
            print("Veuillez choisir parmi les équipes disponibles.")
        
        if input("\nVoulez-vous faire une autre prédiction? (o/n): ").lower() != 'o':
            break

if __name__ == "__main__":
    main()