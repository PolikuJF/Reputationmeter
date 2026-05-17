import axios from 'axios';
import axiosRetry from 'axios-retry';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Перехватчик для JWT
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Настройка ретраев для устойчивости к недоступности сервера 
axiosRetry(apiClient, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay, // экспоненциальная задержка
  retryCondition: (error) => {
    // Повторяем только GET запросы при сетевых ошибках или 5xx
    return axiosRetry.isNetworkOrIdempotentRequestError(error) &&
           error.config?.method?.toUpperCase() === 'GET';
  },
  onRetry: (retryCount, error, requestConfig) => {
    console.warn(`Retry attempt ${retryCount} for ${requestConfig.url} due to`, error.message);
  },
});