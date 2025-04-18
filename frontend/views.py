from django.shortcuts import redirect
from django.views.generic import View
from django.http import JsonResponse
import os
import logging

logger = logging.getLogger(__name__)

class ReactAppView(View):
    """
    During development, this redirects to the React dev server.
    In production, it would serve the built React app.
    """
    def get(self, request, *args, **kwargs):
        # In development, redirect to the React dev server
        return redirect('http://localhost:3000')

# Use ReactAppView for all frontend routes
HomeView = ReactAppView
SignupView = ReactAppView
LoginView = ReactAppView
LogoutView = ReactAppView
ProfileView = ReactAppView
