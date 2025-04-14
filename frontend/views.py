from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'  

class SignupView(TemplateView):
    template_name = 'signup.html'  

class LoginView(TemplateView):
    template_name = 'login.html'  

class LogoutView(TemplateView):
    template_name = 'logout.html'  

class ProfileView(TemplateView):
    template_name = 'profile.html'  
