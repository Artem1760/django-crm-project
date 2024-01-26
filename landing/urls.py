
from django.urls import path
from django.contrib.auth.views import LoginView 
    
from .import views

app_name = 'landing'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing-page'), 
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'), 
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='landing/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout')   
]