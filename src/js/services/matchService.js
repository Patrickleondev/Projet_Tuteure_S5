import { validateMatch } from '../config/teams.js';

export class MatchService {
  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL;
  }

  async getUpcomingMatches(league) {
    try {
      const response = await fetch(`${this.baseUrl}/api/upcoming-matches`);
      const matches = await response.json();
      
      // Filtrer les matchs pour ne garder que ceux du championnat sélectionné
      return matches.filter(match => 
        validateMatch(match.homeTeam, match.awayTeam, league)
      );
    } catch (error) {
      console.error('Error fetching matches:', error);
      return [];
    }
  }

  async predictMatch(league, team1, team2) {
    if (!validateMatch(team1, team2, league)) {
      throw new Error('Les équipes sélectionnées ne sont pas valides pour ce championnat');
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ league, team1, team2 })
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la prédiction');
      }

      return await response.json();
    } catch (error) {
      throw new Error(error.message || 'Erreur lors de la prédiction');
    }
  }
}

export const matchService = new MatchService();