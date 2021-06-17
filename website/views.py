from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib import messages  # import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
from django.views.decorators.http import require_http_methods

# Puramente per debug, prima o poi lo si toglie
CHECK_BOARDS = False


# def registerPage(request):
#     context = {}
#     return render(request, 'registration/register.html', context)
#
#
# def loginPage(request):
#     context = {}
#     return render(request, 'registration/login.html', context)


@require_http_methods(["GET", "HEAD", "POST"])
def landing(request):
    user = request.user

    if user.is_authenticated:
        return render(request, 'registration/profile.html', status=200)
    else:
        return redirect('register/')
        # return registrationPage(request)
        # return render(request, 'registration/login.html', status=200)


@require_http_methods(["GET", "HEAD", "POST"])
def registrationPage(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print("AAAAA")
        print("QUI")
        user = form.save()
        login(request, user)
        print("QUI2")
        messages.success(request, "Registrazione avvenuta con successo")
        print("QUI3")
        return redirect("profile")
        messages.error(request, "Registrazione fallita. Informazioni invalide")
    form = NewUserForm
    return render(request, 'registration/register.html', context={"register_form": form})


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
                messages.info(request, f"Ora sei loggato come {username}.")
                return redirect("profile")
            else:
                messages.error(request, "Username o password non validi")
        else:
            messages.error(request, "Username o password non validi")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', context={"login_form": form})

def profile(request):
    return render(request, 'profile.html', status=200)

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
