from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'  # Updated path

class SignupView(TemplateView):
    template_name = 'signup.html'  # Updated path

class LoginView(TemplateView):
    template_name = 'login.html'  # Updated path

class LogoutView(TemplateView):
    template_name = 'logout.html'  # Updated path

class ProfileView(TemplateView):
    template_name = 'profile.html'  # Updated path
