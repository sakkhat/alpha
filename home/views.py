from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def index(request):
	return render(request, 'home.html', {})

def about(request):
	return render(request, 'about.html', {})

def auth(request):
	return render(request, 'auth.html', {})
