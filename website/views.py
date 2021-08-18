import json
import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views.decorators.http import require_http_methods
from icecream import ic

from .models import UserProfile, Board, Category
from .forms import NewUserForm

ic.disable()


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

    return render(request, 'access/register.html', context={"register_form": NewUserForm()})


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

    return render(request, 'access/login.html', context={"login_form": AuthenticationForm()})


@login_required
@require_http_methods(["GET", "HEAD"])
def profile(request):
    user = get_authenticated_user(request)
    data = {
        'propic': user.profile_pic.name,
        "boards": get_user_boards(user)
    }

    return render(request, 'profile/profile.html', status=200, context=data)


@login_required
@require_http_methods(["GET", "HEAD", "POST"])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'La tua password è stata correttamente aggiornata!')
            return redirect('profile')

        handle_form_errors(request, form, "Modifica fallita:")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'access/change_password.html', {
        'form': form
    })


@login_required
@require_http_methods(["GET", "HEAD"])
def logout_request(request):
    logout(request)
    messages.success(request, "Ti sei disconnesso correttamente")

    return redirect("homepage")


@require_http_methods(["GET", "HEAD"])
def homepage(request):
    if get_authenticated_user(request):
        return redirect('profile')
    return render(request, 'homepage.html', status=200)


@login_required
@require_http_methods(["GET", "HEAD"])
def board(request, name):
    user = get_authenticated_user(request)

    if board_obj := get_user_board(user, name):
        data: dict = {"board_name": board_obj.name, "board_background": board_obj.background}

        # Usa i dati ottenuti per generare l'html
        return render(request, 'board.html', status=200, context=data)

    # Se non esiste, segnala un errore
    messages.warning(request, f"La board {name} non esiste per questo utente")
    return redirect("profile")


@login_required
@require_http_methods(["POST"])
def create_board(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    ic(data)

    if not (get_user_board(user, data["name"])):
        # Se non riesce a trovare una board T per questo utente, vuol dire che può essere creata
        category = None

        if data["category"] != "NaN":
            # Cerca la categoria C nel profilo dell'utente
            ic(data["category"], category)
            category = Category.objects.get(user=user, name=data["category"])

        Board.objects.create(user=user, name=data["name"], category=category, favorite=data["favorite"])

        messages.success(request, f"Board {data['name']} creata con successo!")
        return render(request, "profile/profile-boards-list.html", context={"boards": get_user_boards(user)})

    # Se esiste, segnala un errore
    messages.warning(request, f"La board {data['name']} esiste già per questo utente")
    return redirect("profile")


@login_required
@require_http_methods(["POST"])
def delete_board(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    ic(data)

    # Cerca la board per l'utente
    if board_obj := get_user_board(user, data["name"]):
        ic(board_obj)
        # Se esiste, la si cancella
        board_obj.delete()
        return render(request, "profile/profile-boards-list.html", context={"boards": get_user_boards(user)})

    # Se non riesce a trovare la board, si segnala un errore
    messages.error(request, f"La board {data['name']} non esiste")
    return redirect("profile")


@login_required
@require_http_methods(["POST"])
def edit_board(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    """
    Formato JSON:
    {
        target_field: <name|category|favorite|background>
        board: <nome board da modificare>
        new_value: <nuovo valore>
    }
    """

    field = data["target_field"]
    board_name = data["board_name"]
    new_value = data["new_value"]

    # FIXME: bisognerebbe capire bene cosa ritornare invece di mere HttpResponse
    if board_obj := get_user_board(user, board_name):
        # DIO COME VOGLIO UNO SWITCH IN PYTHON
        if field == "name":
            if not (get_user_board(user, new_value)):
                board_obj.name = new_value
            else:
                return HttpResponse(f"Board {new_value} already exists for this user", status=406)
        if field == "category":
            board_obj.category = new_value
        elif field == "favorite":
            board_obj.favorite = new_value
        elif field == "background":
            board_obj.background = new_value
        board_obj.save()
        return HttpResponse(f"Board field '{field}' changed", status=200)
    else:
        return HttpResponse(f"Board {board_name} not found", status=406)


@login_required
@require_http_methods(["POST"])
def create_card(request, board):
    body = json.loads(request.body())
    user = get_authenticated_user(request)


def handle_form_errors(request, form, header):
    key = list(form.errors.keys())[0]
    error = form.errors[key][0]

    messages.error(request, f"{header}{error}")


def get_authenticated_user(request):
    output = request.user
    return output.userprofile if output.is_authenticated else None


def get_user_board(user, name):
    try:
        return Board.objects.get(user=user, name=name)
    except ObjectDoesNotExist:
        return None


def get_user_boards(user):
    try:
        boards = []
        for b in Board.objects.filter(user=user):
            boards.append(b.name)
        return boards
    except ObjectDoesNotExist:
        return []
