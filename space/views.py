
from django.shortcuts import (render,HttpResponse, redirect)
from django.contrib.auth import (authenticate, login as auth_login, 
	logout as auth_logout )
from django.contrib.auth.decorators import (login_required)
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import (
	Account, Post, PostMedia, Profile)
from .forms import (LoginForm, RegistrationForm)
from . import variables as var

# Create your views here.

def register(request):
	
	context = {}

	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():

			id_name = form.cleaned_data['id_name']
			phone = form.cleaned_data['phone']
			password = form.cleaned_data['password']
			display_name = form.cleaned_data['display_name']
			description = form.cleaned_data['description']
			address = form.cleaned_data['address']


			# create an account and a profile against this account
			# return to the profile section


	form = RegistrationForm()
	context['form'] = form
	return render(request, 'auth/register.html', context)


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

			# check the user_id is phone or not
			if user_id.isdigit():
				# fetch the id_name from phone
				try:
					account = Account.objects.get(phone=user_id)
					user_id = account.id_name
				except ObjectDoesNotExist as e:
					pass

			user = authenticate(id_name=user_id, password=password)

			if user is None:
				messages(request, 'Invalid account id or password')
			else:
				auth_login(request, user)
				return redirect('/')

	form = LoginForm()
	context['form'] = form
	return render(request, 'auth/login.html', context)


@login_required(login_url = var.LOGIN_URL)
def logout(request):
	auth_logout(request)
	return HttpResponse('Logged out')


def change_password(request):
	pass

def forget_password(request):
	pass

	