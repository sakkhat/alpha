from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render,redirect

from account.models import Account

from generic.variables import LOGIN_URL


#@login_required(login_url=LOGIN_URL)
def info(request):
	context = {}
	return render(request, 'account/manage/info.html', context)


@login_required(login_url=LOGIN_URL)
def update(request):
	pass


@login_required(login_url=LOGIN_URL)
def delete(request):
	user = request.user
	logout(request)
	user.delete()

	redirect('/')


@login_required(login_url=LOGIN_URL)
def decactive(request):
	user = request.user
	user.is_active = False
	user.save()
	logout(request)
	return redirect('/')