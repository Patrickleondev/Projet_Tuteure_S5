// Statistiques des équipes par championnat
export const TEAM_STATS = {
  clubs: {
    // Structure pour les statistiques des clubs
    template: {
      general: {
        matchs_joues: 0,
        victoires: 0,
        nuls: 0,
        defaites: 0,
        buts_marques: 0,
        buts_encaisses: 0,
        points: 0,
        classement: 0
      },
      domicile: {
        matchs_joues: 0,
        victoires: 0,
        nuls: 0,
        defaites: 0,
        buts_marques: 0,
        buts_encaisses: 0
      },
      exterieur: {
        matchs_joues: 0,
        victoires: 0,
        nuls: 0,
        defaites: 0,
        buts_marques: 0,
        buts_encaisses: 0
      },
      discipline: {
        cartons_jaunes: 0,
        cartons_rouges: 0,
        fautes_commises: 0,
        fautes_subies: 0
      },
      jeu: {
        possession_moyenne: 0,
        passes_reussies: 0,
        precision_passes: 0,
        tirs: 0,
        tirs_cadres: 0,
        corners: 0,
        hors_jeu: 0
      },
      coups_de_pied_arretes: {
        penalties_marques: 0,
        penalties_concedes: 0,
        coups_francs_marques: 0,
        coups_francs_concedes: 0
      }
    }
  },
  nations: {
    // Structure pour les statistiques des équipes nationales
    template: {
      general: {
        matchs_joues: 0,
        victoires: 0,
        nuls: 0,
        defaites: 0,
        buts_marques: 0,
        buts_encaisses: 0,
        points_fifa: 0,
        classement_fifa: 0
      },
      competitions: {
        participations_coupe_monde: 0,
        meilleur_resultat_coupe_monde: '',
        participations_competition_continentale: 0,
        meilleur_resultat_competition_continentale: ''
      },
      discipline: {
        cartons_jaunes: 0,
        cartons_rouges: 0,
        fautes_commises: 0,
        fautes_subies: 0
      },
      jeu: {
        possession_moyenne: 0,
        passes_reussies: 0,
        precision_passes: 0,
        tirs: 0,
        tirs_cadres: 0,
        corners: 0,
        hors_jeu: 0
      },
      coups_de_pied_arretes: {
        penalties_marques: 0,
        penalties_concedes: 0,
        coups_francs_marques: 0,
        coups_francs_concedes: 0
      }
    }
  },
  // Premier League
  'manchester_city': {
    possession_moyenne: 65.7,
    precision_passes: 90.1,
    tirs_par_match: 17.2
  },
  'liverpool': {
    possession_moyenne: 61.2,
    precision_passes: 85.9,
    tirs_par_match: 16.4
  },
  'arsenal': {
    possession_moyenne: 59.4,
    precision_passes: 86.8,
    tirs_par_match: 15.9
  },
  'manchester_united': {
    possession_moyenne: 56.8,
    precision_passes: 84.7,
    tirs_par_match: 14.8
  },
  
  // La Liga
  'real_madrid': {
    possession_moyenne: 59.8,
    precision_passes: 88.5,
    tirs_par_match: 16.2
  },
  'barcelona': {
    possession_moyenne: 64.2,
    precision_passes: 89.1,
    tirs_par_match: 15.8
  },
  'atletico_madrid': {
    possession_moyenne: 52.4,
    precision_passes: 83.8,
    tirs_par_match: 13.7
  },
  
  // Ligue 1
  'psg': {
    possession_moyenne: 63.5,
    precision_passes: 89.2,
    tirs_par_match: 15.3
  },
  'marseille': {
    possession_moyenne: 58.2,
    precision_passes: 85.7,
    tirs_par_match: 13.5
  }
};