from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter


from . import views

router = DefaultRouter()
router.register(r'transactions', views.TransactionAPIViewSet, basename='transaction')

urlpatterns = [
    path('status/', views.StatusAPIView.as_view(), name='status-list'),
    path('transaction-type/', views.TransactionTypeAPIView.as_view(), name='transaction-type-list'),
    path('category/', views.CategoryAPIView.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryAPIView.as_view(), name='category-list'),
    path('sub-category/', views.SubCategoryAPIView.as_view(), name='sub-category-list'),
    path('transaction/', include(router.urls)),
]
