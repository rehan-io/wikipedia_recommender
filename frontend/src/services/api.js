import axios from 'axios';

// Function to get CSRF token from cookies
const getCsrfToken = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
};

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  withCredentials: true, // Important for cookies (including CSRF)
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor to add auth token and CSRF token
api.interceptors.request.use(
  async (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    
    // Add CSRF token for non-GET requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
      const csrfToken = getCsrfToken();
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// Fetch CSRF token explicitly
export const fetchCsrfToken = async () => {
  try {
    const response = await axios.get('/api/csrf/', { withCredentials: true });
    return response.data.csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    throw error;
  }
};

// User-related API endpoints
export const userApi = {
  signup: (userData) => api.post('/users/', userData),
  login: (credentials) => api.post('/auth/token/', credentials),
  getProfile: () => api.get('/users/profile/'),
};

// Article-related API endpoints
export const articleApi = {
  getRecommended: () => api.get('/articles/recommended/'),
  getTrending: () => api.get('/articles/trending/'),
  search: (query) => api.get(`/articles/search/?q=${encodeURIComponent(query)}`),
  like: (articleId) => api.post(`/articles/${articleId}/like/`),
};

export default api;
