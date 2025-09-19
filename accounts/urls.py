from django.urls import path
from . import views

urlpatterns = [
    # Page d'inscription comme page d'accueil
    path('', views.register_view, name='home'),
    path('register/', views.register_view, name='register'),
    
    # Autres pages
    path('accueil/', views.home_view, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Complétion des profils
    path('complete-etudiant-profile/', views.complete_etudiant_profile, name='complete_etudiant_profile'),
    path('complete-professeur-profile/', views.complete_professeur_profile, name='complete_professeur_profile'),
    
    # Dashboard et profil
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

]