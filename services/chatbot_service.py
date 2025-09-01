"""
Service de chatbot pour l'assistance utilisateur utilisant OpenRouter API avec le modèle Deepseek
"""
import os
import json
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class ChatbotService:
    def __init__(self):
        # Récupérer les variables d'environnement
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.site_url = os.getenv('SITE_URL', 'http://localhost:5000')
        self.site_name = os.getenv('SITE_NAME', 'Football_Insight_Predictor')
        
        # Liste des suggestions de questions
        self.suggested_questions = [
            "Comment fonctionne le système de prédiction ?",
            "Quelles sont les statistiques prises en compte ?",
            "Comment sont calculées les probabilités ?",
            "Quelles compétitions sont disponibles ?",
            "Comment interpréter les résultats ?",
            "Quels facteurs influencent les prédictions ?",
            "Comment est évalué le niveau d'une équipe ?",
            "Quelle est la fiabilité des prédictions ?",
            "Comment sont gérées les absences de joueurs ?",
            "Quelles données historiques sont utilisées ?"
        ]
    
    def get_suggested_questions(self):
        """Retourne la liste des questions suggérées"""
        return self.suggested_questions
        
    def get_response(self, message):
        """Obtenir une réponse du chatbot"""
        try:
            if not self.api_key:
                return "Configuration de l'API manquante. Veuillez configurer votre clé API dans le fichier .env"

            response = requests.post(
                url=f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-coder:latest",
                    "messages": [
                        {
                            "role": "system",
                            "content": """Tu es un assistant spécialisé dans le football et les prédictions de matchs. 
                            Tu peux aider avec :
                            - Les prédictions de matchs
                            - Les statistiques des équipes
                            - Les informations sur les compétitions
                            - L'historique des confrontations
                            - Les analyses tactiques
                            
                            Réponds de manière claire et concise en français."""
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ]
                })
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 401:
                return "Erreur d'authentification. Veuillez vérifier votre clé API."
            else:
                print(f"Erreur API: {response.status_code} - {response.text}")
                return "Je suis désolé, mais je ne peux pas répondre à cette question pour le moment. Essayez une autre question ou revenez plus tard."
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion: {str(e)}")
            return "Impossible de se connecter au service. Veuillez vérifier votre connexion internet."
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse: {str(e)}")
            return "Une erreur inattendue s'est produite. Veuillez réessayer plus tard." 