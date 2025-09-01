import { generateMockPrediction, generateMockUpcomingMatches } from './mockData.js';

export const fetchUpcomingMatches = async () => {
  try {
    // En production, utilise les données simulées
    return generateMockUpcomingMatches();
  } catch (error) {
    console.error('API Error:', error.message);
    return [];
  }
};

export const predictMatch = async (league, team1, team2) => {
  try {
    if (!league || !team1 || !team2) {
      throw new Error('Tous les paramètres sont requis');
    }

    // En production, utilise les prédictions simulées
    return generateMockPrediction(team1, team2);
  } catch (error) {
    throw new Error(error.message || 'Erreur lors de la prédiction. Veuillez réessayer.');
  }
};