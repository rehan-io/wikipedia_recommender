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
from .services.wikipedia_service import WikipediaService


# Create a new WikipediaService that uses MediaWiki API directly
class ArticleSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        articles = WikipediaService.search_articles(query)
        return Response({"articles": articles})

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