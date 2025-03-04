import wikipedia
import json
import random

class WikipediaService:
    @staticmethod
    def search_articles(query, limit=10):
        """Search for Wikipedia articles based on query"""
        try:
            search_results = wikipedia.search(query, results=limit)
            articles = []
            
            for title in search_results:
                try:
                    # Use auto_suggest=False to avoid redirects and disambiguation issues
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
                except Exception as e:
                    print(f"Error fetching article {title}: {e}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error in Wikipedia search: {e}")
            return []

# Simplified version without ML embeddings
def get_recommendations_for_user(user, limit=10):
    """Get article recommendations based on user's liked articles (simplified version)"""
    from .models import WikipediaArticle, UserArticleInteraction
    
    # Get user's liked articles
    liked_interactions = UserArticleInteraction.objects.filter(
        user=user,
        liked=True
    )
    
    if not liked_interactions.exists():
        # If user hasn't liked any articles, return recent articles
        return WikipediaArticle.objects.all().order_by('-created_at')[:limit]
    
    # Get categories from liked articles
    categories = set()
    for interaction in liked_interactions:
        article = interaction.article
        if article.categories:
            for category in article.categories.split(', '):
                if category.strip():
                    categories.add(category.strip())
    
    # Find articles with similar categories
    if categories:
        similar_articles = []
        for category in categories:
            matches = WikipediaArticle.objects.filter(categories__icontains=category)
            similar_articles.extend(list(matches))
        
        # Remove duplicates and liked articles
        liked_ids = liked_interactions.values_list('article__id', flat=True)
        similar_articles = list({article.id: article for article in similar_articles 
                                if article.id not in liked_ids}.values())
        
        # Return a subset or all of them if fewer than limit
        if similar_articles:
            random.shuffle(similar_articles)
            return similar_articles[:limit]
    
    # Fallback to recent articles
    return WikipediaArticle.objects.all().order_by('-created_at')[:limit]
