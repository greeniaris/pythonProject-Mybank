from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from django.urls import reverse

# Create your models here.
class Customers(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE, related_name='customer')
    til = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.owner}'

class Accounts(models.Model):

    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    acc_number = models.CharField(primary_key=True, max_length=20)
    balance = models.FloatField(default= 0)

    def __str__(self):
        return f'Customer : {self.owner} with account number {self.acc_number} and balance: {self.balance} €'


class Transactions(models.Model):

    sender_acc = models.ForeignKey(Accounts,on_delete=models.CASCADE, related_name='sender_acc')
    recipient_acc = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='recipient_acc')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"{self.sender_acc} to {self.recipient_acc} Ammount {self.amount}"