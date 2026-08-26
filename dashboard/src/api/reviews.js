import { apiRequest } from './client';

export async function submitHumanReview(reviewData) {
  return await apiRequest('/review', {
    method: 'POST',
    body: JSON.stringify(reviewData),
  });
}

export async function fetchReviewHistory() {
  return await apiRequest('/review/history');
}

export async function fetchAiResponsesLog() {
  return await apiRequest('/logs/ai-responses');
}

export async function fetchCorrectionsLog() {
  return await apiRequest('/logs/corrections');
}
