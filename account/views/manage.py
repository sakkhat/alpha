from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render,redirect

from account.models import Account

from generic.variables import LOGIN_URL

from space.models import ProductReact


@login_required(login_url=LOGIN_URL)
def profile(request):
	context = {}
	return render(request, 'account/manage/profile.html', context)


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


@login_required(login_url=LOGIN_URL)
def activity_manager(request):
	what = request.GET.get('what', None)
	if what is not None:
		what = what.lower()
		if what == 'product-react-list':
			return activity_product_react_list(request)
		elif what == 'favorite-space-list':
			return activity_favorite_space_list(request)
		elif what == 'pinned-product-list':
			return activity_pinned_product_list(request)

	return redirect('/account/')


@login_required(login_url=LOGIN_URL)
def activity_product_react_list(request):
	return render(request, 'account/manage/product_react_list.html', {})


@login_required(login_url=LOGIN_URL)
def activity_favorite_space_list(request):
	return render(request, 'account/manage/favorite_space_list.html', {})


@login_required(login_url=LOGIN_URL)
def activity_pinned_product_list(request):
	return render(request, 'account/manage/pinned_product_list.html', {})