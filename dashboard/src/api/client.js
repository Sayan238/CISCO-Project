// Centralized API client for NetSage-AI

const BASE_URL = 'http://127.0.0.1:8000/api';
const FALLBACK_URL = '/api';

export async function apiRequest(endpoint, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    try {
      const fallbackResponse = await fetch(`${FALLBACK_URL}${endpoint}`, config);
      if (!fallbackResponse.ok) {
        throw new Error(`Fallback API Error: ${fallbackResponse.status}`);
      }
      return await fallbackResponse.json();
    } catch (fallbackError) {
      console.error(`API Fetch Error [${endpoint}]:`, error);
      throw error;
    }
  }
}
