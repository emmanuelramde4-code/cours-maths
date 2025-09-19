from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Modèle utilisateur personnalisé"""
    USER_TYPE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
    )
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default='etudiant'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def is_etudiant(self):
        return self.user_type == 'etudiant'
    
    def is_professeur(self):
        return self.user_type == 'professeur'

class EtudiantProfile(models.Model):
    """Profil spécifique aux étudiants"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant_profile')
    niveau = models.CharField(max_length=50, blank=True)  # ex: "Terminale S", "1ère année université"
    etablissement = models.CharField(max_length=100, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Étudiant: {self.user.username}"

class ProfesseurProfile(models.Model):
    """Profil spécifique aux professeurs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professeur_profile')
    specialite = models.CharField(max_length=100, blank=True)  # ex: "Mathématiques", "Physique"
    etablissement = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(default=0, help_text="Années d'expérience")
    bio = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Professeur: {self.user.username}"
     

