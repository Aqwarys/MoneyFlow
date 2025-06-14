from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Transaction, Category, TransactionType, SubCategory
from .forms import TransactionAddForm


@login_required(login_url='user:login')
def index(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': transactions
    }
    return render(request, 'transaction/main.html', context=context)


def create_transaction(request):
    form = TransactionAddForm()

    if request.method == "POST":
        form = TransactionAddForm(request.POST)
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