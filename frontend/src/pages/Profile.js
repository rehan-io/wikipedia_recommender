import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Profile.css';

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          throw new Error('Not authenticated');
        }

        const response = await axios.get('/api/users/profile/', {
          headers: {
            'Authorization': `Token ${authToken}`
          }
        });

        setUserData(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching user profile:', err);
        setError('Failed to load profile data');
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return (
      <div className="profile-loading">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading your profile...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-error">
        <div className="alert alert-danger">{error}</div>
        <button 
          className="btn btn-primary" 
          onClick={() => window.location.reload()}
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Your Profile</h1>
        {userData && (
          <div className="profile-info">
            <p><strong>Username:</strong> {userData.username}</p>
            <p><strong>Email:</strong> {userData.email}</p>
            <p><strong>Member since:</strong> {new Date(userData.date_joined).toLocaleDateString()}</p>
          </div>
        )}
      </div>

      <div className="profile-actions">
        <button className="btn btn-primary">Edit Profile</button>
        <button 
          className="btn btn-danger"
          onClick={() => {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Profile;
