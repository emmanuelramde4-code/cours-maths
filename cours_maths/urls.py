from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
 path('',views.accueil_eleves, name='accueil_eleves'),
 path('list_classe',views.liste_classes),
 path('eleves/', views.liste_classes, name='liste_classes'),
 path('eleves/classe/<int:classe_id>/', views.liste_chapitres, name='liste_chapitres'),
 path('eleves/chapitre/<int:chapitre_id>/', views.chapitre_detail, name='chapitre_detail'),
 path('eleves/classe/<int:classe_id>/', views.classe_detail, name='classe_detail'),

 

 path('quiz/<int:quiz_id>/resultat/', views.quiz_resultat, name='quiz_resultat'),
 path('quiz/<int:quiz_id>/correction/', views.correction_quiz, name='quiz_correction'),
 path('quiz/<int:quiz_id>/explication/', views.explication_quiz, name='quiz_explication'),
 path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
 
 path('quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
  ]