from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ImageField, EmailField


class NewUserForm(UserCreationForm):
    propic: ImageField = ImageField(required=False)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "propic",)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
