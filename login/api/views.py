from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import generics
from django.http import JsonResponse
from urllib.parse import urlparse
import urllib.request as urllib2
import io
import datetime



class UsersViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "username"]



from django.contrib.auth import authenticate
class decentralizationUser(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    def post(self,request):
        user = authenticate(request, username=request.data["username"], password=request.data["password"])
        group = None
        if user.groups.exists():
            group = user.groups.all()[0].name
        if group == "admin":
            return JsonResponse({
                "message": "Is admin",
            })
        return JsonResponse({
            "message": "Not admin",
        })




