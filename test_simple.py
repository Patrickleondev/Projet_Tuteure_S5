#!/usr/bin/env python3
"""
Script de test simplifié pour vérifier l'intégration
"""
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test des imports"""
    print("🧪 Test des imports...")
    try:
        from services.regression_service import RegressionPredictionService
        print("✅ RegressionPredictionService importé avec succès")
        
        from services.prediction_service import PredictionService
        print("✅ PredictionService importé avec succès")
        
        from services.chatbot_service import ChatbotService
        print("✅ ChatbotService importé avec succès")
        
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {str(e)}")
        return False

def test_regression_service():
    """Test du service de régression"""
    print("\n🔧 Test du service de régression...")
    try:
        from services.regression_service import RegressionPredictionService
        
        service = RegressionPredictionService()
        
        if service.model and service.scaler:
            print("✅ Modèle et scaler chargés avec succès")
            
            # Test de prédiction
            result = service.predict_match_result("Real Madrid", "Barcelona")
            if result:
                print("✅ Prédiction réussie")
                print(f"   Score: {result['buts_equipe1']} - {result['buts_equipe2']}")
                print(f"   Résultat: {result['resultat']}")
            else:
                print("❌ Échec de la prédiction")
        else:
            print("❌ Modèle ou scaler non chargé")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_prediction_service():
    """Test du service de prédiction principal"""
    print("\n🎯 Test du service de prédiction principal...")
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        
        # Test de récupération des équipes
        teams = service.get_available_competitions()
        if teams:
            print("✅ Compétitions chargées avec succès")
            print(f"   Nombre de types de compétitions: {len(teams)}")
        else:
            print("❌ Échec du chargement des compétitions")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test d'intégration du système FIP")
    print("=" * 50)
    
    # Tests
    success = True
    
    if not test_imports():
        success = False
    
    if not test_regression_service():
        success = False
    
    if not test_prediction_service():
        success = False
    
    # Résultat final
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
        print("\n📋 Prochaines étapes:")
        print("1. Activer l'environnement virtuel: .venv\\Scripts\\Activate.ps1")
        print("2. Lancer l'application: python app.py")
        print("3. Ouvrir http://localhost:5000 dans le navigateur")
    else:
        print("❌ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return success

if __name__ == "__main__":
    main() 