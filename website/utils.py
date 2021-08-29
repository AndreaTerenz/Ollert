from typing import Union

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from website.models import Board, List


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
