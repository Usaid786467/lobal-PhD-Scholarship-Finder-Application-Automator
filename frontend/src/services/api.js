/**
 * API Service
 * Centralized API calls to backend
 */
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getProfile: () => api.get('/api/auth/profile'),
  updateProfile: (data) => api.put('/api/auth/profile', data),
};

// Universities API
export const universitiesAPI = {
  search: (params) => api.get('/api/universities/search', { params }),
  discover: (data) => api.post('/api/universities/discover', data),
  getOne: (id) => api.get(`/api/universities/${id}`),
  getCountries: () => api.get('/api/universities/countries'),
  getStats: () => api.get('/api/universities/stats'),
};

// Professors API
export const professorsAPI = {
  search: (params) => api.get('/api/professors/search', { params }),
  discover: (data) => api.post('/api/professors/discover', data),
  getOne: (id) => api.get(`/api/professors/${id}`),
  getStats: () => api.get('/api/professors/stats'),
};

// Emails API
export const emailsAPI = {
  generate: (data) => api.post('/api/emails/generate', data),
  getBatches: () => api.get('/api/emails/batches'),
  getBatch: (id) => api.get(`/api/emails/batches/${id}`),
  approveBatch: (id) => api.post(`/api/emails/batches/${id}/approve`),
  sendBatch: (id) => api.post(`/api/emails/batches/${id}/send`),
  updateEmail: (id, data) => api.put(`/api/emails/${id}`, data),
};

// Applications API
export const applicationsAPI = {
  getAll: (params) => api.get('/api/applications', { params }),
  getOne: (id) => api.get(`/api/applications/${id}`),
  update: (id, data) => api.put(`/api/applications/${id}`, data),
  getStats: () => api.get('/api/applications/stats'),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics/dashboard'),
  getTimeline: (params) => api.get('/api/analytics/timeline', { params }),
  getUniversityStats: () => api.get('/api/analytics/universities'),
  getProfessorStats: () => api.get('/api/analytics/professors'),
};

export default api;
