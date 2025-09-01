// Error handling utilities
export function handleApiError(error, fallback = []) {
  console.error('API Error:', error.message);
  return fallback;
}

export function showUserError(message) {
  const errorMessage = message || 'Une erreur est survenue. Veuillez réessayer.';
  console.error(errorMessage);
  alert(errorMessage);
}