from api.handler.tokenization import decode as token_decode

from account.forms import SignupForm,SigninForm,PasswordChangeForm
from account.models import Account, UserManager

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from generic import views
from generic.mail import verify_email
from generic.variables import LOGIN_URL


from home.models import Notification, _NOTIFICATION_LABEL_DIC as NDIC


def signup(request):

	if request.user.is_authenticated:
		return redirect('/account/')

	context = {}
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()

			verify_email(request, user)

			return render(request, 'account/auth/verify.html', {})

	else:
		form = SignupForm()

	context['form'] = form

	return render(request, 'account/auth/signup.html', context)



def verify(request, token):

	data = token_decode(token)
	if data is None:
		return views.invalid_request(request)

	user_id = data['user_id']
	email = data['email']

	user = Account.objects.get(id=user_id)
	if user.is_active:
		return redirect('/account/')
	if email == user.email:
		user.is_active = True
		_notify(user)
		user.save()
		return render(request, 'account/auth/confirm.html', {})

	return views.invalid_request(request)


def _notify(user):
	Notification.objects.create(
		user=user,
		label=NDIC['general'],
		title='Welcome to sakkhat',
		action='/account/',
		message='Hello '+user.name+
		', explore your favorite space, pinned products and reacts activities.'
		)
	user.has_notification = True

def signin(request):
	if request.user.is_authenticated:
		return redirect('/account/')
		
	context = {}
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			phone = form.cleaned_data['phone']
			password = form.cleaned_data['password']

			user = authenticate(phone=phone, password=password)

			if user is not None:
				login(request, user)

				goto = request.GET.get('next', None)
				if goto:
					return redirect(goto)
				return redirect('/account/')


			else:
				messages.error(request, 'Incorrect information')

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

	return render(request, 'account/password/change.html', context)