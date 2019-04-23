from account.forms import ProfileUpdateForm
from account.models import Account

from api.handler.tokenization import encode as token_encode

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render,redirect

from generic.variables import LOGIN_URL

from space.models import ProductReact,Space,Status


@login_required(login_url=LOGIN_URL)
def profile(request):
	context = {}

	if request.user.has_space:
		space = Space.objects.get(owner=request.user)
		status = Status.objects.get(space=space)
		context['space'] = space
		context['status'] = status

	return render(request, 'account/manage/profile.html', context)


@login_required(login_url=LOGIN_URL)
def update(request):
	context = {}
	if request.method == 'POST':

		form = ProfileUpdateForm(request.POST, user=request.user)
		if form.is_valid():
			
			request.user.name = form.cleaned_data['name']
			request.user.email = form.cleaned_data['email']
			request.user.gender = form.cleaned_data['gender']
			request.user.save()

			return redirect('/account/')


	form = ProfileUpdateForm(user=request.user)

	context['form'] = form

	return render(request, 'account/manage/update.html', context)


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
	token = token_encode({'user_id' : request.user.id})
	context = {'token' : token}
	return render(request, 'account/manage/product_react_list.html', context)


@login_required(login_url=LOGIN_URL)
def activity_favorite_space_list(request):
	token = token_encode({'user_id' : request.user.id})
	context = {'token' : token}
	return render(request, 'account/manage/favorite_space_list.html', context)


@login_required(login_url=LOGIN_URL)
def activity_pinned_product_list(request):
	token = token_encode({'user_id' : request.user.id})
	context = {'token' : token}
	return render(request, 'account/manage/pinned_product_list.html', context)