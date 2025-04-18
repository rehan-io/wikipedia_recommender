import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      checkAuthStatus(token);
    } else {
      setLoading(false);
    }
  }, []);

  const checkAuthStatus = async (token) => {
    try {
      const response = await api.get('/users/me/', {
        headers: { Authorization: `Token ${token}` }
      });
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      localStorage.removeItem('authToken');
      setError('Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    setLoading(true);
    try {
      const response = await api.post('/auth/token/', credentials);
      const { token } = response.data;
      localStorage.setItem('authToken', token);
      await checkAuthStatus(token);
      return true;
    } catch (error) {
      setError('Login failed: ' + (error.response?.data?.detail || 'Unknown error'));
      setLoading(false);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setUser(null);
    setIsAuthenticated(false);
  };

  const signup = async (userData) => {
    setLoading(true);
    try {
      await api.post('/users/', userData);
      const success = await login({
        username: userData.username,
        password: userData.password
      });
      return success;
    } catch (error) {
      setError('Signup failed: ' + (error.response?.data?.detail || 'Unknown error'));
      setLoading(false);
      return false;
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    signup
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
