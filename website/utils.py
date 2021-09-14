import json
from typing import Union

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from icecream import ic

from website.models import Board, List, Card, Category


def handle_form_errors(request, form, header):
    key = list(form.errors.keys())[0]
    error = form.errors[key][0]

    messages.error(request, f"{header}{error}")


def get_authenticated_user(request):
    output = request.user
    return output.userprofile if output.is_authenticated else None


def get_user_from_username(name):
    try:
        return User.objects.get(username=name).userprofile
    except ObjectDoesNotExist:
        return None


def get_user_board(user, name):
    try:
        return Board.objects.get(user=user, name=name)
    except ObjectDoesNotExist:
        return None


def get_user_boards(user):
    boards = []
    for b in Board.objects.filter(user=user):
        data = {
            "name": b.name,
            "favorite": b.favorite,
            "description": b.description
        }
        if cat := b.category:
            data.update({"category": cat.name})

        boards.append(data)
    return boards


def get_board_dictionary(board_obj: Board, other_user=None):
    lists = []

    for l_obj in get_lists_in_board(board_obj, user=other_user):
        lists.append(get_list_dict(l_obj))

    output: dict = {
        "board_name": board_obj.name,
        "board_background": board_obj.background,
        "board_description": board_obj.description,
        "board_lists": lists,
        "is_owner": not other_user
    }

    if not other_user:
        output.update({
            "board_members": board_obj.members,
        })

    return output


def get_user_category(user, name):
    if name == "NaN":
        return None

    try:
        return Category.objects.get(user=user, name=name)
    except ObjectDoesNotExist:
        return None


def get_user_categories(user):
    cats = []
    for c in Category.objects.filter(user=user):
        cats.append(c.name)
    return cats


def get_list_in_board(pos, parent_board: Board):
    try:
        ic(parent_board.user, parent_board, pos)
        return List.objects.get(position=pos, user=parent_board.user, board=parent_board)
    except ObjectDoesNotExist:
        return None


def get_lists_in_board(board: Board, user=None):
    if not user:
        user = board.user
    return List.objects.filter(user=user, board=board)


def get_list_dict(l_obj: List):
    l = {
        "list_title": l_obj.title,
        "list_id": f"list_{l_obj.position}",
        "list_cards": []
    }
    for c_obj in get_cards_in_list(l_obj):
        l["list_cards"].append(get_card_dict(c_obj, l_obj))

    return l


def get_card_in_list(pos, parent_list: List):
    try:
        board = parent_list.board
        return Card.objects.get(position=pos, user=board.user, board=board, list=parent_list)
    except ObjectDoesNotExist:
        return None


def get_card_dict(c_obj: Card, l_obj: List):
    ids = get_card_ids(l_obj, c_obj.position)

    date = c_obj.date
    ic(date)

    return {
        "card_unique_id": ids[0],
        "card_json_id": ids[1],
        "card_title": c_obj.title,
        "card_date": date if date else None,
        # TODO: L'IMMAGINE CAZZOCULO
        "card_descr": c_obj.description,
        "card_members": c_obj.members,
        "card_checks": c_obj.checklist
    }


def get_card_ids(parent_list, pos):
    id = f"{parent_list.position}_{pos}"
    json_id = f"{parent_list.position}_{pos}_json"

    return id, json_id


def get_cards_in_list(parent_list: List):
    return Card.objects.filter(user=parent_list.board.user, board=parent_list.board, list=parent_list)


def move_object(current_pos: int, new_pos: int, parent_obj: Union[Board, List], obj_type):
    if current_pos != new_pos:
        # FIXME: MADRE DE DIOS CHE ROBA INEFFICENTE
        if current_pos < new_pos:
            for c in obj_type.objects.filter(parent_obj,
                                             position__range=range(current_pos + 1, new_pos)):
                c.position -= 1
                c.save()
        else:
            for c in obj_type.objects.filter(parent_obj,
                                             position__range=range(new_pos, current_pos - 1)):
                c.position += 1
                c.save()


def get_user_data(request) -> tuple:
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    return user, data
