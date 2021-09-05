import datetime
import json
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views.decorators.http import require_http_methods
from icecream import ic

from .models import UserProfile, Category, Card
from .forms import NewUserForm
from .utils import *


#ic.disable()


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
        "boards": get_user_boards(user),
        "categories": get_user_categories(user)
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
        lists = []

        for l_obj in get_lists_in_board(board_obj):
            l = {
                "list_title": l_obj.title,
                "list_id": f"list_{len(lists) + 1}",
                "list_cards": []
            }
            for idx, c_obj in enumerate(get_cards_in_list(l_obj)):
                c = {
                    "card_title": c_obj.title,
                    "card_descr": c_obj.description,
                    "card_unique_id": f"{l_obj.title}_{idx}"
                }
                # FIXME: Temporaneo
                l["list_cards"].append(c)

            lists.append(l)

        data: dict = {
            "board_name": board_obj.name,
            "board_background": board_obj.background,
            "board_description": board_obj.description,
            "board_lists": lists
        }

        # Usa i dati ottenuti per generare l'html
        return render(request, 'board/board.html', status=200, context=data)

    # Se non esiste, segnala un errore
    messages.warning(request, f"La board {name} non esiste per questo utente")
    return redirect("profile")


@login_required
@require_http_methods(["POST"])
def create_board(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    if not (get_user_board(user, data["name"])):
        # Se non riesce a trovare una board T per questo utente, vuol dire che può essere creata
        category = None

        if data["category"] != "NaN":
            # Cerca la categoria C nel profilo dell'utente
            category = Category.objects.get(user=user, name=data["category"])

        Board.objects.create(user=user, name=data["name"], category=category, description=data["description"],
                             favorite=data["favorite"])

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

    # Cerca la board per l'utente
    if board_obj := get_user_board(user, data["name"]):
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
        board: <nome board da modificare>
        edits: <lista delle modifiche da fare alla board in formato:>
            target_field: <name|category|favorite|background|description>
            new_value: <nuovo valore per il target_field>
    }
    """

    board_name = data["board_name"]

    # FIXME: bisognerebbe capire bene cosa ritornare invece di mere HttpResponse
    if board_obj := get_user_board(user, board_name):
        for edit in ic(data["edits"]):
            field = edit["target_field"]
            new_value = edit["new_value"]

            # DIO COME VOGLIO UNO SWITCH IN PYTHON
            if field == "name":
                if not (get_user_board(user, new_value)):
                    board_obj.name = new_value
                else:
                    return HttpResponse(f"Board {new_value} already exists for this user", status=406)
            elif field == "category":
                board_obj.category = get_user_category(user, new_value)
            elif field == "description":
                board_obj.description = new_value
            elif field == "favorite":
                board_obj.favorite = new_value
            elif field == "background":
                board_obj.background = new_value

        board_obj.save()
        return render(request, "profile/profile-boards-list.html", context={"boards": get_user_boards(user)})
    else:
        return HttpResponse(f"Board {board_name} not found", status=406)


@login_required
@require_http_methods(["POST"])
def create_board_content(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    """
    Formato JSON:
    
    {
        target_type: <list|card>
        target_id: {
            target_id_board: <nome della board>
            [target_id_list: <id della lista>]       se bisogna creare una card
        }
        new_data: { 
                list_name: <nome lista>                 se bisogna creare una lista

                card_name: <nome card>                  se bisogna creare una card
                [card_descr: <descrizione card>]
                [card_date: <data card>]
                [card_img: <immagine card (non so ancora come)>]
                [card_checks: <checklist card (non so ancora come)>]
                [card_members: <elenco utenti assegnati alla card (non so ancora come)>]
                [card_tags: <elenco tag assegnati alla card>]
        }
    }
    """

    trgt_type = data["target_type"]
    if trgt_board := get_user_board(user, data["target_id"]["target_id_board"]):
        trgt_content: dict = data["new_data"]

        if trgt_type == "list":
            pos = trgt_board.lists_count + 1
            title = trgt_content["list_name"]

            List.objects.create(
                user=user,
                board=trgt_board,
                position=ic(pos),
                title=title
            )

            trgt_board.lists_count += 1
            trgt_board.save()

            return render(request, 'board/list.html', context={
                "title": title,
                "cards": [],
                "id": f"list_{pos}"
            })
        elif trgt_type == "card":
            ic(data["target_id"]["target_id_list"])
            trgt_list = List.objects.get(board=ic(trgt_board), position=int(data["target_id"]["target_id_list"]))
            pos = trgt_list.cards_count + 1

            Card.objects.create(
                user=user,
                board=trgt_board,
                list=trgt_list,
                position=pos,
                title=trgt_content["card_name"],
                description=trgt_content.get("card_descr", None),
                date=trgt_content.get("card_date", None),
                # TODO: mancano immagine, checklist e membri
                # image
                # checklist
                # members
                tags=trgt_content.get("card_tags", {})
            )

            trgt_list.cards_count += 1
            trgt_list.save()

            data = ic({"card_title": trgt_content["card_name"], "card_descr": trgt_content.get("card_descr", None)})

            return render(request, "board/card.html", context={"data": data})
    else:
        return HttpResponse(f"Board {data['target_id']['target_id_board']} not found", status=406)


@login_required
@require_http_methods(["POST"])
def delete_board_content(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    """
    Formato JSON:
    
    {
        target_type: <list|card>
        target_id: {
            target_id_board: <nome della board>
            target_id_list: <id della lista>
            [target_id_card: <id della card>]       se bisogna eliminare una card
        }
    }
    """

    trgt_type = data["target_type"]

    if trgt_board := get_user_board(user, data["target_id"]["target_id_board"]):
        trgt_list = List.objects.get(board=trgt_board, position=data["target_id"]["target_id_list"])

        if trgt_type == "list":
            trgt_list.delete()
        elif trgt_type == "card":
            trgt_card = Card.objects.get(list=trgt_list, position=data["target_id"]["target_id_card"])
            trgt_card.delete()

        return HttpResponse("Content deleted", status=200)
    else:
        return HttpResponse(f"Board {data['target_id']['target_id_board']} not found", status=406)


@login_required
@require_http_methods(["POST"])
def edit_board_content(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    """
    Formato JSON:
    
    {
        target_type: <list|card>
        target_id: {
            target_id_board: <nome della board>
            target_id_list: <id della lista>
            [target_id_card: <id della card>]       se bisogna modificare una card
        }
        target_field:
            <title|position>      se bisogna modificare una lista
            
            <name|position|description|date|img|checks|members|tags> se bisogna modificare una card
        new_value: <nuovo valore del target field>
    }
    """

    trgt_type = data["target_type"]

    if trgt_board := get_user_board(user, data["target_id"]["target_id_board"]):
        trgt_list = List.objects.get(board=trgt_board, position=data["target_id"]["target_id_list"])
        trgt_field = data["target_field"]
        new_value = data["new_value"]

        if trgt_type == "list":
            if trgt_field == "title":
                trgt_list.title = new_value
            elif trgt_field == "position":
                # initial_pos = trgt_list.position
                # dest_pos = new_value
                #
                # if initial_pos != dest_pos:
                #     if initial_pos < dest_pos:
                #         for l in List.objects.filter(board=trgt_board,
                #                                      position__range=range(initial_pos + 1, dest_pos)):
                #             l.position -= 1
                #             l.save()
                #     else:
                #         for l in List.objects.filter(board=trgt_board,
                #                                      position__range=range(dest_pos, initial_pos - 1)):
                #             l.position += 1
                #             l.save()
                #
                #

                move_object(trgt_list.position, new_value, trgt_board, List)
                trgt_list.position = new_value

            trgt_list.save()
        elif trgt_type == "card":
            trgt_card = Card.objects.get(list=trgt_list, position=data["target_id"]["target_id_card"])

            if trgt_field == "name":
                trgt_card.title = new_value
            elif trgt_field == "position":
                move_object(trgt_card.position, new_value, trgt_list, Card)
                trgt_card.position = new_value
            elif trgt_field == "description":
                trgt_card.description = new_value
            elif trgt_field == "date":
                trgt_card.date = datetime.fromtimestamp(new_value)
            elif trgt_field == "img":
                pass  # TODO
            elif trgt_field == "checks":
                pass  # TODO
            elif trgt_field == "members":
                pass  # TODO
            elif trgt_field == "tags":
                trgt_card.tags = json.loads(new_value)

            trgt_card.save()

        return HttpResponse("Content edited", status=200)
    else:
        return HttpResponse(f"Board {data['target_id']['target_id_board']} not found", status=406)


@login_required
@require_http_methods(["POST"])
def create_category(request):
    user, data = get_user_data(request)

    """
    Formato JSON (niente di che)
    {
        new_cat_name: <nome>
    }
    """

    name = data["new_cat_name"]

    Category.objects.create(user=user, name=name)

    return HttpResponse("Boh non saprei come una cosa così potrebbe fallire tbh", status=200)
