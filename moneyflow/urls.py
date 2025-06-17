from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('transaction.urls')),


    # API
    path('api/v1/user/', include('user.api.user.urls')),
    path('api/v1/', include('transaction.api.transaction.urls')),
]
