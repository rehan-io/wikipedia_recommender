from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import WikipediaArticle, UserArticleInteraction
from .serializers import WikipediaArticleSerializer, UserArticleInteractionSerializer
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests

# Create a new WikipediaService that uses MediaWiki API directly
class WikipediaService:
    @staticmethod
    def search_articles(query, limit=10):
        """Search for Wikipedia articles using MediaWiki API directly"""
        try:
            # Use MediaWiki API with generator=search for efficiency
            api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": limit,
                "prop": "extracts|pageimages|info",
                "exintro": 1,
                "explaintext": 1,
                "piprop": "thumbnail",
                "pithumbsize": 500,
                "pilimit": limit,
                "inprop": "url"
            }
            
            response = requests.get(api_url, params=params)
            data = response.json()
            
            articles = []
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                print(f"No results found for query: {query}")
                return []
            
            # Sort pages to ensure consistent ordering
            for page_id, page_info in sorted(pages.items(), key=lambda item: int(item[0])):
                title = page_info.get("title", "")
                summary = page_info.get("extract", "")
                url = page_info.get("fullurl", f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")
                
                # Get image if available
                image_url = None
                if "thumbnail" in page_info:
                    image_url = page_info["thumbnail"]["source"]
                
                article = {
                    "article_id": str(page_id),
                    "title": title,
                    "summary": summary[:500] + "..." if len(summary) > 500 else summary,
                    "url": url,
                    "image_url": image_url,
                    "categories": ""  # Simplified - no categories for better performance
                }
                
                articles.append(article)
            
            print(f"Found {len(articles)} articles for query: {query}")
            return articles
        except Exception as e:
            print(f"Error in MediaWiki search: {e}")
            return []

class ArticleSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        print(f"Searching for: {query}")
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Search for articles
            articles_data = WikipediaService.search_articles(query)
            
            if not articles_data:
                return Response([], status=status.HTTP_200_OK)
            
            # Save articles to database if they don't exist
            articles = []
            for article_data in articles_data:
                try:
                    article, created = WikipediaArticle.objects.update_or_create(
                        article_id=article_data['article_id'],
                        defaults={
                            'title': article_data.get('title', ''),
                            'summary': article_data.get('summary', ''),
                            'url': article_data.get('url', ''),
                            'image_url': article_data.get('image_url'),
                            'categories': article_data.get('categories', '')
                        }
                    )
                    articles.append(article)
                except Exception as e:
                    print(f"Error saving article to database: {e}")
                    continue
            
            # Serialize and return
            serializer = WikipediaArticleSerializer(
                articles, many=True, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            print(f"Search API error: {e}")
            return Response(
                {"error": f"An error occurred during search: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RecommendedArticlesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get recommendations for the user
        recommended_articles = get_recommendations_for_user(request.user)
        
        serializer = WikipediaArticleSerializer(
            recommended_articles, many=True, context={'request': request}
        )
        return Response(serializer.data)

class ArticleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, article_id):
        try:
            article = WikipediaArticle.objects.get(id=article_id)
        except WikipediaArticle.DoesNotExist:
            return Response(
                {"error": "Article not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Toggle the like status
        interaction, created = UserArticleInteraction.objects.get_or_create(
            user=request.user,
            article=article,
            defaults={'liked': True, 'viewed': True}
        )
        
        if not created:
            interaction.liked = not interaction.liked
            interaction.viewed = True
            interaction.save()
        
        return Response({
            "article_id": article.id,
            "liked": interaction.liked
        })

class TrendingArticlesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get trending articles (based on most interactions)
        trending_articles = WikipediaArticle.objects.filter(
            userarticleinteraction__isnull=False
        ).distinct().order_by('-created_at')[:10]
        
        serializer = WikipediaArticleSerializer(
            trending_articles, many=True, context={'request': request}
        )
        return Response(serializer.data)


@require_http_methods(["GET"])
def fetch_articles(request):
    """API endpoint to fetch more Wikipedia articles for infinite scrolling"""
    count = int(request.GET.get('count', 5))
    
    # Directly implement random article fetching here instead of using WikipediaService
    base_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    articles = []
    
    for _ in range(count):
        try:
            response = requests.get(base_url)
            data = response.json()
            
            article = {
                'title': data.get('title'),
                'extract': data.get('extract'),
                'thumbnail': data.get('thumbnail', {}).get('source') if data.get('thumbnail') else None,
                'url': data.get('content_urls', {}).get('desktop', {}).get('page') if data.get('content_urls') else None
            }
            articles.append(article)
        except Exception as e:
            print(f"Error fetching Wikipedia article: {e}")
    
    return JsonResponse({'articles': articles})