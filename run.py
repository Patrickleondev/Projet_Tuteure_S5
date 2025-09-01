#!/usr/bin/env python3
"""
Script de lancement de l'application Football Insight Predictor
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Vérifier l'environnement"""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier Python
    print(f"   Python: {sys.version}")
    
    # Vérifier les dépendances
    try:
        import flask
        print("   ✅ Flask installé")
    except ImportError:
        print("   ❌ Flask non installé")
        return False
    
    try:
        import pandas
        print("   ✅ Pandas installé")
    except ImportError:
        print("   ❌ Pandas non installé")
        return False
    
    try:
        import joblib
        print("   ✅ Joblib installé")
    except ImportError:
        print("   ❌ Joblib non installé")
        return False
    
    try:
        import sklearn
        print("   ✅ Scikit-learn installé")
    except ImportError:
        print("   ❌ Scikit-learn non installé")
        return False
    
    return True

def check_files():
    """Vérifier les fichiers nécessaires"""
    print("\n📁 Vérification des fichiers...")
    
    # Fichiers du modèle
    model_path = Path(__file__).parent.parent.parent / 'Implémentation' / 'Regression' / 'modele_regression_foot.pkl'
    scaler_path = Path(__file__).parent.parent.parent / 'Implémentation' / 'Regression' / 'scaler_regression.pkl'
    
    if model_path.exists():
        print("   ✅ Modèle de régression trouvé")
    else:
        print("   ❌ Modèle de régression non trouvé")
        return False
    
    if scaler_path.exists():
        print("   ✅ Scaler trouvé")
    else:
        print("   ❌ Scaler non trouvé")
        return False
    
    # Fichiers de données
    data_dir = Path(__file__).parent.parent.parent / 'FIP_DB'
    equipes_file = data_dir / 'equipes_par_championnat.csv'
    matchs_file = data_dir / 'matchs_par_championnat.csv'
    
    if equipes_file.exists():
        print("   ✅ Données des équipes trouvées")
    else:
        print("   ❌ Données des équipes non trouvées")
        return False
    
    if matchs_file.exists():
        print("   ✅ Données des matchs trouvées")
    else:
        print("   ❌ Données des matchs non trouvées")
        return False
    
    return True

def run_tests():
    """Lancer les tests"""
    print("\n🧪 Lancement des tests...")
    
    try:
        from test_simple import main as test_main
        return test_main()
    except Exception as e:
        print(f"   ❌ Erreur lors des tests: {str(e)}")
        return False

def start_app():
    """Démarrer l'application"""
    print("\n🚀 Démarrage de l'application...")
    
    try:
        from app import app
        print("   ✅ Application Flask chargée")
        print("\n🌐 L'application est accessible à l'adresse:")
        print("   http://localhost:5000")
        print("\n📋 Fonctionnalités disponibles:")
        print("   - Prédiction de matchs")
        print("   - Statistiques des équipes")
        print("   - Assistant IA (chatbot)")
        print("   - Interface moderne")
        
        # Démarrer l'application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"   ❌ Erreur lors du démarrage: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("⚽ Football Insight Predictor - Lancement")
    print("=" * 50)
    
    # Vérifications
    if not check_environment():
        print("\n❌ Problème d'environnement détecté.")
        print("   Installez les dépendances: pip install -r requirements.txt")
        return False
    
    if not check_files():
        print("\n❌ Fichiers manquants détectés.")
        print("   Vérifiez que tous les fichiers sont présents.")
        return False
    
    # Tests
    if not run_tests():
        print("\n❌ Tests échoués.")
        return False
    
    print("\n✅ Toutes les vérifications sont passées !")
    
    # Démarrer l'application
    start_app()

if __name__ == "__main__":
    main() 