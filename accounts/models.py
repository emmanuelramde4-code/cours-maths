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
     

### aujourd'hui
# accounts/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Premium' if self.is_premium else 'Free'}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # ex: en XOF
    currency = models.CharField(max_length=10, default='XOF')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    external_id = models.CharField(max_length=128, blank=True, null=True)  # id renvoyé par Orange
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user} - {self.status}"
