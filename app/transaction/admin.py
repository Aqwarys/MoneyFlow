from django.contrib import admin
from .models import Transaction, Status, TransactionType, Category, SubCategory

admin.site.register(TransactionType)
admin.site.register(Status)
admin.site.register(SubCategory)
admin.site.register(Transaction)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)