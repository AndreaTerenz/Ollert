import os

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods

from .models import UserProfile
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


def is_user_authenticated(request):
    return request.user.is_authenticated


@require_http_methods(["GET", "HEAD"])
def profile(request):
    if not is_user_authenticated(request):
        messages.warning(request, "Devi effettuare il login")
        return redirect("homepage")

    user = request.user.userprofile

    return render(request, 'profile.html', status=200, context={'propic': user.profile_pic.name})


@require_http_methods(["GET", "HEAD"])
def logout_request(request):
    if is_user_authenticated(request):
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
def board(request, title):
    if (user := request.user).is_authenticated:
        # TODO: controllare se la board "title" esiste per l'utente "user"
        if CHECK_BOARDS:
            pass

        return render(request, 'board.html', status=200)
    else:
        return HttpResponse("User cannot be anonymous", status=403)


@require_http_methods(["POST"])
def create_board(request):
    print("UE COJONE CIAO")
    return HttpResponse("Ye", status=200)
