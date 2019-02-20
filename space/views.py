
from django.shortcuts import (render,HttpResponse, redirect)
from django.contrib.auth import (authenticate, login as auth_login, 
	logout as auth_logout )
from django.contrib.auth.decorators import (login_required)
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import (
	Account, Product, PostMedia)
from .forms import (LoginForm, RegistrationForm)
from . import variables as var

# Create your views here.
	
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .api.serializer import PostSerializer, AccountSerializer

class PostViewSet(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = PostSerializer