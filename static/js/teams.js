import { TEAMS_BY_LEAGUE } from './data/teams.js';
import { predictMatch } from './api.js';

class TeamSelector {
    constructor() {
        this.leagueSelect = document.getElementById('league');
        this.team1Select = document.getElementById('team1');
        this.team2Select = document.getElementById('team2');
        this.predictButton = document.getElementById('predict');
        this.resultsDiv = document.getElementById('prediction-results');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.leagueSelect.addEventListener('change', () => this.updateTeams());
        [this.team1Select, this.team2Select].forEach(select => {
            select.addEventListener('change', () => this.updatePredictButton());
        });
        this.predictButton.addEventListener('click', () => this.handlePrediction());
    }

    updateTeams() {
        const teams = TEAMS_BY_LEAGUE[this.leagueSelect.value] || [];
        
        [this.team1Select, this.team2Select].forEach(select => {
            select.innerHTML = '<option value="">Sélectionnez une équipe</option>';
            teams.forEach(team => {
                const option = new Option(team, team.toLowerCase().replace(/ /g, '_'));
                select.add(option);
            });
            select.disabled = teams.length === 0;
        });
        
        this.predictButton.disabled = true;
    }

    // Reste du code de la classe inchangé
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => new TeamSelector());