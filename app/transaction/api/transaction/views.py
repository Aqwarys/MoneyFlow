from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from user.api.user.permissions import IsOwnerOrReadOnly
from . import serializers
from transaction.models import (
    Status,
    TransactionType,
    Category,
    SubCategory,
    Transaction
)


class StatusAPIView(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [IsAuthenticated,]


class TransactionTypeAPIView(ListCreateAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = serializers.TransactionTypeSerializer
    permission_classes = [IsAuthenticated,]


class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk=None):
        if pk:
            category = Category.objects.get(pk=pk)
            return Response({"category": serializers.CategorySerializer(category, many=False).data})
        else:
            return Response({"categories": serializers.CategorySerializer(Category.objects.all(), many=True).data})

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "Missing pk"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Category.objects.get(pk=pk)
        except:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CategorySerializer(request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryAPIView(ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer
    permission_classes = [IsAuthenticated,]





class TransactionAPIViewSet(ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    permission_classes = [IsOwnerOrReadOnly,]


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Transaction.objects.filter(user=self.request.user).order_by('-date')
        return Transaction.objects.none()


    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': serializers.CategorySerializer(category, many=False).data})

    @action(methods=['get'], detail=True)
    def transaction_type(self, request, pk=None):
        trans_type = TransactionType.objects.get(pk=pk)
        return Response({'transaction_type': serializers.TransactionTypeSerializer(trans_type, many=False).data})

    @action(methods=['get'], detail=True)
    def subcategory(self, request, pk=None):
        sub_category = SubCategory.objects.get(pk=pk)
        return Response({'subcategory': serializers.SubCategorySerializer(sub_category, many=False).data})
