import { TEAMS_BY_LEAGUE } from './data/teams.js';
import { generateMatchStats } from './utils/matchStatsGenerator.js';

export const generateMockPrediction = (team1, team2) => {
  // Simule une prédiction réaliste avec des valeurs par défaut
  const defaultStats = {
    possession_moyenne: 50,
    precision_passes: 80,
    tirs_par_match: 12
  };

  const team1Stats = defaultStats;
  const team2Stats = defaultStats;

  // Utilise le service de prédiction
  const predictions = generateMatchStats(team1Stats, team2Stats);
  
  return {
    status: 'success',
    predictions,
    accuracy: 75 + Math.floor(Math.random() * 15)
  };
};

export const generateMockUpcomingMatches = () => {
  const competitions = ['Ligue 1', 'Premier League', 'La Liga', 'Champions League'];
  const matches = [];

  // Génère 5 matchs valides
  for (let i = 0; i < 5; i++) {
    const competition = competitions[Math.floor(Math.random() * competitions.length)];
    const teams = TEAMS_BY_LEAGUE[competition.toLowerCase().replace(/ /g, '_')] || [];
    
    if (teams.length < 2) continue;

    // Sélectionne deux équipes différentes du même championnat
    const team1Index = Math.floor(Math.random() * teams.length);
    let team2Index;
    do {
      team2Index = Math.floor(Math.random() * teams.length);
    } while (team2Index === team1Index);

    matches.push({
      competition,
      date: new Date(Date.now() + Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      homeTeam: teams[team1Index],
      awayTeam: teams[team2Index]
    });
  }

  return matches;
};