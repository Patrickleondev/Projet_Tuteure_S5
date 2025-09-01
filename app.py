"""
Application Flask pour la prédiction des matchs de football
"""
from flask import Flask, request, jsonify, render_template, send_from_directory, abort
from services.prediction_service import PredictionService
from services.chatbot_service import ChatbotService
from data.competitions import COMPETITIONS
from flask_cors import CORS
from dotenv import load_dotenv
import os
from services.match_service import MatchService
from services.club_service import ClubService

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialiser les services
prediction_service = PredictionService()
chatbot_service = ChatbotService()
match_service = MatchService()
club_service = ClubService()

@app.route('/')
def index():
    """Page d'accueil avec présentation du projet"""
    return render_template('index.html', competitions=COMPETITIONS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/clubs')
def clubs():
    """Page des clubs"""
    return render_template('clubs.html')

@app.route('/predictions')
def predictions():
    """Page de prédiction des matchs"""
    return render_template('predictions.html', competitions=COMPETITIONS)

@app.route('/competitions')
def competitions():
    """Page des compétitions"""
    return render_template('competitions.html', competitions=COMPETITIONS)

@app.route('/competitions/<competition_id>')
def competition_detail(competition_id):
    """Page de détail d'une compétition"""
    # Récupérer les équipes pour cette compétition
    teams = prediction_service.get_teams_by_competition(competition_id)
    
    # Récupérer les informations de la compétition
    competition_info = None
    for comp_type in ['clubs', 'nations']:
        for comp in COMPETITIONS[comp_type]:
            if comp['id'] == competition_id:
                competition_info = comp
                break
        if competition_info:
            break
    
    if not competition_info:
        abort(404)
    
    # Récupérer les matchs à venir (simulés)
    upcoming_matches = prediction_service.get_upcoming_matches(competition_id)
    
    return render_template('competition_detail.html', 
                         competition=competition_info,
                         teams=teams,
                         upcoming_matches=upcoming_matches)

@app.route('/chatbot')
def chatbot():
    """Page du chatbot"""
    return render_template('chatbot.html')

@app.route('/static/<path:path>')
def send_static(path):
    """Servir les fichiers statiques"""
    return send_from_directory('static', path)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        competition_type = data.get('type', 'clubs')
        competition = data.get('competition')

        if not home_team or not away_team:
            return jsonify({'error': 'Les équipes ne sont pas spécifiées'}), 400

        result = prediction_service.predict_match(
            home_team,
            away_team,
            competition_type,
            competition
        )
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        # Formater la réponse pour le frontend
        response = {
            'predictions': {
                'home_win': result.get('home_win', result.get('victoire_domicile', 0)),
                'draw': result.get('draw', result.get('match_nul', 0)),
                'away_win': result.get('away_win', result.get('victoire_exterieur', 0))
            },
            'statistics': result.get('statistiques', result.get('statistics', {})),
            'home_team': home_team,
            'away_team': away_team
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team/<team_id>')
def get_team(team_id):
    """API endpoint pour obtenir les informations d'une équipe"""
    try:
        team_info = prediction_service.get_team_info(team_id)
        if team_info:
            return jsonify(team_info)
        return jsonify({'error': 'Équipe non trouvée'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<competition_id>', methods=['GET'])
def get_teams_by_competition(competition_id):
    """Endpoint pour récupérer la liste des équipes d'une compétition"""
    try:
        teams = prediction_service.get_teams_by_competition(competition_id)
        return jsonify(teams)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/competitions', methods=['GET'])
def get_competitions():
    """Endpoint pour récupérer la liste des compétitions"""
    try:
        competitions = prediction_service.get_available_competitions()
        return jsonify(competitions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/competition/<competition_id>', methods=['GET'])
def get_competition_details(competition_id):
    """Endpoint pour récupérer les détails d'une compétition"""
    try:
        competition = prediction_service.get_competition_details(competition_id)
        return jsonify(competition)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint pour le chatbot"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message manquant'}), 400
        
        message = data['message']
        response = chatbot_service.get_response(message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Erreur dans l'API chat: {str(e)}")
        return jsonify({
            'error': 'Une erreur est survenue',
            'details': str(e)
        }), 500

@app.route('/api/clubs/<competition_id>')
def get_clubs(competition_id):
    """Récupère les clubs d'une compétition"""
    try:
        clubs = club_service.get_clubs_by_competition(competition_id)
        return jsonify(clubs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clubs/details/<team_id>')
def get_club_details(team_id):
    """Récupère les détails d'un club"""
    try:
        details = club_service.get_team_details(team_id)
        if details:
            return jsonify(details)
        return jsonify({'error': 'Club non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upcoming-matches')
def upcoming_matches():
    """Page des matchs à venir"""
    return render_template('upcoming_matches.html')

@app.route('/api/upcoming-matches/<competition_id>')
def get_upcoming_matches(competition_id):
    """API pour récupérer les matchs à venir"""
    try:
        matches = match_service.get_upcoming_matches(competition_id)
        return jsonify(matches)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/match/<int:match_id>')
def get_match_details(match_id):
    """API pour récupérer les détails d'un match"""
    try:
        match = match_service.get_match_details(match_id)
        if match:
            return jsonify(match)
        return jsonify({'error': 'Match non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/suggestions', methods=['GET'])
def get_chat_suggestions():
    """API endpoint pour obtenir les suggestions de questions"""
    try:
        suggestions = chatbot_service.get_suggested_questions()
        return jsonify({
            'suggestions': suggestions,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': 'Une erreur est survenue',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)