from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'transaction'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name="transaction:main", permanent=True)),
    path('dashboard/', views.index, name='main'),
    path('create/', views.create_transaction, name='create'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
