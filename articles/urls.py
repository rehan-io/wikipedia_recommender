from django.urls import path
from .views import (
    RecommendedArticlesAPIView, 
    ArticleLikeAPIView,
    TrendingArticlesAPIView,
    fetch_articles,
    WikipediaService
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

# Define a direct search view function that calls WikipediaService.search_articles
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def direct_search(request):
    """Directly search Wikipedia articles using MediaWiki API"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=400)
    
    # Directly call WikipediaService.search_articles
    articles = WikipediaService.search_articles(query)
    return JsonResponse({"articles": articles})

urlpatterns = [
    # Use direct_search instead of ArticleSearchAPIView.as_view()
    path('search/', direct_search, name='article-search'),
    path('recommended/', RecommendedArticlesAPIView.as_view(), name='recommended-articles'),
    path('trending/', TrendingArticlesAPIView.as_view(), name='trending-articles'),
    path('<int:article_id>/like/', ArticleLikeAPIView.as_view(), name='article-like'),
    path('', fetch_articles, name='fetch-articles'),
]
