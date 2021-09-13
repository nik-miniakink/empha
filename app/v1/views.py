from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOnlyUserSerializer
        else:
            return ReadOnlyUserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyUserSerializer
        return WriteOnlyUserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
