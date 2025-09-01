export class MatchStats {
  constructor(container) {
    this.container = container;
  }

  display(predictions, team1Name, team2Name) {
    this.container.innerHTML = `
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${team1Name}</h4>
          <div class="space-y-2">
            <p>Score: ${predictions.buts_equipe1}</p>
            <p>Possession: ${predictions.possession_equipe1}%</p>
            <p>Tirs: ${predictions.tirs_equipe1}</p>
            <p>Tirs cadrés: ${predictions.tirs_cadres_equipe1}</p>
            <p>Cartons jaunes: ${predictions.cartons_jaunes_equipe1}</p>
            <p>Cartons rouges: ${predictions.cartons_rouges_equipe1}</p>
            <p>Passes réussies: ${predictions.passes_reussies_equipe1}</p>
            <p>Coups francs: ${predictions.coups_francs_equipe1}</p>
            <p>Corners: ${predictions.corners_equipe1}</p>
            <p>Fautes: ${predictions.fautes_equipe1}</p>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${team2Name}</h4>
          <div class="space-y-2">
            <p>Score: ${predictions.buts_equipe2}</p>
            <p>Possession: ${predictions.possession_equipe2}%</p>
            <p>Tirs: ${predictions.tirs_equipe2}</p>
            <p>Tirs cadrés: ${predictions.tirs_cadres_equipe2}</p>
            <p>Cartons jaunes: ${predictions.cartons_jaunes_equipe2}</p>
            <p>Cartons rouges: ${predictions.cartons_rouges_equipe2}</p>
            <p>Passes réussies: ${predictions.passes_reussies_equipe2}</p>
            <p>Coups francs: ${predictions.coups_francs_equipe2}</p>
            <p>Corners: ${predictions.corners_equipe2}</p>
            <p>Fautes: ${predictions.fautes_equipe2}</p>
          </div>
        </div>
      </div>
    `;
  }
}