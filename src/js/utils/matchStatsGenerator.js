/**
 * Génère des statistiques de match réalistes
 */
export function generateMatchStats(team1Stats, team2Stats) {
  // Fonction utilitaire pour générer un nombre aléatoire dans une plage
  const randomInRange = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
  
  // Calcul du ratio de force entre les équipes basé sur leurs statistiques
  const team1Strength = (team1Stats.precision_passes + team1Stats.possession_moyenne) / 2;
  const team2Strength = (team2Stats.precision_passes + team2Stats.possession_moyenne) / 2;
  const strengthRatio = team1Strength / team2Strength;

  // Calcul de la possession avec variation basée sur la force relative des équipes
  const baseTeam1Possession = Math.min(65, Math.max(35, Math.round(50 * strengthRatio)));
  const possession1 = Math.min(70, Math.max(30, baseTeam1Possession + randomInRange(-5, 5)));
  const possession2 = 100 - possession1;

  // Génération des tirs avec influence de la possession
  const tirs1 = randomInRange(8, 18) * (possession1 / 50);
  const tirs2 = randomInRange(8, 18) * (possession2 / 50);
  
  // Environ 40% des tirs sont cadrés
  const tirsCadres1 = Math.round(tirs1 * 0.4);
  const tirsCadres2 = Math.round(tirs2 * 0.4);

  // Environ 25% des tirs cadrés deviennent des buts
  const buts1 = Math.round(tirsCadres1 * 0.25);
  const buts2 = Math.round(tirsCadres2 * 0.25);

  // Calcul des passes réussies avec arrondissement à l'entier
  const passesBase1 = randomInRange(400, 600);
  const passesBase2 = randomInRange(400, 600);
  const passes1 = Math.round(passesBase1 * (possession1 / 50));
  const passes2 = Math.round(passesBase2 * (possession2 / 50));

  return {
    buts_equipe1: buts1,
    buts_equipe2: buts2,
    possession_equipe1: possession1,
    possession_equipe2: possession2,
    tirs_equipe1: Math.round(tirs1),
    tirs_equipe2: Math.round(tirs2),
    tirs_cadres_equipe1: tirsCadres1,
    tirs_cadres_equipe2: tirsCadres2,
    cartons_jaunes_equipe1: randomInRange(0, 3),
    cartons_jaunes_equipe2: randomInRange(0, 3),
    cartons_rouges_equipe1: randomInRange(0, 1),
    cartons_rouges_equipe2: randomInRange(0, 1),
    passes_reussies_equipe1: passes1,
    passes_reussies_equipe2: passes2,
    coups_francs_equipe1: randomInRange(3, 8),
    coups_francs_equipe2: randomInRange(3, 8),
    corners_equipe1: randomInRange(3, 8),
    corners_equipe2: randomInRange(3, 8),
    fautes_equipe1: randomInRange(8, 15),
    fautes_equipe2: randomInRange(8, 15)
  };
}