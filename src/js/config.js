// Configuration de l'environnement
const isDev = import.meta.env.DEV;

// Configuration de l'API
export const API_URL = isDev 
  ? 'http://localhost:5000'
  : import.meta.env.VITE_API_URL;

// Intervalles de rafraîchissement
export const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes

// Configuration des requêtes
export const API_CONFIG = {
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
};