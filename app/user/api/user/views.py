from rest_framework.generics import ListCreateAPIView


from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from user.models import User



class UserListAPI(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)