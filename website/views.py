import datetime
import json
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.views import View
from django.views.decorators.http import require_http_methods

from .models import UserProfile, Category, Card, Notification, NotificationType
from .forms import NewUserForm
from .utils import *
from icecream import ic


# ic.disable()


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
        data = get_board_dictionary(board_obj)

        # Usa i dati ottenuti per generare l'html
        return render(request, 'board/board.html', status=200, context=data)
    else:
        for b in Board.objects.filter(name=name):
            if request.user.username in b.members:
                data = get_board_dictionary(b, user=b.user)

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

    board_name = data["board_name"]

    # FIXME: bisognerebbe capire bene cosa ritornare invece di mere HttpResponse
    if board_obj := get_user_board(user, board_name):
        for edit in data["edits"]:
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

    trgt_type = data["target_type"]
    if trgt_board := get_user_board(user, data["target_id"]["target_id_board"]):
        trgt_content: dict = data["new_data"]

        ic(trgt_content)

        if trgt_type == "list":
            pos = trgt_board.lists_count
            title = trgt_content["list_name"]

            List.objects.create(
                user=user,
                board=trgt_board,
                position=pos,
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
            trgt_list = List.objects.get(board=trgt_board, position=int(data["target_id"]["target_id_list"]))
            pos = trgt_list.cards_count

            c_obj = Card.objects.create(
                user=user,
                board=trgt_board,
                list=trgt_list,
                position=pos,
                title=trgt_content["card_name"],
                description=trgt_content.get("card_descr", None),
                date=trgt_content.get("card_date", None),
                # TODO: mancano immagine, checklist e membri
                # image
                checklist=trgt_content.get("card_checks", {}),
                members=trgt_content.get("card_members", {}),
                tags=trgt_content.get("card_tags", {})
            )

            trgt_list.cards_count += 1
            trgt_list.save()

            context = get_card_dict(c_obj, trgt_list)

            return render(request, "board/card.html", context={"data": context})
    else:
        return HttpResponse(f"Board {data['target_id']['target_id_board']} not found", status=406)


@login_required
@require_http_methods(["POST"])
def delete_board_content(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    if parent_board := get_user_board(user, data["board"]):
        for target in data["targets"]:
            trgt_type = target["target_type"]
            trgt_id = target["target_id"]

            trgt_list = List.objects.get(position=trgt_id["target_id_list"], board=parent_board,
                                         user=parent_board.user)

            if trgt_type == "list":
                trgt_list.delete()
            elif trgt_type == "card":
                trgt_card = Card.objects.get(position=trgt_id["target_id_card"],
                                             list=trgt_list,
                                             board=parent_board,
                                             user=user)

                trgt_card.delete()

        return render(request, "board/board_lists.html",
                      context={"lists": [get_list_dict(l) for l in get_lists_in_board(parent_board)]})
    else:
        return HttpResponse(f"Board {data['target_id']['target_id_board']} not found", status=406)


@login_required
@require_http_methods(["POST"])
def edit_board_content(request):
    user = get_authenticated_user(request)
    data = json.loads(request.body)

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
                trgt_card.checklist = json.loads(new_value)
            elif trgt_field == "members":
                trgt_card.members = json.loads(new_value)
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

    name = data["new_cat_name"]

    Category.objects.create(user=user, name=name)

    return render(request, "profile/profile-category-list.html", context={"categories": get_user_categories(user)})


@login_required
@require_http_methods(["POST"])
def delete_category(request):
    user, data = get_user_data(request)

    name = data["cat_name"]

    Category.objects.get(user=user, name=name).delete()

    return render(request, "profile/profile-category-list.html", context={"categories": get_user_categories(user)})



@login_required
@require_http_methods(["POST"])
# "rename" invece di "edit" perchè è l'unica modifica possibile
def rename_category(request):
    user, data = get_user_data(request)

    name = data["cat_name"]

    cat = Category.objects.get(user=user, name=name)
    cat.name = data["new_value"]
    cat.save()

    return HttpResponse("Boh non saprei come una cosa così potrebbe fallire tbh", status=200)


class ManageBoardUser(View):
    def post(self, request, *args, **kwargs):
        user, data = get_user_data(request)

        """
        Formato JSON:
        {
            receiver: <nome destinatario>
            board_name: <nome board>
            action: <ADDED|REMOVED>
        }
        """

        receiver = data["receiver"]
        board_name = data["board_name"]
        action = NotificationType[data["action"]]

        receiver_obj = User.objects.get(username=receiver)
        board_obj = Board.objects.get(user=user, name=board_name)

        if action == NotificationType.ADDED:
            board_obj.members += [receiver]
        elif action == NotificationType.REMOVED:
            board_obj.members.remove(receiver)

        board_obj.save()

        Notification.objects.create(
            from_user=request.user,
            to_user=receiver_obj,
            board=board_obj,
            notif_type=NotificationType.ADDED.value
        )

        return HttpResponse("ok")


class ManageCardAssignee(View):
    def post(self, request, *args, **kwargs):
        user, data = get_user_data(request)

        """
        Formato JSON:
        {
            receiver: <nome destinatario>
            board_name: <nome board>
            list_id: <pos lista>
            card_id: <pos card>
            action: <ADDED|REMOVED>
        }
        """

        receiver = data["receiver"]
        board_obj = Board.objects.get(user=user, name=data["board_name"])
        list_obj = List.objects.get(board=board_obj, position=data["list_id"])
        card_obj = Card.objects.get(list=list_obj, position=data["card_id"])
        action = NotificationType[data["action"]]

        receiver_obj = User.objects.get(username=receiver)

        if action == NotificationType.ADDED:
            card_obj.members.append(receiver)
        elif action == NotificationType.REMOVED:
            card_obj.members.remove(receiver)

        card_obj.save()

        Notification.objects.create(
            from_user=user,
            to_user=receiver_obj,
            card=card_obj,
            notif_type=action
        )

        return HttpResponse("ok")


class BoardNotification(View):
    def get(self, request, notification_pk, board_name, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('get-board', name=board_name)


class CardNotification(View):
    def get(self, request, notification_pk, card_id, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        card = Card.objects.get(id=card_id)
        parent_list = card.list
        parent_board = parent_list.board

        return redirect('get-board', name=parent_board.name)
