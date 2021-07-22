import os

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods
from icecream import ic

from .models import UserProfile, Board, Category
from .forms import NewUserForm

# Puramente per debug, prima o poi lo si toglie
CHECK_BOARDS = False


@require_http_methods(["GET", "HEAD", "POST"])
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            propic: UploadedFile = request.FILES.get("propic", default=None)

            if propic is not None:
                tmp = f"{user.id}{propic.name}"
                ext = os.path.splitext(propic.name)[1]

                propic.name = f"{hash(tmp)}{ext}"

                UserProfile.objects.create(user=user, profile_pic=propic)
            else:
                UserProfile.objects.create(user=user)

            login(request, user)
            messages.success(request, "Registrazione avvenuta con successo")
            return redirect("profile")

        handle_form_errors(request, form, "Registrazione fallita:")

    return render(request, 'registration/register.html', context={"register_form": NewUserForm()})


@require_http_methods(["GET", "HEAD", "POST"])
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hai acceduto come {username}.")
                return redirect("profile")

        handle_form_errors(request, form, "Accesso fallito:")

    return render(request, 'registration/login.html', context={"login_form": AuthenticationForm()})


def handle_form_errors(request, form, header):
    key = list(form.errors.keys())[0]
    error = form.errors[key][0]

    messages.error(request, f"{header}{error}")


def get_authenticated_user(request):
    output = request.user
    return output.userprofile if output.is_authenticated else None


@require_http_methods(["GET", "HEAD"])
def profile(request):
    if user := get_authenticated_user(request):
        data = {'propic': user.profile_pic.name}

        try:
            boards = []
            for b in Board.objects.filter(user=ic(user)):
                boards.append(b.name)
            data.update({"boards": boards})
        except Model.DoesNotExist:
            pass

        return render(request, 'profile.html', status=200, context=data)

    messages.warning(request, "Devi effettuare il login")
    return redirect("homepage")


@require_http_methods(["GET", "HEAD"])
def logout_request(request):
    if get_authenticated_user(request):
        logout(request)
        messages.success(request, "Ti sei disconnesso correttamente")

    return redirect("homepage")


@require_http_methods(["GET", "HEAD"])
def homepage(request):
    return render(request, 'homepage.html', status=200)


@require_http_methods(["GET", "HEAD"])
def board_debug(request):
    return render(request, 'board.html', status=200)


@require_http_methods(["GET", "HEAD"])
def board(request, name):
    if user := get_authenticated_user(request):
        try:
            board_obj = Board.objects.get(user=user, name=name)

            # FIXME: questa lettura dei dati della board è un po' farlocca (board.name è uguale all'argomento name)
            # ma vabbè
            data: dict = {"board_name": board_obj.name}

            # Usa i dati ottenuti per generare l'html
            return render(request, 'board.html', status=200, context=data)
        except:
            # Se non esiste, segnala un errore
            messages.warning(request, f"La board {name} non esiste per questo utente")
            return redirect("profile")
    else:
        return HttpResponse("User cannot be anonymous", status=403)


@require_http_methods(["POST"])
def create_board(request, name, category, f):
    if user := get_authenticated_user(request):
        favorite = f == "true"

        try:
            # Cerca la board per l'utente
            Board.objects.get(user=user, name=name)
            # Se esiste, segnala un errore
            messages.warning(request, f"La board {name} esiste già per questo utente")
            return redirect('profile.html', status=406)
        except Model.DoesNotExist:
            # Se non riesce a trovare una board T per questo utente, vuol dire che può essere creata
            cat = None

            if c != "NaN":
                # Cerca la categoria C nel profilo dell'utente
                cat = Category.objects.get(user=user, name=category)

            Board.objects.create(user=user, name=name, category=cat, favorite=favorite)

            messages.success(request, f"Board {name} creata con successo!")
            return redirect('profile.html', status=200)

    else:
        return HttpResponse("User cannot be anonymous", status=403)
