from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, EtudiantProfile, ProfesseurProfile

class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription personnalisé"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    phone = forms.CharField(max_length=15, required=False, label="Téléphone")
    birth_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de naissance"
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Type de compte"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'phone', 'birth_date', 'user_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.birth_date = self.cleaned_data['birth_date']
        user.user_type = self.cleaned_data['user_type']
        
        if commit:
            user.save()
            # Créer le profil correspondant
            if user.user_type == 'etudiant':
                EtudiantProfile.objects.create(user=user)
            else:
                ProfesseurProfile.objects.create(user=user)
        
        return user

class EtudiantProfileForm(forms.ModelForm):
    """Formulaire pour compléter le profil étudiant"""
    class Meta:
        model = EtudiantProfile
        fields = ['niveau', 'etablissement']
        widgets = {
            'niveau': forms.TextInput(attrs={'placeholder': 'ex: Terminale S, Licence 1...'}),
            'etablissement': forms.TextInput(attrs={'placeholder': 'Nom de votre établissement'})
        }

class ProfesseurProfileForm(forms.ModelForm):
    """Formulaire pour compléter le profil professeur"""
    class Meta:
        model = ProfesseurProfile
        fields = ['specialite', 'etablissement', 'experience', 'bio']
        widgets = {
            'specialite': forms.TextInput(attrs={'placeholder': 'ex: Mathématiques, Physique...'}),
            'etablissement': forms.TextInput(attrs={'placeholder': 'Nom de votre établissement'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez-nous de vous...'}),
        }

class CustomLoginForm(forms.Form):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom d\'utilisateur',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe',
            'class': 'form-control'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
            if not self.user.is_active:
                raise forms.ValidationError("Ce compte est désactivé.")
        
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)