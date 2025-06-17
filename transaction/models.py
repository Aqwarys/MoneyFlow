from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

from dateutil.relativedelta import relativedelta


from user.models import User

def subtract_month():
    return timezone.now().date() - relativedelta(months=1)

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'


class TransactionType(models.Model):
    name = models.CharField(max_length=100)
    is_expense = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='categories')


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category'])
        ]
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=False, blank=False)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    comment = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(auto_now_add=False, editable=True, default=timezone.now().date)

    class Meta:
        ordering = [
            'status',
            'transaction_type',
            'category',
            'date',
        ]
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['category']),
            models.Index(fields=['sub_category']),
        ]
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'


    def clean(self):

        if self.category.transaction_type != self.transaction_type:
            raise ValidationError("Category does not belong to the selected transaction type.")

        if self.sub_category.category != self.category:
            raise ValidationError("Subcategory does not belong to the selected category.")


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.created_at} | ${self.amount}"


    def monthly_expenses(self, request):
        return (
            Transaction.objects
            .filter(user=request.user, transaction_type__is_expense=True, date__gte=subtract_month())
            .aggregate(total=Sum('amount'))['total'] or 0
        )

    def monthly_income(self, request):
        return (
            Transaction.objects
            .filter(user=request.user, transaction_type__is_expense=False, date__gte=subtract_month())
            .aggregate(total=Sum('amount'))['total'] or 0
        )
