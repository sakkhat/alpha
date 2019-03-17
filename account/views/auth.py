from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.forms import SignupForm,SigninForm,PasswordChangeForm
from account.models import Account, UserManager

from generic.variables import LOGIN_URL
from generic import views

def signup(request):
	if request.user.is_authenticated:
		return redirect('/')

	context = {}
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)

			return redirect('/account/')

	else:
		form = SignupForm()

	context['form'] = form

	return render(request, 'account/auth/signup.html', context)


def signin(request):
	if request.user.is_authenticated:
		return redirect('/')
		
	context = {}
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			phone = form.cleaned_data['phone']
			password = form.cleaned_data['password']

			user = authenticate(phone=phone, password=password)

			if user is not None:
				if(not user.is_active):
					user.is_active = True
					user.save()
			
				login(request, user)
				return redirect('/account/')

	else:
		form = SigninForm()

	context['form'] = form

	return render(request, 'account/auth/signin.html', context)


@login_required(login_url=LOGIN_URL)
def signout(request):
	logout(request)
	return views.response(request,'account/auth/signout.html')
	

@login_required(login_url=LOGIN_URL)
def change_password(request):
	context = {}

	if request.method == 'POST':
		form = PasswordChangeForm(request.POST, user=request.user)
		if form.is_valid():
			new_password = form.cleaned_data['confirm_password']
			user = request.user
			user.set_password(new_password)
			user.save()

			logout(request)
			login(request, user)

			return redirect('/account/')


	form = PasswordChangeForm(user=request.user)
	context['form'] = form

	return render(request, 'account/auth/change_password.html', context)