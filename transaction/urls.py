from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'transaction'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name="transaction:main", permanent=True)),
    path('main/', views.index, name='main'),
    path('create/', views.create_transaction, name='create'),
    path('create/', views.create_transaction, name='create'),
    path('update/<int:pk>', views.update_transaction, name='update'),
    path('delete/<int:pk>', views.delete_transaction, name='delete'),
    # Utils
    path('utils/', views.create_utils, name='utils'),
    path('utils/status/delete/<int:pk>/', views.delete_status, name='delete_status'),
    path('utils/type/delete/<int:pk>/', views.delete_transaction_type, name='delete_transaction_type'),
    path('utils/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('utils/subcategory/delete/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),

    # ajax
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
