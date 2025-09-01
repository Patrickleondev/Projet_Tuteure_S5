// Configuration des équipes par championnat avec validation
export const TEAMS_CONFIG = {
  champions_league: {
    name: 'Ligue des Champions',
    teams: [
      'Real Madrid', 'Manchester City', 'Bayern Munich', 'PSG', 'Barcelona',
      'Liverpool', 'Chelsea', 'Juventus', 'Inter Milan', 'Milan',
      'Dortmund', 'Atletico Madrid', 'Porto', 'Benfica', 'Ajax'
    ]
  },
  ligue1: {
    name: 'Ligue 1',
    teams: [
      'PSG', 'Marseille', 'Lyon', 'Lille', 'Monaco', 
      'Rennes', 'Nice', 'Lens', 'Strasbourg', 'Montpellier'
    ]
  },
  premier_league: {
    name: 'Premier League',
    teams: [
      'Manchester City', 'Liverpool', 'Arsenal', 'Manchester United',
      'Chelsea', 'Tottenham', 'Newcastle', 'West Ham', 'Brighton', 'Aston Villa'
    ]
  },
  liga: {
    name: 'La Liga',
    teams: [
      'Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla',
      'Real Sociedad', 'Villarreal', 'Athletic Bilbao', 'Valencia', 'Betis', 'Osasuna'
    ]
  }
};

// Fonction de validation d'équipe
export function validateTeamInLeague(team, league) {
  return TEAMS_CONFIG[league]?.teams.includes(team) || false;
}

// Fonction de validation de match
export function validateMatch(homeTeam, awayTeam, league) {
  return validateTeamInLeague(homeTeam, league) && 
         validateTeamInLeague(awayTeam, league) && 
         homeTeam !== awayTeam;
}