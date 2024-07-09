from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, AllowAny
from .serializers import (
    TaskSerializer,
    LogSerializer,
    UserSerializer
)
from .models import (
    Task,
    Log
)
from .filters import (
    TaskFilter,
    LogFilter
)


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class CustomObtainAuthToken(ObtainAuthToken):
#     permission_classes = [AllowAny]
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={
#                 'request': request
#             }
#         )

#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get(user=user)
#         return Response({
#             'token': token.key
#         })


class LogViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DjangoModelPermissions,)

    queryset = Log.objects.all()
    serializer_class = LogSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LogFilter


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,) 
    permission_classes = (DjangoModelPermissions,)
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
