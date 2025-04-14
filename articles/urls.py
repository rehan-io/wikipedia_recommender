from django.urls import path
from .views import (
    ArticleLikeAPIView,
    TrendingArticlesAPIView,
    WikipediaService,
    ArticleSearchAPIView,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse


urlpatterns = [
    # Use direct_search instead of ArticleSearchAPIView.as_view()
    path('search/', ArticleSearchAPIView.as_view(), name='article-search'),
    # path('recommended/', RecommendedArticlesAPIView.as_view(), name='recommended-articles'),
    # path('trending/', TrendingArticlesAPIView.as_view(), name='trending-articles'),
    path('<int:article_id>/like/', ArticleLikeAPIView.as_view(), name='article-like'),
    # path('', fetch_articles, name='fetch-articles'),
]
