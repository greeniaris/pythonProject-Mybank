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
    balance = forms.DecimalField(decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acc_number'].initial = 'MB000' + get_random_string(length=15, allowed_chars="1234567890")

class TransfermoneyForm(forms.Form):

    sender_acc = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    recepient_acc = forms.CharField(max_length=20)
    ammount = forms.DecimalField(decimal_places=2)