from rest_framework import generics
from .models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = ReadOnlyUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOnlyUserSerializer
        else:
            return self.serializer_class
