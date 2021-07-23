from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


# "estende" il modello User fornito da django admin
class UserProfile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='propics', default='propics/default_propic.png')


class Category(Model):
    name = models.CharField(
        max_length=128,
        null=False
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("name", "user")


class Board(Model):
    name = models.CharField(
        max_length=128,
        null=False
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        null=True
    )
    favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "user")


class List(Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(
        default=0
    )
    title = models.CharField(
        max_length=64,
        null=False
    )

    class Meta:
        unique_together = ("id", "board")


class Card(Model):
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(
        default=0
    )
    title = models.CharField(
        max_length=128,
        null=False
    )
    description = models.TextField(null=False)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField()
    checklist = models.JSONField()
    tags = models.JSONField()
    members = models.JSONField()

    class Meta:
        unique_together = ("id", "list")
