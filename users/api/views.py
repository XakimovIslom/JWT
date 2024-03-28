from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status

User = get_user_model()


# class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"
#
#     def get_queryset(self, *args, **kwargs):
#         assert isinstance(self.request.user.id, int)
#         return self.queryset.filter(id=self.request.user.id)
#
#     @action(detail=False)
#     def me(self, request):
#         serializer = UserSerializer(request.user, context={"request": request})
#         return Response(status=status.HTTP_200_OK, data=serializer.data)

class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        username = serializer.data.get('username')
        tokens = User.objects.get(username=username).tokens
        user_data['tokens'] = tokens
        return Response({'success': True, 'data': user_data}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
