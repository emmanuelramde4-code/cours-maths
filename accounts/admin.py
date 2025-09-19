from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EtudiantProfile, ProfesseurProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée pour le modèle User"""
    
    # Champs affichés dans la liste
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'phone', 'birth_date')
        }),
    )
    
    # Champs pour l'ajout d'un nouvel utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'phone', 'birth_date')
        }),
    )

class EtudiantProfileInline(admin.StackedInline):
    """Inline pour afficher le profil étudiant dans l'admin User"""
    model = EtudiantProfile
    can_delete = False
    verbose_name_plural = "Profil Étudiant"
    extra = 0

class ProfesseurProfileInline(admin.StackedInline):
    """Inline pour afficher le profil professeur dans l'admin User"""
    model = ProfesseurProfile
    can_delete = False
    verbose_name_plural = "Profil Professeur"
    extra = 0

@admin.register(EtudiantProfile)
class EtudiantProfileAdmin(admin.ModelAdmin):
    """Administration pour les profils étudiants"""
    list_display = ('user', 'niveau', 'etablissement', 'date_inscription')
    list_filter = ('niveau', 'etablissement', 'date_inscription')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'etablissement')
    readonly_fields = ('date_inscription',)
    
    # Organiser les champs
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations académiques', {
            'fields': ('niveau', 'etablissement')
        }),
        ('Dates', {
            'fields': ('date_inscription',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProfesseurProfile)
class ProfesseurProfileAdmin(admin.ModelAdmin):
    """Administration pour les profils professeurs"""
    list_display = ('user', 'specialite', 'etablissement', 'experience', 'date_creation')
    list_filter = ('specialite', 'etablissement', 'experience', 'date_creation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialite', 'etablissement')
    readonly_fields = ('date_creation',)
    
    # Organiser les champs
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations professionnelles', {
            'fields': ('specialite', 'etablissement', 'experience')
        }),
        ('À propos', {
            'fields': ('bio',)
        }),
        ('Dates', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )

# Personnalisation de l'interface d'administration
admin.site.site_header = "Administration - Cours de Maths"
admin.site.site_title = "Admin Cours Maths"
admin.site.index_title = "Gestion de l'application"