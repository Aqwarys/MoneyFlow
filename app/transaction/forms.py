from django import forms
from .models import Transaction, Category, TransactionType, SubCategory, Status


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status', 'transaction_type', 'category', 'sub_category', 'amount', 'comment', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name', 'is_expense']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
