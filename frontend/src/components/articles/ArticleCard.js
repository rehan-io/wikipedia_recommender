import React, { useState } from 'react';
import { toggleLikeArticle } from '../../services/api';
import '../../styles/ArticleCard.css';

const ArticleCard = ({ article }) => {
  const [isLiked, setIsLiked] = useState(article.is_liked);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleLike = async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await toggleLikeArticle(article.id);
      setIsLiked(response.liked);
    } catch (error) {
      console.error('Error toggling like:', error);
      alert('Could not update like status. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const createPlaceholder = () => {
    return (
      <div className="article-placeholder-image">
        {article.title.charAt(0).toUpperCase()}
      </div>
    );
  };

  return (
    <div className="article-card" data-article-id={article.id}>
      {/* Image container */}
      <div>
        {article.image_url ? (
          <img 
            src={article.image_url} 
            alt={article.title} 
            className="article-image"
            onError={(e) => {
              e.target.parentNode.replaceWith(createPlaceholder());
            }}
          />
        ) : (
          createPlaceholder()
        )}
      </div>
      
      {/* Article body */}
      <div className="article-body">
        <h5 className="article-title">{article.title}</h5>
        <p className="article-summary">{article.summary}</p>
        
        {/* Actions */}
        <div className="d-flex justify-content-between align-items-center">
          <a 
            href={article.url} 
            className="btn btn-sm btn-outline-primary"
            target="_blank" 
            rel="noopener noreferrer"
          >
            Read More
          </a>
          
          <button
            className={`like-button ${isLiked ? 'liked' : 'not-liked'}`}
            aria-label={isLiked ? 'Unlike this article' : 'Like this article'}
            onClick={handleToggleLike}
            disabled={isLoading}
          >
            ❤
          </button>
        </div>
      </div>
    </div>
  );
};

export default ArticleCard;
