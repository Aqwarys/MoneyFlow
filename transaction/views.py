from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Transaction, Category, TransactionType, SubCategory
from .forms import TransactionForm
from .filters import TransactionFilter


@login_required(login_url='user:login')
def index(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    filterset = TransactionFilter(request.GET, queryset=transactions)
    context = {
        'filter': filterset,
        'transactions': filterset.qs
    }
    return render(request, 'transaction/main.html', context=context)


def create_transaction(request):
    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction:main')

    return render(request, 'transaction/create_transaction.html', {
        'form': form
    })

def load_categories(request):
    type_id = request.GET.get('type_id')
    print('here')
    categories = Category.objects.filter(transaction_type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

@login_required(login_url='user:login')
def update_transaction(request, pk):
    instance = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=instance)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(reverse_lazy('transaction:main'))
    else:
        form = TransactionForm(instance=instance)
    context = {
        'form': form
    }

    return render(request, 'transaction/update_transaction.html', context=context)


@login_required(login_url='user:login')
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    return redirect('transaction:main')