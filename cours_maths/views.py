# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Classe

from django.shortcuts import render, get_object_or_404
from .models import (Classe, Chapitre, Lecon, Video, Exercice, Quiz,Correction)

def accueil(request):
    return render(request, 'cours_maths/home.html')

def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'cours_maths/classe.html', {'classes': classes})

def liste_chapitres(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    chapitres = classe.chapitres.all()
    return render(request, 'cours_maths/chapitre.html', {'classe': classe, 'chapitres': chapitres})


def classe_detail(request, classe_id):
    classe = Classe.objects.get(id=classe_id)
    chapitres = classe.chapitres.all()
    return render(request, 'cours_maths/classe_detail.html', {
        'classe': classe,
        'chapitres': chapitres
    })

def chapitre_detail(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    lecons = chapitre.lecons.all()
    exercices = chapitre.exercices.all()
    quiz = chapitre.quiz.all()
    videos = Video.objects.filter(lecon__in=lecons)
    corrections = Correction.objects.filter(exercice__in=exercices)
    return render(request, 'cours_maths/chaptitre_detail.html', {
        'chapitre': chapitre,
        'lecons': lecons,
        'exercices': exercices,
        'corrections':corrections, 
        'quiz': quiz,
        'videos': videos,
    })

def accueil_eleves(request):
    classes = Classe.objects.all()
    return render(request, 'cours_maths/acceuil.html', {'classes': classes})


from django.shortcuts import render, get_object_or_404
from .models import( Quiz, Question, Reponse)

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'cours_maths/quiz_detail.html', {'quiz': quiz, 'questions': questions})

from django.shortcuts import redirect

def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    bonnes_reponses = 0
    total_questions = questions.count()

    if request.method == 'POST':
        for question in questions:
            reponse_id = request.POST.get(str(question.id))
            if reponse_id:
                reponse = Reponse.objects.get(id=reponse_id)
                if reponse.est_correcte:
                    bonnes_reponses += 1

        score = int((bonnes_reponses / total_questions) * 100)

        # Stocker le score dans la session
        request.session['score'] = score

        # Rediriger vers la page de score
        return redirect('quiz_resultat', quiz_id=quiz.id)




from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Reponse, Explication

def quiz_resultat(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = request.session.get('score')
    total_questions = request.session.get('total_questions')
    return render(request, 'cours_maths/quiz_resultat.html', {
        'quiz': quiz,
        'score': score
    })


def correction_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('reponses')
    return render(request, 'cours_maths/quiz_correction.html', {
        'quiz': quiz,
        'questions': questions
    })


def explication_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('reponses')

    return render(request, 'cours_maths/quiz_explication.html', {
        'quiz': quiz,
        'questions': questions
    })

from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Reponse

def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('reponses')

    bonnes_reponses = 0
    total_questions = questions.count()
    reponses_utilisateur = {}

    if request.method == 'POST':
        for question in questions:
            selected_id = request.POST.get(str(question.id))
            if selected_id:
                reponses_utilisateur[question.id] = int(selected_id)
                bonne_reponse = question.reponses.filter(est_correcte=True).first()
                if bonne_reponse and bonne_reponse.id == int(selected_id):
                    bonnes_reponses += 1

    # On peut passer les réponses utilisateur pour la correction/explication
    request.session['reponses_utilisateur'] = reponses_utilisateur

    return render(request, 'cours_maths/quiz_resultat.html', {
        'quiz': quiz,
        'score': bonnes_reponses,
        'total_questions': total_questions
    })


#aujourd'hui
