from rest_framework import serializers
from .models import WikipediaArticle, UserArticleInteraction

class WikipediaArticleSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = WikipediaArticle
        fields = ['id', 'article_id', 'title', 'summary', 'url', 'image_url', 
                  'categories', 'created_at', 'is_liked']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                interaction = UserArticleInteraction.objects.get(
                    user=request.user,
                    article=obj
                )
                return interaction.liked
            except UserArticleInteraction.DoesNotExist:
                return False
        return False

class UserArticleInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArticleInteraction
        fields = ['id', 'article', 'liked', 'viewed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
