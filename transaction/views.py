from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from .models import Transaction, Category, TransactionType, SubCategory, Status
from .forms import TransactionForm, StatusForm, TransactionTypeForm, CategoryForm, SubCategoryForm
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

@login_required(login_url='user:login')
def create_utils(request):
    status_form = StatusForm(prefix='status')
    type_form = TransactionTypeForm(prefix='type')
    category_form = CategoryForm(prefix='category')
    subcategory_form = SubCategoryForm(prefix='subcategory')

    if request.method == 'POST':
        if 'submit_status' in request.POST:
            status_form = StatusForm(request.POST, prefix='status')
            if status_form.is_valid():
                status_form.save()
                return redirect('transaction:utils')

        elif 'submit_type' in request.POST:
            type_form = TransactionTypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                return redirect('transaction:utils')

        elif 'submit_category' in request.POST:
            category_form = CategoryForm(request.POST, prefix='category')
            if category_form.is_valid():
                category_form.save()
                return redirect('transaction:utils')

        elif 'submit_subcategory' in request.POST:
            subcategory_form = SubCategoryForm(request.POST, prefix='subcategory')
            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('transaction:utils')

    context = {
        'statusForm': status_form,
        'typeForm': type_form,
        'categoryForm': category_form,
        'subcategoryForm': subcategory_form,
        'statuses': Status.objects.all(),
        'transactiontypes': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
    }

    return render(request, 'transaction/utils.html', context)

@login_required(login_url='user:login')
def delete_status(request, pk):
    get_object_or_404(Status, pk=pk).delete()
    return redirect('transaction:utils')

@login_required(login_url='user:login')
def delete_transaction_type(request, pk):
    get_object_or_404(TransactionType, pk=pk).delete()
    return redirect('transaction:utils')

@login_required(login_url='user:login')
def delete_category(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect('transaction:utils')

@login_required(login_url='user:login')
def delete_subcategory(request, pk):
    get_object_or_404(SubCategory, pk=pk).delete()
    return redirect('transaction:utils')