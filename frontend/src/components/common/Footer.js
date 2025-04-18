import React from 'react';
import '../../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="container">
        <div className="footer-content">
          <p>&copy; {new Date().getFullYear()} WikiExplorer. All rights reserved.</p>
          <div className="footer-links">
            <a href="#terms">Terms of Service</a>
            <a href="#privacy">Privacy Policy</a>
            <a href="#about">About</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
