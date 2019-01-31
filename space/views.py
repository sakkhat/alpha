
from django.shortcuts import (render,HttpResponse, redirect)
from django.contrib.auth import (authenticate, login as auth_login, 
	logout as auth_logout )
from django.contrib.auth.decorators import (login_required)
from django.contrib import messages

from .models import (
	Account, Post, PostMedia, Profile)
from .forms import (LoginForm, RegistrationForm)
from . import variables as var

# Create your views here.


def login(request):
	"""
	Account authenticate and login function
	
	Get method:
		render the login page

	Post method params:
		`id_name` : User ID 
			or
		`phone` : Account Phone Number
			and
		`password` : Account Password
	"""
	context = {}

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user_id = form.cleaned_data['user_id']
			password = form.cleaned_data['password']

			# Phone Number
			if user_id.isdigit():
				pass


	return render(request, 'login.html', {} )


@login_required(login_url = var.LOGIN_URL)
def logout():
	pass


