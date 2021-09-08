from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Model
from colorful.fields import RGBColorField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


# "estende" il modello User fornito da django admin
class UserProfile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='propics', default='propics/default_propic.png')


class Category(Model):
    name = models.CharField(
        max_length=128
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("name", "user")


class Board(Model):
    name = models.CharField(
        max_length=128
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    tags = models.JSONField(
        default=dict
    )
    lists_count = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(32)]  # una board può contenere al massimo 32 liste
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    background = RGBColorField(
        default='#222'
    )
    favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "user")


class List(Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(
        default=0
    )
    title = models.CharField(
        max_length=64,
        blank=False
    )
    cards_count = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(64)]  # una lisa può contenere al massimo 64 card
    )

    class Meta:
        unique_together = ("position", "board", "user")


@receiver(post_delete, sender=List)
def on_list_delete(sender, instance: List, using, **kwargs):
    p_board = instance.board
    user = p_board.user
    for l in List.objects.filter(user=user, board=p_board, position__gt=instance.position):
        l.position -= 1
        l.save()
    p_board.lists_count -= 1


class Card(Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE
    )
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(
        default=0
    )
    title = models.CharField(
        max_length=128,
        blank=False
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    image = models.ImageField(
        blank=True,
        null=True
    )
    tags = models.JSONField(default=dict)
    checklist = models.JSONField(default=dict)
    members = models.JSONField(default=dict)

    class Meta:
        unique_together = ("position", "list", "board", "user")


@receiver(post_delete, sender=Card)
def on_card_delete(sender, instance: Card, using, **kwargs):
    p_list = instance.list
    p_board = p_list.board
    user = p_board.user
    for c in Card.objects.filter(user=user, board=p_board, list=p_list,
                                 position__gt=instance.position):
        c.position -= 1
        c.save()
    p_list.cards_count -= 1


class Notifications(models.Model):
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    board = models.ForeignKey(Board, related_name='board', on_delete=models.CASCADE, null=True)
    # rappresenta la data in cui avviene la notifica
    date = models.DateTimeField(default=timezone.now)
    # Se l'utente ha letto la notifica o meno (per evitare che venga visualizzata come nuova tutte le volte che accedi)
    user_has_seen = models.BooleanField(default=False)
