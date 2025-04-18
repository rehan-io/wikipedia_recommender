from django.urls import path, re_path
from .views import ReactAppView

app_name = 'frontend'

urlpatterns = [
    # Specific routes
    path('', ReactAppView.as_view(), name='home'),
    path('login/', ReactAppView.as_view(), name='login'),
    path('signup/', ReactAppView.as_view(), name='signup'),
    path('logout/', ReactAppView.as_view(), name='logout'),
    path('profile/', ReactAppView.as_view(), name='profile'),
    
    # Catch-all pattern for all other frontend routes
    re_path(r'^(?:.*)/?$', ReactAppView.as_view(), name='catch_all'),
]
