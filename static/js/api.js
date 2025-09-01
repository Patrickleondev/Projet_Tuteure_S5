const API_URL = 'http://localhost:5000';

export const fetchUpcomingMatches = async () => {
    try {
        const response = await fetch(`${API_URL}/api/upcoming-matches`);
        if (!response.ok) throw new Error('Erreur réseau');
        return await response.json();
    } catch (error) {
        console.error('Erreur:', error);
        return [];
    }
};

export const predictMatch = async (league, team1, team2) => {
    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ league, team1, team2 })
        });
        if (!response.ok) throw new Error('Erreur réseau');
        return await response.json();
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
};