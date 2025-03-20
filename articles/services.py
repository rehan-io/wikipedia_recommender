import wikipedia
import requests
import json
import numpy as np
# from sentence_transformers import SentenceTransformer
from .models import WikipediaArticle, UserArticleInteraction
import logging

# Set up logging
logger = logging.getLogger(__name__)

class WikipediaService:
    @staticmethod
    def search_articles(query, limit=10):
        """Search for Wikipedia articles based on query"""
        try:
            # Check if wikipedia package is available
            if not hasattr(wikipedia, 'search'):
                logger.error("Wikipedia package not properly imported")
                # Fallback to a basic search using the API directly
                return WikipediaService._fallback_search(query, limit)
                
            search_results = wikipedia.search(query, results=limit)
            
            # If no results found, return empty list
            if not search_results:
                logger.info(f"No Wikipedia results found for query: {query}")
                return []
                
            articles = []
            
            for title in search_results:
                try:
                    # Use auto_suggest=False to avoid redirects
                    page = wikipedia.page(title, auto_suggest=False)
                    
                    # Get page image if available
                    image_url = None
                    if hasattr(page, 'images') and page.images:
                        # Filter for common image formats
                        images = [img for img in page.images if any(
                            ext in img.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg'])]
                        if images:
                            image_url = images[0]
                    
                    # Create article dictionary with safe handling of attributes
                    article = {
                        'article_id': str(page.pageid),  # Ensure it's a string
                        'title': page.title,
                        'summary': page.summary[:500] + '...' if len(page.summary) > 500 else page.summary,
                        'url': page.url,
                        'image_url': image_url,
                        'categories': ', '.join(page.categories[:5]) if hasattr(page, 'categories') and page.categories else ''
                    }
                    articles.append(article)
                except wikipedia.exceptions.DisambiguationError as e:
                    # Instead of failing, try to get the first option from the disambiguation list
                    logger.info(f"Disambiguation for '{title}': {e.options[:5]}")
                    
                    # Try the first option if available
                    if e.options:
                        try:
                            specific_title = e.options[0]
                            specific_page = wikipedia.page(specific_title, auto_suggest=False)
                            
                            # Get page image if available
                            image_url = None
                            if hasattr(specific_page, 'images') and specific_page.images:
                                images = [img for img in specific_page.images if any(
                                    ext in img.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg'])]
                                if images:
                                    image_url = images[0]
                            
                            article = {
                                'article_id': str(specific_page.pageid),
                                'title': specific_page.title,
                                'summary': specific_page.summary[:500] + '...' if len(specific_page.summary) > 500 else specific_page.summary,
                                'url': specific_page.url,
                                'image_url': image_url,
                                'categories': ', '.join(specific_page.categories[:5]) if hasattr(specific_page, 'categories') and specific_page.categories else ''
                            }
                            articles.append(article)
                        except Exception as inner_e:
                            logger.warning(f"Failed to get first disambiguation option for {title}: {inner_e}")
                            continue
                except wikipedia.exceptions.PageError as e:
                    logger.warning(f"Wikipedia page error for {title}: {e}")
                    continue
                except Exception as e:
                    logger.exception(f"Error fetching article {title}: {e}")
                    continue
                    
            return articles
        except Exception as e:
            logger.exception(f"Error in Wikipedia search: {e}")
            # Try fallback method
            return WikipediaService._fallback_search(query, limit)
    
    @staticmethod
    def _fallback_search(query, limit=10):
        """Fallback method using Wikipedia's REST API directly"""
        try:
            articles = []
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srlimit={limit}&srsearch={query}"
            
            response = requests.get(url)
            data = response.json()
            
            search_results = data.get('query', {}).get('search', [])
            
            for result in search_results:
                pageid = result.get('pageid')
                title = result.get('title')
                snippet = result.get('snippet', '')
                
                # Strip HTML tags from snippet
                import re
                snippet = re.sub('<[^<]+?>', '', snippet)
                
                article = {
                    'article_id': str(pageid),
                    'title': title,
                    'summary': snippet,
                    'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                    'image_url': None,
                    'categories': ''
                }
                articles.append(article)
                
            return articles
        except Exception as e:
            logger.exception(f"Fallback Wikipedia search failed: {e}")
            return []

class EmbeddingService:
    _instance = None
    _model = None
    
    def __new__(cls):
        # Singleton pattern to avoid loading the model multiple times
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance
    
    @property
    def model(self):
        # Lazy loading of the model
        if self._model is None:
            try:
                self._model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"Error loading embedding model: {e}")
                return None
        return self._model
    
    def generate_embedding(self, text):
        """Generate an embedding for the given text"""
        if not text or not self.model:
            return None
            
        try:
            # Limit text size to avoid memory issues
            if len(text) > 10000:
                text = text[:10000]
                
            return self.model.encode(text).tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def find_similar_articles(self, embedding, limit=10):
        """Find similar articles based on embedding"""
        if not embedding:
            return []
            
        try:
            embedding_vector = np.array(embedding)
            
            # Get all articles with embeddings
            articles = WikipediaArticle.objects.filter(embedding__isnull=False)
            similarities = []
            
            for article in articles:
                article_embedding = article.get_embedding()
                if article_embedding:
                    try:
                        # Calculate cosine similarity
                        article_vector = np.array(article_embedding)
                        similarity = np.dot(embedding_vector, article_vector) / (
                            np.linalg.norm(embedding_vector) * np.linalg.norm(article_vector) or 1e-10  # Avoid division by zero
                        )
                        similarities.append((article, similarity))
                    except Exception as e:
                        print(f"Error calculating similarity for article {article.id}: {e}")
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top similar articles
            return [item[0] for item in similarities[:limit]]
        except Exception as e:
            print(f"Error finding similar articles: {e}")
            return []

def get_recommendations_for_user(user, limit=10):
    """Get article recommendations based on user's liked articles"""
    try:
        # Get user's liked articles
        liked_interactions = UserArticleInteraction.objects.filter(
            user=user,
            liked=True
        )
        
        if not liked_interactions.exists():
            # If user hasn't liked any articles, return trending/popular ones
            return WikipediaArticle.objects.all().order_by('-created_at')[:limit]
        
        # Combine content from all liked articles
        combined_text = ""
        for interaction in liked_interactions:
            article = interaction.article
            combined_text += f"{article.title} {article.summary} {article.categories} "
        
        # Generate embedding from combined text
        service = EmbeddingService()
        user_profile_embedding = service.generate_embedding(combined_text)
        
        if not user_profile_embedding:
            return WikipediaArticle.objects.all().order_by('-created_at')[:limit]
        
        # Find similar articles
        recommended_articles = service.find_similar_articles(user_profile_embedding, limit * 2)
        
        # Exclude already liked articles
        liked_article_ids = liked_interactions.values_list('article__id', flat=True)
        recommended_articles = [a for a in recommended_articles if a.id not in liked_article_ids]
        
        # Return the requested number of articles or fewer if not enough
        return recommended_articles[:limit]
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        # Return recent articles as fallback
        return WikipediaArticle.objects.all().order_by('-created_at')[:limit]
