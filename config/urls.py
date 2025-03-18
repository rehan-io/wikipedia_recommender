from django.contrib import admin
from django.urls import path, include
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/articles', views.fetch_articles, name='fetch_articles'),
    path('', include('frontend.urls')),  # Add this line for frontend URLs
]
