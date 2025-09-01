import { TEAMS_CONFIG } from '../config/teams.js';
import { matchService } from '../services/matchService.js';

export class TeamSelector {
  constructor() {
    this.initializeElements();
    this.initializeEventListeners();
    this.initializeSearchableDropdowns();
  }

  initializeElements() {
    this.leagueSelect = document.getElementById('league');
    this.team1Select = document.getElementById('team1');
    this.team2Select = document.getElementById('team2');
    this.predictButton = document.getElementById('predict');
    this.resultsDiv = document.getElementById('prediction-results');
  }

  initializeEventListeners() {
    this.leagueSelect.addEventListener('change', () => this.updateTeams());
    [this.team1Select, this.team2Select].forEach(select => {
      select.addEventListener('change', () => this.updatePredictButton());
    });
    this.predictButton.addEventListener('click', () => this.handlePrediction());
  }

  initializeSearchableDropdowns() {
    [this.team1Select, this.team2Select].forEach(select => {
      const searchBox = document.createElement('input');
      searchBox.type = 'text';
      searchBox.placeholder = 'Rechercher une équipe...';
      searchBox.className = 'w-full p-2 border rounded mb-2';
      searchBox.addEventListener('input', (e) => this.filterTeams(e.target, select));
      select.parentNode.insertBefore(searchBox, select);
    });
  }

  filterTeams(searchBox, select) {
    const searchTerm = searchBox.value.toLowerCase();
    const teams = TEAMS_CONFIG[this.leagueSelect.value]?.teams || [];
    
    select.innerHTML = '<option value="">Sélectionnez une équipe</option>';
    teams
      .filter(team => team.toLowerCase().includes(searchTerm))
      .forEach(team => {
        const option = new Option(team, team);
        select.add(option);
      });
  }

  updateTeams() {
    const teams = TEAMS_CONFIG[this.leagueSelect.value]?.teams || [];
    
    [this.team1Select, this.team2Select].forEach(select => {
      select.innerHTML = '<option value="">Sélectionnez une équipe</option>';
      teams.forEach(team => {
        const option = new Option(team, team);
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
      const data = await matchService.predictMatch(
        this.leagueSelect.value,
        this.team1Select.value,
        this.team2Select.value
      );
      this.displayPrediction(data);
    } catch (error) {
      alert(error.message);
    }
  }

  displayPrediction(data) {
    if (data.status === 'error') {
      alert(data.message);
      return;
    }

    this.resultsDiv.classList.remove('hidden');
    
    const team1Name = this.team1Select.value;
    const team2Name = this.team2Select.value;
    
    document.getElementById('team1-name').textContent = team1Name;
    document.getElementById('team2-name').textContent = team2Name;
    document.getElementById('score1').textContent = data.predictions.buts_equipe1;
    document.getElementById('score2').textContent = data.predictions.buts_equipe2;
    
    const statsDiv = document.getElementById('detailed-stats');
    statsDiv.innerHTML = `
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${team1Name}</h4>
          <div class="space-y-2">
            <p>Cartons jaunes: ${data.predictions.cartons_jaunes_equipe1}</p>
            <p>Cartons rouges: ${data.predictions.cartons_rouges_equipe1}</p>
            <p>Coups francs: ${data.predictions.coups_francs_equipe1}</p>
            <p>Fautes: ${data.predictions.fautes_equipe1}</p>
            <p>Corners: ${data.predictions.corners_equipe1}</p>
            <p>Passes réussies: ${data.predictions.passes_reussies_equipe1}</p>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${team2Name}</h4>
          <div class="space-y-2">
            <p>Cartons jaunes: ${data.predictions.cartons_jaunes_equipe2}</p>
            <p>Cartons rouges: ${data.predictions.cartons_rouges_equipe2}</p>
            <p>Coups francs: ${data.predictions.coups_francs_equipe2}</p>
            <p>Fautes: ${data.predictions.fautes_equipe2}</p>
            <p>Corners: ${data.predictions.corners_equipe2}</p>
            <p>Passes réussies: ${data.predictions.passes_reussies_equipe2}</p>
          </div>
        </div>
      </div>
    `;
  }
}