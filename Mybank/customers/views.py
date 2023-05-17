from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Accounts, Customers, Transactions
from .forms import RegistrationForm, CreateAccountForm , TransfermoneyForm
from django.contrib import messages
from django.db.models import Q


def welcome(request):
    return render(request, 'welcome.html')


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customers.objects.create(owner=user)
            customer.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('welcome_page')
    else:
        form = RegistrationForm()
    return render(request, 'register_user.html', {'form': form})


@login_required()
def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            # Create a new object in the database
            create_obj = Accounts(owner=request.user, acc_number=form.cleaned_data['acc_number'],\
                                  balance=form.cleaned_data['balance'])
            create_obj.save()
            return redirect('user_profile')
    else:
        form = CreateAccountForm()
    return render(request, 'create_account.html', {'form': form})


@login_required()
def profile_page(request):
    user = request.user
    query = Accounts.objects.filter(owner=user).all()
    context = {
        'object': query,
        'user': user
    }
    return render(request, 'user_profile.html', context=context)


@login_required
def send_balance(request):
    if request.method == 'POST':
        sender_account_number = request.POST.get('sender_account_number')
        recipient_account_number = request.POST.get('recipient_account_number')
        ammount = request.POST.get('amount')
        amount = float(ammount)
        try:
            sender_account = Accounts.objects.get(acc_number=sender_account_number)
        except Accounts.DoesNotExist:
            messages.error(request, 'Sender account number does not exist.')
            return redirect('transfer')

        try:
            recipient_account = Accounts.objects.get(acc_number=recipient_account_number)
        except Accounts.DoesNotExist:
            messages.error(request, 'Recipient account number does not exist.')
            return redirect('transfer')

        if sender_account.balance >= amount and sender_account.owner == request.user:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            trans_acc = Transactions(sender_acc= sender_account, recipient_acc= recipient_account, amount= amount)
            trans_acc.save()
            messages.success(request, f'{amount} successfully transferred to {recipient_account_number}')

        else:
            messages.error(request, 'Λαθος στοιχεια')

    # Get any messages that have been sent to the user
    all_messages = messages.get_messages(request)

    # Pass the messages to the template
    context = {
            'messages': all_messages,
        }

    return render(request, 'transfer.html', context)

@login_required()
def my_transactions(request):

    user = request.user
    sender = Accounts.objects.filter(owner= user).all()
    saw_me = Transactions.objects.filter((Q(sender_acc__in=sender) | Q(recipient_acc__in=sender)))
    saw_me = saw_me.order_by('-date')
    context = {
        'object' : saw_me
    }
    return render(request, 'mytransactions.html', context)

def account(request, acc_number):
    query = Accounts.objects.get(acc_number = acc_number)
    saw_me = Transactions.objects.filter((Q(sender_acc=query) | Q(recipient_acc=query)))
    saw_me = saw_me.order_by('-date')
    context = {
        'object': query,
        'trans' : saw_me,
    }
    return render(request, 'account.html', context=context)

def send_moneys(request, acc_number):

    form = TransfermoneyForm(initial={'sender_acc': acc_number})

    if request.method == 'POST':
        form = TransfermoneyForm(request.POST)
        if form.is_valid():
            if request.method == 'POST':
                sender_account_number = request.POST['sender_acc']
                recipient_account_number = request.POST['recepient_acc']
                ammount = request.POST['ammount']
                amount = float(ammount)
                try:
                    sender_account = Accounts.objects.get(acc_number=sender_account_number)
                except Accounts.DoesNotExist:
                    messages.error(request, 'Sender account number does not exist.')
                    return redirect('transfer')

                try:
                    recipient_account = Accounts.objects.get(acc_number=recipient_account_number)
                except Accounts.DoesNotExist:
                    messages.error(request, 'Recipient account number does not exist.')
                    return redirect('transfer')

                if sender_account.balance >= amount and sender_account.owner == request.user:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    trans_acc = Transactions(sender_acc=sender_account, recipient_acc=recipient_account, amount=amount)
                    trans_acc.save()
                    messages.success(request, f'{amount} successfully transferred to {recipient_account_number}')

                else:
                    messages.error(request, 'Λαθος στοιχεια')

            # Get any messages that have been sent to the user
            all_messages = messages.get_messages(request)

            # Pass the messages to the template
            context = {
                'messages': all_messages,
            }

            return render(request, 'transfer.html', context)


    return render(request, 'transfer_2.html', {'form': form})
