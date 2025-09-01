import { predictMatch } from './api.js';
import { showUserError } from './utils/error-handler.js';
import { TEAMS_BY_LEAGUE } from './data/teams.js';
import { MatchStats } from './components/MatchStats.js';

class TeamSelector {
  constructor() {
    this.leagueSelect = document.getElementById('league');
    this.team1Select = document.getElementById('team1');
    this.team2Select = document.getElementById('team2');
    this.predictButton = document.getElementById('predict');
    this.resultsDiv = document.getElementById('prediction-results');
    this.matchStats = new MatchStats(document.getElementById('detailed-stats'));
    
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
    const league = this.leagueSelect.value;
    const teams = TEAMS_BY_LEAGUE[league] || [];
    
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

  updatePredictButton() {
    this.predictButton.disabled = !this.team1Select.value || 
                                !this.team2Select.value || 
                                this.team1Select.value === this.team2Select.value;
  }

  async handlePrediction() {
    try {
      const data = await predictMatch(
        this.leagueSelect.value,
        this.team1Select.value,
        this.team2Select.value
      );
      this.displayPrediction(data);
    } catch (error) {
      showUserError(error.message);
    }
  }

  displayPrediction(data) {
    if (data.status === 'error') {
      showUserError(data.message);
      return;
    }

    this.resultsDiv.classList.remove('hidden');
    
    const team1Name = this.team1Select.options[this.team1Select.selectedIndex].text;
    const team2Name = this.team2Select.options[this.team2Select.selectedIndex].text;
    
    document.getElementById('team1-name').textContent = team1Name;
    document.getElementById('team2-name').textContent = team2Name;
    document.getElementById('score1').textContent = data.predictions.buts_equipe1;
    document.getElementById('score2').textContent = data.predictions.buts_equipe2;
    document.getElementById('accuracy').textContent = data.accuracy.toFixed(1);
    
    this.matchStats.display(data.predictions, team1Name, team2Name);
  }
}

document.addEventListener('DOMContentLoaded', () => new TeamSelector());