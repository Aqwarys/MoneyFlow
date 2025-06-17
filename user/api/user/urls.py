from django.urls import path

from . import views

urlpatterns = [
    path('users/' , views.UserListAPI.as_view(), name='user-list'),
]
