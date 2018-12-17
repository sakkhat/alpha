from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as redirect
from django.http import HttpResponse
from space.models import Account
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request):
	return render(request, 'home.html', {})

def about(request):
	return render(request, 'about.html', {})

def auth(request):
	return render(request, 'auth.html', {})

def dashboard(request):
	return render(request, 'dashboard.html', {})

def login(request):
	remail = request.POST.get('email')
	password = request.POST.get('password')
	try:
		uemail = Account.objects.get(email = remail)
		if uemail.password == password:
			return redirect('/dashboard')
		else:
			return redirect('/auth')
	except ObjectDoesNotExist as e:
		return redirect('/auth')
	

def signup(request):
	dname = request.POST.get('dname')
	sname = request.POST.get('sname')
	email = request.POST.get('email')
	phone = request.POST.get('phone')
	password = request.POST.get('password')
	re_pass = request.POST.get('re-pass')

	if password != re_pass:
		return redirect('/auth')
	a = Account()
	a.dname = dname
	a.sname = sname
	a.email = email
	a.phone = phone
	a.password = password

	a.save()

	return redirect('/dashboard')

	

