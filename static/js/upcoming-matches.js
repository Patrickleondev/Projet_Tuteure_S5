import { fetchUpcomingMatches } from './api.js';

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function updateUpcomingMatches(matches) {
    const container = document.getElementById('upcoming-matches');
    
    if (!matches?.length) {
        container.innerHTML = '<p class="text-gray-500">Aucun match à venir</p>';
        return;
    }

    container.innerHTML = matches.map(match => `
        <div class="bg-white rounded-lg shadow p-4 mb-4">
            <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-medium text-blue-600">${match.competition}</span>
                <span class="text-sm text-gray-500">${formatDate(match.date)}</span>
            </div>
            <div class="flex justify-between items-center">
                <div class="flex-1 text-right">
                    <span class="font-semibold">${match.homeTeam}</span>
                </div>
                <div class="mx-4 font-bold text-gray-600">VS</div>
                <div class="flex-1 text-left">
                    <span class="font-semibold">${match.awayTeam}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const matches = await fetchUpcomingMatches();
        updateUpcomingMatches(matches);
        
        // Rafraîchir toutes les 5 minutes
        setInterval(async () => {
            const updatedMatches = await fetchUpcomingMatches();
            updateUpcomingMatches(updatedMatches);
        }, 5 * 60 * 1000);
    } catch (error) {
        console.error('Erreur:', error);
        updateUpcomingMatches([]);
    }
});