from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CreateAccountForm(forms.Form):

    acc_number = forms.CharField(initial='MB000'+get_random_string(length=15,allowed_chars="1234567890"))
    balance = forms.FloatField()


