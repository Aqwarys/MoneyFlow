import django_filters
from django import forms
from .models import Transaction, Status, Category, SubCategory

class TransactionFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date', 'class': 'form-control'
        })
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sub_category = django_filters.ModelChoiceFilter(
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Transaction
        fields = ['date', 'status', 'category', 'sub_category']
