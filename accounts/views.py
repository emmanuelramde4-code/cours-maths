from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, EtudiantProfileForm, ProfesseurProfileForm, CustomLoginForm
from .models import User

def register_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Compte créé avec succès ! Bienvenue {user.first_name}.')
            login(request, user)
            
            # Rediriger selon le type d'utilisateur
            if user.user_type == 'etudiant':
                return redirect('complete_etudiant_profile')
            else:
                return redirect('complete_professeur_profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        # Rediriger selon le type d'utilisateur
        if request.user.is_etudiant():
            return redirect('accueil_eleves')  # App cours_maths
        else:
            return redirect('dashboard')  # Dashboard professeur
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name} !')
            
            # Rediriger selon le type d'utilisateur
            if user.is_etudiant():
                next_url = request.GET.get('next', 'accueil_eleves')
            else:
                next_url = request.GET.get('next', 'dashboard')
            
            return redirect(next_url)
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('home')

@login_required
def complete_etudiant_profile(request):
    """Vue pour compléter le profil étudiant"""
    if not request.user.is_etudiant():
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    profile = request.user.etudiant_profile
    
    if request.method == 'POST':
        form = EtudiantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil complété avec succès !')
            return redirect('dashboard')
    else:
        form = EtudiantProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_etudiant_profile.html', {'form': form})

@login_required
def complete_professeur_profile(request):
    """Vue pour compléter le profil professeur"""
    if not request.user.is_professeur():
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    profile = request.user.professeur_profile
    
    if request.method == 'POST':
        form = ProfesseurProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil complété avec succès !')
            return redirect('dashboard')
    else:
        form = ProfesseurProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_professeur_profile.html', {'form': form})

@login_required
@login_required
def dashboard(request):
    """Dashboard principal selon le type d'utilisateur"""
    if request.user.is_etudiant():
        return redirect('accueil_eleves')  # Rediriger vers l'app cours_maths
    elif request.user.is_professeur():
        return render(request, 'accounts/dashboard_professeur.html')
    else:
        messages.error(request, "Type d'utilisateur non reconnu.")
        return redirect('home')
@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    context = {'user': request.user}
    
    if request.user.is_etudiant():
        context['profile'] = request.user.etudiant_profile
        template = 'accounts/profile_etudiant.html'
    else:
        context['profile'] = request.user.professeur_profile
        template = 'accounts/profile_professeur.html'
    
    return render(request, template, context)

def home_view(request):
    """Page d'accueil"""
    return render(request, 'accounts/home.html')

