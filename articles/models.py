from django.db import models
from django.conf import settings
import json

class WikipediaArticle(models.Model):
    """Model to store minimal information about Wikipedia articles"""
    
    article_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    url = models.URLField()
    image_url = models.URLField(null=True, blank=True)
    categories = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Vector embedding stored as JSON
    embedding = models.TextField(blank=True, null=True)
    
    def set_embedding(self, embedding_array):
        self.embedding = json.dumps(embedding_array)
    
    def get_embedding(self):
        if self.embedding:
            return json.loads(self.embedding)
        return None
    
    def __str__(self):
        return self.title

class UserArticleInteraction(models.Model):
    """Model to track user interactions with articles"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(WikipediaArticle, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'article')
    
    def __str__(self):
        action = "liked" if self.liked else "viewed"
        return f"{self.user.username} {action} {self.article.title}"