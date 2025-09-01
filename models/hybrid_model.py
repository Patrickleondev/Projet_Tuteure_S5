"""
Modèle hybride combinant ML classique et Deep Learning
"""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

# Import conditionnel de TensorFlow
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    Sequential = None
    Dense = None
    Dropout = None

class HybridModel:
    def __init__(self):
        self.gb_model = GradientBoostingClassifier()
        self.scaler = StandardScaler()
        self.tensorflow_available = TENSORFLOW_AVAILABLE
        
        if self.tensorflow_available:
            self.nn_model = self._build_nn_model()
        else:
            self.nn_model = None
            print("Warning: TensorFlow n'est pas disponible. Le modèle hybride utilisera uniquement GradientBoosting.")
        
    def _build_nn_model(self):
        """Construit le modèle de réseau de neurones si TensorFlow est disponible"""
        if not self.tensorflow_available:
            return None
            
        model = Sequential([
            Dense(128, activation='relu', input_shape=(20,)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(3, activation='softmax')  # Win, Draw, Loss
        ])
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def preprocess_features(self, X):
        """
        Prétraitement des caractéristiques
        - Normalisation
        - Feature engineering
        """
        features = [
            'classement_moyen',
            'buts_marques_domicile',
            'buts_marques_exterieur',
            'buts_encaisses_domicile',
            'buts_encaisses_exterieur',
            'clean_sheets',
            'possession_moyenne',
            'precision_passes',
            'duels_gagnes',
            'tirs_par_match',
            # Nouvelles features
            'forme_derniers_matchs',
            'fatigue_equipe',
            'force_effectif',
            'historique_confrontations',
            'meteo_impact',
            'distance_deplacement',
            'jours_repos',
            'blessures_impact',
            'xG_moyen',
            'ppda_moyen'
        ]
        return self.scaler.fit_transform(X[features])
    
    def fit(self, X, y):
        """
        Entraînement du modèle hybride
        """
        X_processed = self.preprocess_features(X)
        
        # Entraînement GradientBoosting
        self.gb_model.fit(X_processed, y)
        
        # Entraînement Neural Network si disponible
        if self.tensorflow_available and self.nn_model is not None:
            self.nn_model.fit(X_processed, y,
                             epochs=50,
                             batch_size=32,
                             validation_split=0.2,
                             verbose=0)
    
    def predict(self, X):
        """
        Prédiction hybride
        """
        X_processed = self.preprocess_features(X)
        
        # Prédictions GradientBoosting
        gb_pred = self.gb_model.predict_proba(X_processed)
        
        if self.tensorflow_available and self.nn_model is not None:
            # Prédictions Neural Network
            nn_pred = self.nn_model.predict(X_processed)
            # Moyenne pondérée des prédictions
            final_pred = 0.6 * gb_pred + 0.4 * nn_pred
        else:
            # Utiliser uniquement GradientBoosting si TensorFlow n'est pas disponible
            final_pred = gb_pred
        
        return np.argmax(final_pred, axis=1)
    
    def evaluate_confidence(self, X):
        """
        Évaluation de la confiance de la prédiction
        """
        X_processed = self.preprocess_features(X)
        
        gb_pred = self.gb_model.predict_proba(X_processed)
        
        if self.tensorflow_available and self.nn_model is not None:
            nn_pred = self.nn_model.predict(X_processed)
            final_pred = 0.6 * gb_pred + 0.4 * nn_pred
        else:
            final_pred = gb_pred
            
        confidence = np.max(final_pred, axis=1)
        
        return confidence 