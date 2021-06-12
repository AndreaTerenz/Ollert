from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

# Puramente per debug, prima o poi lo si toglie
CHECK_BOARDS = False


@require_http_methods(["GET", "HEAD"])
def landing(request):
    user = request.user

    if user.is_authenticated:
        return render(request, 'profile.html', status=200)
    else:
        return render(request, 'login.html', status=200)


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
