import React from 'react';
import '../../styles/Spinner.css';

const Spinner = ({ message = 'Loading...' }) => {
  return (
    <div className="spinner-container">
      <div className="spinner">
        <div className="cube1"></div>
        <div className="cube2"></div>
      </div>
      <p className="spinner-message">{message}</p>
    </div>
  );
};

export default Spinner;
