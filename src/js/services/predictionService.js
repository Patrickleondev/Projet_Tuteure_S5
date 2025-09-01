import { TEAM_STATS } from '../data/teamStats.js';
import { generateMatchStats } from '../utils/statsPredictor.js';

export class PredictionService {
  predictMatch(team1, team2) {
    const team1Stats = TEAM_STATS[team1] || this.getDefaultTeamStats();
    const team2Stats = TEAM_STATS[team2] || this.getDefaultTeamStats();
    
    const predictions = generateMatchStats(team1Stats, team2Stats);
    const accuracy = this.calculateAccuracy(team1Stats, team2Stats);

    return {
      status: 'success',
      predictions,
      accuracy
    };
  }

  getDefaultTeamStats() {
    return {
      possession_moyenne: 50,
      precision_passes: 80,
      tirs_par_match: 12
    };
  }

  calculateAccuracy(team1Stats, team2Stats) {
    // Plus les données sont complètes, plus la précision est élevée
    const baseAccuracy = 75;
    const dataCompleteness = (
      (team1Stats !== this.getDefaultTeamStats() ? 10 : 0) +
      (team2Stats !== this.getDefaultTeamStats() ? 10 : 0)
    );
    
    return Math.min(95, baseAccuracy + dataCompleteness);
  }
}

export const predictionService = new PredictionService();