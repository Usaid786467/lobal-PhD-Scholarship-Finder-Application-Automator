import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  logout: () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  },
  getCurrentUser: () => api.get('/api/auth/me'),
};

// Scholarships API calls
export const scholarshipsAPI = {
  getAll: (params) => api.get('/api/scholarships', { params }),
  getById: (id) => api.get(`/api/scholarships/${id}`),
  search: (searchParams) => api.post('/api/scholarships/search', searchParams),
};

// Applications API calls
export const applicationsAPI = {
  getAll: () => api.get('/api/applications'),
  getById: (id) => api.get(`/api/applications/${id}`),
  create: (applicationData) => api.post('/api/applications', applicationData),
  update: (id, applicationData) => api.put(`/api/applications/${id}`, applicationData),
  delete: (id) => api.delete(`/api/applications/${id}`),
  getStats: () => api.get('/api/applications/stats'),
};

// Documents API calls
export const documentsAPI = {
  upload: (formData) => api.post('/api/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getAll: () => api.get('/api/documents'),
  delete: (id) => api.delete(`/api/documents/${id}`),
};

export default api;
