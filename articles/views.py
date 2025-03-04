from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import WikipediaArticle, UserArticleInteraction
from .serializers import WikipediaArticleSerializer, UserArticleInteractionSerializer

# Import the lite version of services
try:
    from .services_lite import WikipediaService, get_recommendations_for_user
except ImportError:
    # Fallback to full version if available
    try:
        from .services import WikipediaService, get_recommendations_for_user
    except ImportError:
        # Define minimal functionality if neither is available
        class WikipediaService:
            @staticmethod
            def search_articles(query, limit=10):
                return []
                
        def get_recommendations_for_user(user, limit=10):
            return WikipediaArticle.objects.all().order_by('-created_at')[:limit]

class ArticleSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Search for articles
        articles_data = WikipediaService.search_articles(query)
        
        # Save articles to database if they don't exist
        articles = []
        for article_data in articles_data:
            article, created = WikipediaArticle.objects.update_or_create(
                article_id=article_data['article_id'],
                defaults={
                    'title': article_data['title'],
                    'summary': article_data['summary'],
                    'url': article_data['url'],
                    'image_url': article_data['image_url'],
                    'categories': article_data['categories']
                }
            )
            articles.append(article)
        
        # Serialize and return
        serializer = WikipediaArticleSerializer(
            articles, many=True, context={'request': request}
        )
        return Response(serializer.data)

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
