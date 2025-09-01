/**
 * Script de prédiction des matchs
 * Amélioration de l'interface utilisateur
 */

class PredictionInterface {
    constructor() {
        this.selectedCompetition = null;
        this.teams = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadCompetitions();
    }

    bindEvents() {
        // Sélection de compétition
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('competition-btn')) {
                this.selectCompetition(e.target.dataset.competition);
            }
        });

        // Formulaire de prédiction
        const form = document.getElementById('prediction-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitPrediction();
            });
        }

        // Changement d'équipe
        const homeSelect = document.getElementById('equipe-domicile');
        const awaySelect = document.getElementById('equipe-exterieur');
        
        if (homeSelect) {
            homeSelect.addEventListener('change', () => this.updateTeamComparison());
        }
        if (awaySelect) {
            awaySelect.addEventListener('change', () => this.updateTeamComparison());
        }
    }

    selectCompetition(competitionId) {
        // Retirer la sélection précédente
        document.querySelectorAll('.competition-btn').forEach(btn => {
            btn.classList.remove('bg-blue-600', 'text-white');
            btn.classList.add('bg-gray-700', 'hover:bg-gray-600');
        });

        // Sélectionner la nouvelle compétition
        const selectedBtn = document.querySelector(`[data-competition="${competitionId}"]`);
        if (selectedBtn) {
            selectedBtn.classList.remove('bg-gray-700', 'hover:bg-gray-600');
            selectedBtn.classList.add('bg-blue-600', 'text-white');
        }

        this.selectedCompetition = competitionId;
        this.loadTeams(competitionId);
        
        // Animation de transition
        this.showTeamSelection();
    }

    showTeamSelection() {
        const teamSelection = document.getElementById('team-selection');
        if (teamSelection) {
            teamSelection.classList.remove('hidden');
            teamSelection.style.opacity = '0';
            teamSelection.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                teamSelection.style.transition = 'all 0.3s ease';
                teamSelection.style.opacity = '1';
                teamSelection.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    async loadCompetitions() {
        try {
            const response = await fetch('/api/competitions');
            const competitions = await response.json();
            console.log('Compétitions chargées:', competitions);
        } catch (error) {
            console.error('Erreur lors du chargement des compétitions:', error);
        }
    }

    async loadTeams(competitionId) {
        try {
            const response = await fetch(`/api/teams/${competitionId}`);
            const teams = await response.json();
            
            this.teams[competitionId] = teams;
            this.populateTeamSelects(teams);
            
        } catch (error) {
            console.error('Erreur lors du chargement des équipes:', error);
            // Utiliser des équipes par défaut
            this.populateTeamSelects(this.getDefaultTeams(competitionId));
        }
    }

    getDefaultTeams(competitionId) {
        const defaultTeams = {
            'cl': [
                {id: 'Real Madrid', name: 'Real Madrid'},
                {id: 'Barcelona', name: 'Barcelona'},
                {id: 'Manchester City', name: 'Manchester City'},
                {id: 'Liverpool', name: 'Liverpool'},
                {id: 'Bayern Munich', name: 'Bayern Munich'},
                {id: 'PSG', name: 'PSG'}
            ],
            'fr.1': [
                {id: 'PSG', name: 'PSG'},
                {id: 'Marseille', name: 'Marseille'},
                {id: 'Lyon', name: 'Lyon'},
                {id: 'Lille', name: 'Lille'},
                {id: 'Monaco', name: 'Monaco'},
                {id: 'Rennes', name: 'Rennes'}
            ],
            'world_cup': [
                {id: 'France', name: 'France'},
                {id: 'Brazil', name: 'Brazil'},
                {id: 'Argentina', name: 'Argentina'},
                {id: 'England', name: 'England'},
                {id: 'Spain', name: 'Spain'},
                {id: 'Germany', name: 'Germany'}
            ]
        };
        
        return defaultTeams[competitionId] || defaultTeams['cl'];
    }

    populateTeamSelects(teams) {
        const homeSelect = document.getElementById('equipe-domicile');
        const awaySelect = document.getElementById('equipe-exterieur');
        
        if (homeSelect && awaySelect) {
            // Vider les selects
            homeSelect.innerHTML = '<option value="">Sélectionnez une équipe</option>';
            awaySelect.innerHTML = '<option value="">Sélectionnez une équipe</option>';
            
            // Ajouter les équipes
            teams.forEach(team => {
                const homeOption = document.createElement('option');
                homeOption.value = team.id;
                homeOption.textContent = team.name;
                homeSelect.appendChild(homeOption);
                
                const awayOption = document.createElement('option');
                awayOption.value = team.id;
                awayOption.textContent = team.name;
                awaySelect.appendChild(awayOption);
            });
        }
    }

    updateTeamComparison() {
        const homeTeam = document.getElementById('equipe-domicile').value;
        const awayTeam = document.getElementById('equipe-exterieur').value;
        
        if (homeTeam && awayTeam && homeTeam !== awayTeam) {
            // Activer le bouton de prédiction
            const submitBtn = document.querySelector('#prediction-form button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }
    }

    async submitPrediction() {
        const homeTeam = document.getElementById('equipe-domicile').value;
        const awayTeam = document.getElementById('equipe-exterieur').value;
        
        if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
            this.showError('Veuillez sélectionner deux équipes différentes');
            return;
        }

        // Afficher le loading
        this.showLoading();

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    equipe_domicile: homeTeam,
                    equipe_exterieur: awayTeam,
                    type: this.getCompetitionType(),
                    competition: this.selectedCompetition
                })
            });

            const result = await response.json();

            if (result.error) {
                this.showError(result.error);
            } else {
                this.displayResults(result);
            }

        } catch (error) {
            console.error('Erreur lors de la prédiction:', error);
            this.showError('Erreur lors de la prédiction. Veuillez réessayer.');
        } finally {
            this.hideLoading();
        }
    }

    getCompetitionType() {
        const clubCompetitions = ['cl', 'en.1', 'es.1', 'de.1', 'it.1', 'fr.1'];
        return clubCompetitions.includes(this.selectedCompetition) ? 'clubs' : 'nations';
    }

    showLoading() {
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        
        if (loading) loading.classList.remove('hidden');
        if (results) results.classList.add('hidden');
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) loading.classList.add('hidden');
    }

    showError(message) {
        // Créer une notification d'erreur
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Supprimer après 5 secondes
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    displayResults(result) {
        const resultsDiv = document.getElementById('results');
        if (!resultsDiv) return;

        // Masquer le formulaire
        const form = document.getElementById('prediction-form');
        if (form) form.classList.add('hidden');

        // Afficher les résultats
        resultsDiv.classList.remove('hidden');
        
        // Animation d'entrée
        resultsDiv.style.opacity = '0';
        resultsDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            resultsDiv.style.transition = 'all 0.5s ease';
            resultsDiv.style.opacity = '1';
            resultsDiv.style.transform = 'translateY(0)';
        }, 100);

        // Mettre à jour le contenu
        this.updateResultsContent(result);
        this.createCharts(result);
    }

    updateResultsContent(result) {
        // Score prédit
        const scoreElement = document.getElementById('predicted-score');
        if (scoreElement && result.buts_equipe1 !== undefined && result.buts_equipe2 !== undefined) {
            scoreElement.textContent = `${result.equipe_domicile} ${result.buts_equipe1} - ${result.buts_equipe2} ${result.equipe_exterieur}`;
        }

        // Résultat
        const resultElement = document.getElementById('predicted-result');
        if (resultElement && result.resultat) {
            resultElement.textContent = result.resultat;
        }

        // Modèle utilisé
        const modelElement = document.getElementById('model-used');
        if (modelElement && result.modele_utilise) {
            modelElement.textContent = result.modele_utilise;
        }

        // Statistiques des équipes
        if (result.statistiques) {
            this.updateTeamStats(result.statistiques);
        }
    }

    updateTeamStats(stats) {
        // Statistiques équipe domicile
        if (stats.domicile) {
            this.updateTeamStatsSection('equipe-domicile', stats.domicile);
        }
        
        // Statistiques équipe extérieur
        if (stats.exterieur) {
            this.updateTeamStatsSection('equipe-exterieur', stats.exterieur);
        }
    }

    updateTeamStatsSection(teamId, stats) {
        // Statistiques générales
        const generalDiv = document.getElementById(`${teamId}-general`);
        if (generalDiv) {
            generalDiv.innerHTML = `
                <div class="flex justify-between">
                    <span>Buts marqués:</span>
                    <span class="font-semibold">${stats.buts_marques?.toFixed(1) || 'N/A'}</span>
                </div>
                <div class="flex justify-between">
                    <span>Buts encaissés:</span>
                    <span class="font-semibold">${stats.buts_encaisses?.toFixed(1) || 'N/A'}</span>
                </div>
                <div class="flex justify-between">
                    <span>Points par match:</span>
                    <span class="font-semibold">${stats.points_par_match?.toFixed(1) || 'N/A'}</span>
                </div>
            `;
        }

        // Discipline
        const disciplineDiv = document.getElementById(`${teamId}-discipline`);
        if (disciplineDiv && stats.discipline) {
            disciplineDiv.innerHTML = `
                <div class="flex justify-between">
                    <span>Cartons jaunes:</span>
                    <span class="font-semibold">${stats.discipline.cartons_jaunes?.toFixed(1) || 'N/A'}</span>
                </div>
                <div class="flex justify-between">
                    <span>Cartons rouges:</span>
                    <span class="font-semibold">${stats.discipline.cartons_rouges?.toFixed(1) || 'N/A'}</span>
                </div>
            `;
        }

        // Jeu
        const jeuDiv = document.getElementById(`${teamId}-jeu`);
        if (jeuDiv && stats.jeu) {
            jeuDiv.innerHTML = `
                <div class="flex justify-between">
                    <span>Possession:</span>
                    <span class="font-semibold">${stats.jeu.possession_moyenne?.toFixed(1) || 'N/A'}%</span>
                </div>
                <div class="flex justify-between">
                    <span>Passes réussies:</span>
                    <span class="font-semibold">${stats.jeu.passes_reussies?.toFixed(1) || 'N/A'}</span>
                </div>
                <div class="flex justify-between">
                    <span>Précision passes:</span>
                    <span class="font-semibold">${stats.jeu.precision_passes?.toFixed(1) || 'N/A'}%</span>
                </div>
            `;
        }
    }

    createCharts(result) {
    // Graphique des probabilités
        this.createProbabilityChart(result);
        
        // Graphique de forme récente
        this.createFormChart(result);
        
        // Graphique des confrontations directes
        this.createH2HChart(result);
    }

    createProbabilityChart(result) {
        const ctx = document.getElementById('probabilities-chart');
        if (!ctx) return;

        const data = {
            labels: ['Victoire domicile', 'Match nul', 'Victoire extérieur'],
            datasets: [{
                data: [
                    result.victoire_domicile || 0.33,
                    result.match_nul || 0.33,
                    result.victoire_exterieur || 0.33
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(156, 163, 175, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(59, 130, 246, 1)',
                    'rgba(156, 163, 175, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        };

        new Chart(ctx, {
            type: 'doughnut',
            data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                            color: 'white'
                    }
                }
            }
        }
    });
    }

    createFormChart(result) {
        const ctx = document.getElementById('form-chart');
        if (!ctx || !result.statistiques) return;

        const homeForm = result.statistiques.domicile?.forme || { victoires: 0.33, nuls: 0.33, defaites: 0.34 };
        const awayForm = result.statistiques.exterieur?.forme || { victoires: 0.33, nuls: 0.33, defaites: 0.34 };

        const data = {
            labels: ['Victoires', 'Nuls', 'Défaites'],
            datasets: [
                {
                    label: result.equipe_domicile,
                    data: [homeForm.victoires, homeForm.nuls, homeForm.defaites],
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2
                },
                {
                    label: result.equipe_exterieur,
                    data: [awayForm.victoires, awayForm.nuls, awayForm.defaites],
                    backgroundColor: 'rgba(239, 68, 68, 0.5)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 2
                }
            ]
        };

        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
                },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'white'
                    }
                },
                x: {
                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });
}

    createH2HChart(result) {
        const ctx = document.getElementById('h2h-chart');
        if (!ctx || !result.statistiques?.confrontations_directes) return;

        const h2h = result.statistiques.confrontations_directes;

        const data = {
            labels: ['Victoires domicile', 'Nuls', 'Victoires extérieur'],
            datasets: [{
                data: [
                    h2h.victoires_domicile || 0.33,
                    h2h.nuls || 0.33,
                    h2h.victoires_exterieur || 0.33
                ],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(156, 163, 175, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(34, 197, 94, 1)',
                    'rgba(156, 163, 175, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        };

        new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'white'
                        }
                    }
                }
            }
        });
    }
}

// Initialisation quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    new PredictionInterface();
}); 