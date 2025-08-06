from django.db import models

# Create your models here.
from django.db import models

class Classe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Chapitre(models.Model):
    titre = models.CharField(max_length=200)
    numero = models.IntegerField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="chapitres")

    def __str__(self):
        return f"{self.numero} - {self.titre}"

class Lecon(models.Model):
    nom = models.CharField(max_length=200)
    contenu = models.TextField()
    fichier = models.FileField(upload_to='lecons_pdfs/', null=True, blank=True)  # ✅
    chapitre = models.ForeignKey('Chapitre', on_delete=models.CASCADE, related_name='lecons')

    def __str__(self):
        return self.nom


class Video(models.Model):
    titre = models.CharField(max_length=200)
    url = models.URLField()
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE, related_name="videos")

    def __str__(self):
        return self.titre




class Exercice(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    fichier = models.FileField(upload_to='exercices_pdfs/', null=True, blank=True)  # ✅
    chapitre = models.ForeignKey('Chapitre', on_delete=models.CASCADE, related_name='exercices')

    def __str__(self):
        return self.titre


class Correction(models.Model):
    contenu = models.TextField()
    fichier = models.FileField(upload_to='corrections_pdfs/', null=True, blank=True)  # ✅
    exercice = models.OneToOneField(Exercice, on_delete=models.CASCADE, related_name='correction')

    def __str__(self):
        return f"Correction de : {self.exercice.titre}"



class Quiz(models.Model):
    titre = models.CharField(max_length=200)
    duree = models.IntegerField(help_text="Durée en minutes")
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, related_name="quiz")

    def __str__(self):
        return self.titre


class Question(models.Model):
    texte = models.TextField()
    image = models.ImageField(upload_to='questions_images/', null=True, blank=True)  # ✅ Ajout du champ image
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.texte[:50] + "..."

    
class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=255)
    est_correcte = models.BooleanField(default=False)

    def __str__(self):
        return self.texte

class Explication(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='explication')
    texte = models.TextField(blank=True)
    image = models.ImageField(upload_to='explications_images/', null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Explication de : {self.question.texte[:50]}..."




        