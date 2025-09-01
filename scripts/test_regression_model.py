"""
Script de test pour le modèle de régression
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.regression_service import RegressionPredictionService
import pandas as pd

def test_regression_model():
    """Test du modèle de régression"""
    print("🧪 Test du modèle de régression linéaire")
    print("=" * 50)
    
    # Initialisation du service
    service = RegressionPredictionService()
    
    if not service.model or not service.scaler:
        print("❌ Modèle ou scaler non chargé")
        return False
    
    print("✅ Modèle et scaler chargés avec succès")
    
    # Test avec des équipes existantes
    test_matches = [
        ("Real Madrid", "Barcelona"),
        ("Manchester City", "Liverpool"),
        ("PSG", "Bayern Munich"),
        ("France", "Brazil"),
        ("Argentina", "England")
    ]
    
    print("\n📊 Tests de prédiction:")
    print("-" * 30)
    
    for equipe1, equipe2 in test_matches:
        try:
            result = service.predict_match_result(equipe1, equipe2)
            
            if result:
                print(f"\n🏆 {equipe1} vs {equipe2}")
                print(f"   Score prédit: {equipe1} {result['buts_equipe1']} - {equipe2} {result['buts_equipe2']}")
                print(f"   Résultat: {result['resultat']}")
                print(f"   Gagnant: {result['gagnant']}")
                print(f"   Probabilités:")
                print(f"     - Victoire {equipe1}: {result['probabilites']['victoire_domicile']:.1%}")
                print(f"     - Match nul: {result['probabilites']['match_nul']:.1%}")
                print(f"     - Victoire {equipe2}: {result['probabilites']['victoire_exterieur']:.1%}")
            else:
                print(f"❌ Échec de prédiction pour {equipe1} vs {equipe2}")
                
        except Exception as e:
            print(f"❌ Erreur pour {equipe1} vs {equipe2}: {str(e)}")
    
    return True

def test_feature_preparation():
    """Test de la préparation des features"""
    print("\n🔧 Test de la préparation des features")
    print("=" * 50)
    
    service = RegressionPredictionService()
    
    # Test avec des équipes existantes
    equipe1, equipe2 = "Real Madrid", "Barcelona"
    
    try:
        features = service.prepare_features(equipe1, equipe2)
        
        if features is not None:
            print(f"✅ Features préparées pour {equipe1} vs {equipe2}")
            print(f"   Différence de tirs: {features[0][0]:.2f}")
            print(f"   Différence de possession: {features[0][1]:.2f}")
            print(f"   Différence de passes: {features[0][2]:.2f}")
            print(f"   Cartons jaunes: {features[0][3]}")
            print(f"   Cartons rouges: {features[0][4]}")
        else:
            print(f"❌ Échec de préparation des features pour {equipe1} vs {equipe2}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la préparation des features: {str(e)}")

def test_data_availability():
    """Test de la disponibilité des données"""
    print("\n📁 Test de la disponibilité des données")
    print("=" * 50)
    
    from pathlib import Path
    
    # Vérifier les fichiers de données
    data_dir = Path(__file__).parent.parent.parent / 'FIP_DB'
    
    files_to_check = [
        'equipes_par_championnat.csv',
        'matchs_par_championnat.csv'
    ]
    
    for file in files_to_check:
        file_path = data_dir / file
        if file_path.exists():
            print(f"✅ {file} trouvé")
            # Afficher quelques statistiques
            try:
                df = pd.read_csv(file_path)
                print(f"   - Nombre de lignes: {len(df)}")
                print(f"   - Colonnes: {list(df.columns)}")
            except Exception as e:
                print(f"   - Erreur de lecture: {str(e)}")
        else:
            print(f"❌ {file} non trouvé")
    
    # Vérifier les modèles
    model_dir = Path(__file__).parent.parent.parent / 'Implémentation' / 'Regression'
    
    model_files = [
        'modele_regression_foot.pkl',
        'scaler_regression.pkl'
    ]
    
    for file in model_files:
        file_path = model_dir / file
        if file_path.exists():
            print(f"✅ {file} trouvé")
        else:
            print(f"❌ {file} non trouvé")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du modèle de régression")
    print("=" * 60)
    
    # Tests
    test_data_availability()
    test_feature_preparation()
    test_regression_model()
    
    print("\n🎉 Tests terminés!") 