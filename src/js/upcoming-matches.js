import { fetchUpcomingMatches } from './api.js';
import { formatMatchDate } from './utils/date-formatter.js';
import { REFRESH_INTERVAL } from './config.js';

function updateUpcomingMatches(matches) {
  const container = document.getElementById('upcoming-matches');
  
  if (!matches?.length) {
    container.innerHTML = '<p class="text-gray-500">Aucun match à venir</p>';
    return;
  }

  container.innerHTML = matches.map(match => `
    <div class="bg-white rounded-lg shadow p-4 mb-4">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-blue-600">${match.competition || ''}</span>
        <span class="text-sm text-gray-500">${formatMatchDate(match.date)}</span>
      </div>
      <div class="flex justify-between items-center">
        <div class="flex-1 text-right">
          <span class="font-semibold">${match.homeTeam || ''}</span>
        </div>
        <div class="mx-4 font-bold text-gray-600">VS</div>
        <div class="flex-1 text-left">
          <span class="font-semibold">${match.awayTeam || ''}</span>
        </div>
      </div>
    </div>
  `).join('');
}

async function initUpcomingMatches() {
  try {
    const matches = await fetchUpcomingMatches();
    updateUpcomingMatches(matches);
    
    setInterval(async () => {
      const updatedMatches = await fetchUpcomingMatches();
      updateUpcomingMatches(updatedMatches);
    }, REFRESH_INTERVAL);
  } catch (error) {
    console.error('Error initializing upcoming matches:', error);
    updateUpcomingMatches([]);
  }
}

document.addEventListener('DOMContentLoaded', initUpcomingMatches);