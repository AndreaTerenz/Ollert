from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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


@require_http_methods(["GET", "HEAD"])
def landing(request):
    user = request.user

    if user.is_authenticated:
        return render(request, 'registration/profile.html', status=200)
    else:
        return render(request, 'registration/login.html', status=200)


@require_http_methods(["GET", "HEAD"])
def registrationPage(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'registration/register.html', status=200, context=context)


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
