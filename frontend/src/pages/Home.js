import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Home.css';

const Home = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/articles?count=5&page=${page}`);
      if (response.data && response.data.articles) {
        setArticles(prev => [...prev, ...response.data.articles]);
        setPage(prev => prev + 1);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching articles:', err);
      setError('Failed to load articles. Please try again.');
      setLoading(false);
    }
  };

  // Infinite scroll handler
  useEffect(() => {
    const handleScroll = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !loading) {
        fetchArticles();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loading]);

  return (
    <div className="home-container">
      <div className="header">
        <h1>Wikipedia Explorer</h1>
        <p>Discover interesting Wikipedia articles</p>
      </div>
      
      <div className="articles-container">
        {articles.map((article, index) => (
          <div className="article" key={index}>
            <h2>{article.title}</h2>
            {article.thumbnail && (
              <img src={article.thumbnail} alt={article.title} className="article-image" />
            )}
            <div className="article-extract">{article.extract}</div>
            {article.url && (
              <a href={article.url} className="article-link" target="_blank" rel="noreferrer">
                Read more on Wikipedia
              </a>
            )}
          </div>
        ))}
      </div>
      
      {loading && (
        <div className="loading">
          <p>Loading more articles...</p>
        </div>
      )}
      
      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default Home;
