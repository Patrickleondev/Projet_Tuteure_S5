import { API_URL, API_CONFIG } from '../config.js';

/**
 * Service pour gérer les appels API
 */
class ApiService {
  constructor(baseURL = API_URL, config = API_CONFIG) {
    this.baseURL = baseURL;
    this.config = config;
  }

  async fetch(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...this.config,
        ...options,
        headers: {
          ...this.config.headers,
          ...options.headers
        }
      });

      const data = await response.json();

      if (!response.ok || data.status === 'error') {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Méthodes spécifiques aux endpoints
  async getUpcomingMatches() {
    return this.fetch('/api/upcoming-matches');
  }

  async predictMatch(league, team1, team2) {
    if (!league || !team1 || !team2) {
      throw new Error('Tous les paramètres sont requis');
    }

    return this.fetch('/api/predict', {
      method: 'POST',
      body: JSON.stringify({ league, team1, team2 })
    });
  }
}

export const apiService = new ApiService();