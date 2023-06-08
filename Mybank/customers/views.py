from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Accounts, Customers, Transactions
from .forms import RegistrationForm, CreateAccountForm , TransfermoneyForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


def welcome(request):
    return render(request, 'welcome.html')


def our_bank(request):
    return render(request, 'our_bank.html')


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
            if Accounts.objects.filter(acc_number=form.cleaned_data['acc_number']).exists():
                messages.error(request,f"account already exists")
                form = CreateAccountForm
            else:
                create_obj.save()
                messages.success(request, f"succesfully created account {create_obj.acc_number} with {create_obj.balance}")
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

def send_balance_form(request):
    my_acc = Accounts.objects.filter(owner=request.user)
    context = {
        'object' : my_acc
    }
    return render(request, 'transfer3.html', context)

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
            return redirect('transfer3')

        try:
            recipient_account = Accounts.objects.get(acc_number=recipient_account_number)
        except Accounts.DoesNotExist:
            messages.error(request, 'Recipient account number does not exist.')
            return redirect('transfer3')

        if sender_account_number == recipient_account_number:
            messages.error(request, 'Recipient account number must be different')
            return redirect('transfer3')

        if sender_account.balance >= amount and sender_account.owner == request.user:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            trans_acc = Transactions(sender_acc= sender_account, recipient_acc= recipient_account, amount= amount)
            trans_acc.save()
            messages.success(request, f'{amount}€ successfully transferred to {recipient_account_number}')
            return redirect('transfer3')

        else:
            messages.error(request, 'Λαθος στοιχεια')
        return redirect('transfer3')
    return redirect('transfer3')


@login_required()
def my_transactions(request):
    user = request.user
    sender = Accounts.objects.filter(owner= user).all()
    saw_me = Transactions.objects.filter((Q(sender_acc__in=sender) | Q(recipient_acc__in=sender)))
    saw_me = saw_me.order_by('-date')
    paginator = Paginator(saw_me, per_page=10)
    page_number = request.GET.get('page', 1)
    pagin = paginator.get_page(page_number)
    context = {

        'pagin' : pagin,
    }
    return render(request, 'mytransactions.html', context)

@login_required()
def account(request, acc_number):
    query = Accounts.objects.get(acc_number = acc_number)
    saw_me = Transactions.objects.filter((Q(sender_acc=query) | Q(recipient_acc=query)))
    saw_me = saw_me.order_by('-date')
    paginator = Paginator(saw_me, per_page=10)
    page_number = request.GET.get('page', 1)
    pagin = paginator.get_page(page_number)
    context = {
        'object': query,
        'pagin' : pagin
    }
    return render(request, 'account.html', context=context)

@login_required()
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
                    return redirect(reverse('transfer2', args=[acc_number]))

                try:
                    recipient_account = Accounts.objects.get(acc_number=recipient_account_number)
                except Accounts.DoesNotExist:
                    messages.error(request, 'Recipient account number does not exist.')
                    return redirect(reverse('transfer2', args=[acc_number]))

                if sender_account_number == recipient_account_number:
                    messages.error(request, 'Recipient account number must be different')
                    return redirect(reverse('transfer2', args=[acc_number]))

                if sender_account.balance >= amount and sender_account.owner == request.user:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    trans_acc = Transactions(sender_acc=sender_account, recipient_acc=recipient_account, amount=amount)
                    trans_acc.save()
                    messages.success(request, f'{amount} successfully transferred to {recipient_account_number}')
                    return redirect(reverse('account', args=[acc_number]))

                else:
                    messages.error(request, 'Λαθος στοιχεια')


    return render(request, 'transfer_2.html',{'form':form})
