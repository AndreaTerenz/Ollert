import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from website.models import Board, List, Card, Category, UserProfile


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


def get_username(user: UserProfile):
    try:
        return User.objects.get(userprofile=user).username
    except ObjectDoesNotExist:
        return ""


def get_board(user: UserProfile, name, owner: UserProfile = None):
    try:
        if not owner or owner == user:
            return Board.objects.get(user=user, name=name)
        else:
            output = Board.objects.get(user=owner, name=name)
            if is_board_member(output, user):
                return output
            return None
    except ObjectDoesNotExist:
        return None


def get_user_boards(user: UserProfile):
    return [get_board_short_dict(b) for b in Board.objects.filter(user=user)]


def is_board_member(b: Board, user: UserProfile):
    return get_username(user) in b.members.keys()


def get_user_permission(b: Board, user: UserProfile):
    if is_board_member(b, user):
        return b.members[get_username(user)]

    return None


def get_shared_boards(user: UserProfile):
    boards = []
    for b in Board.objects.filter():
        if is_board_member(b, user):
            data = get_board_short_dict(b)
            data.update({
                "owner": get_username(b.user),
                "permission": get_user_permission(b, user)
            })
            boards.append(data)
    return boards


def get_board_short_dict(board_obj: Board):
    data = {
        "name": board_obj.name,
        "favorite": board_obj.favorite,
        "description": board_obj.description
    }
    if cat := board_obj.category:
        data.update({"category": cat.name})

    return data


def get_board_dictionary(board_obj: Board, is_owner=True, can_edit=True):
    output: dict = {
        "board_name": board_obj.name,
        "board_owner": get_username(board_obj.user),
        "board_background": board_obj.background,
        "board_description": board_obj.description,
        "is_owner": is_owner,
        "can_edit": can_edit
    }

    lists = [get_list_dict(l_obj, can_edit=can_edit) for l_obj in get_lists_in_board(board_obj)]
    output.update({
        "board_lists": lists
    })

    if not is_owner:
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
        return List.objects.get(position=pos, user=parent_board.user, board=parent_board)
    except ObjectDoesNotExist:
        return None


def get_lists_in_board(board: Board):
    return List.objects.filter(user=board.user, board=board)


def get_list_dict(l_obj: List, can_edit=True):
    l = {
        "title": l_obj.title,
        "id": f"list_{l_obj.position}",
        "cards": [],
        "can_edit": can_edit
    }
    for c_obj in get_cards_in_list(l_obj):
        l["cards"].append(get_card_dict(c_obj, l_obj))

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


def get_user_data(request) -> tuple:
    user = get_authenticated_user(request)
    data = json.loads(request.body)

    return user, data
