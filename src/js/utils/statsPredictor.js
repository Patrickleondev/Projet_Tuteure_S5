// Utilitaire de prédiction des statistiques
export function generateMatchStats(team1Stats, team2Stats) {
  // Fonction utilitaire pour générer un nombre aléatoire dans une plage
  const randomInRange = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
  
  // Fonction pour ajouter une légère variation aux statistiques
  const addVariation = (value, variance = 0.2) => {
    const variation = value * variance;
    return Math.round(value + (Math.random() * variation * 2 - variation));
  };

  // Calcul du ratio de force entre les équipes
  const team1Strength = (team1Stats.possession_moyenne + team1Stats.precision_passes) / 2;
  const team2Strength = (team2Stats.possession_moyenne + team2Stats.precision_passes) / 2;
  const strengthRatio = team1Strength / team2Strength;

  // Génération des statistiques de base
  const possession1 = Math.round(50 * strengthRatio);
  const possession2 = 100 - possession1;

  // Génération des tirs
  const tirs1 = addVariation(team1Stats.tirs_par_match * strengthRatio);
  const tirs2 = addVariation(team2Stats.tirs_par_match / strengthRatio);
  
  // Calcul des tirs cadrés (environ 40% des tirs totaux)
  const tirsCadres1 = Math.round(tirs1 * 0.4);
  const tirsCadres2 = Math.round(tirs2 * 0.4);

  // Prédiction des buts (basé sur les tirs cadrés et la précision)
  const buts1 = Math.min(tirsCadres1, randomInRange(0, Math.ceil(tirsCadres1 * 0.5)));
  const buts2 = Math.min(tirsCadres2, randomInRange(0, Math.ceil(tirsCadres2 * 0.5)));

  return {
    buts_equipe1: buts1,
    buts_equipe2: buts2,
    possession_equipe1: possession1,
    possession_equipe2: possession2,
    tirs_equipe1: tirs1,
    tirs_equipe2: tirs2,
    tirs_cadres_equipe1: tirsCadres1,
    tirs_cadres_equipe2: tirsCadres2,
    cartons_jaunes_equipe1: randomInRange(0, 3),
    cartons_jaunes_equipe2: randomInRange(0, 3),
    cartons_rouges_equipe1: randomInRange(0, 1),
    cartons_rouges_equipe2: randomInRange(0, 1),
    passes_reussies_equipe1: addVariation(450 * strengthRatio),
    passes_reussies_equipe2: addVariation(450 / strengthRatio),
    coups_francs_equipe1: randomInRange(3, 8),
    coups_francs_equipe2: randomInRange(3, 8),
    corners_equipe1: randomInRange(3, 8),
    corners_equipe2: randomInRange(3, 8),
    fautes_equipe1: randomInRange(8, 15),
    fautes_equipe2: randomInRange(8, 15)
  };
}