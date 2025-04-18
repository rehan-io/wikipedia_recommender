from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.conf import settings
from django.conf.urls.static import static

@ensure_csrf_cookie
def csrf_token_view(request):
    """
    Explicit view to set the CSRF cookie
    """
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', csrf_token_view),
    path('api/', include('users.urls')),
    path('api/', include('articles.urls')),
    path('', include('frontend.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
