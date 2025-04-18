import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { userApi, fetchCsrfToken } from '../services/api';
import '../styles/Auth.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Fetch CSRF token when component mounts
  useEffect(() => {
    const getCsrfToken = async () => {
      try {
        await fetchCsrfToken();
        console.log('CSRF token fetched successfully');
      } catch (error) {
        console.error('Failed to fetch CSRF token:', error);
      }
    };
    
    getCsrfToken();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    const { username, email, password, confirmPassword } = formData;
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    try {
      setLoading(true);
      
      // Make sure we have a fresh CSRF token
      await fetchCsrfToken();
      
      // Submit the signup request with CSRF token
      await userApi.signup({ username, email, password });
      
      // Login after successful signup
      const loginResponse = await userApi.login({ username, password });
      localStorage.setItem('authToken', loginResponse.data.token);
      
      navigate('/');
    } catch (err) {
      console.error('Signup error:', err);
      
      // Error handling logic
      let errorMessage = 'Registration failed: ';
      
      if (err.response?.data) {
        const errors = err.response.data;
        
        if (typeof errors === 'string') {
          errorMessage += errors;
        } else if (typeof errors === 'object') {
          const fieldErrors = [];
          
          for (const field in errors) {
            if (errors[field]) {
              const message = Array.isArray(errors[field]) 
                ? errors[field].join(' ')
                : String(errors[field]);
              
              fieldErrors.push(`${field}: ${message}`);
            }
          }
          
          errorMessage += fieldErrors.join(', ');
        }
      } else {
        errorMessage += 'An unknown error occurred';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h2>Sign Up</h2>
        
        {error && <div className="alert alert-danger">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              type="email"
              className="form-control"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
            <input
              type="password"
              className="form-control"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>
          
          <button 
            type="submit" 
            className="btn btn-primary w-100"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>
        
        <div className="mt-3 text-center">
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;
