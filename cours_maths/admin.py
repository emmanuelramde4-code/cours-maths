from django.contrib import admin

# Register your models here.
from .models import (
    Classe, Chapitre, Lecon, Video,
    Exercice, Correction, Quiz, Question, Reponse,Explication,
)
@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)


@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'numero', 'classe')
    list_filter = ('classe',)
    search_fields = ('titre',)


@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'chapitre')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'lecon')
    search_fields = ('titre',)

@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'chapitre')


@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exercice')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'chapitre', 'duree')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz')
    search_fields = ('texte',)

admin.site.register(Reponse)

@admin.register(Explication)
class ExplicationAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question__texte',)




