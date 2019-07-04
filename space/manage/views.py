from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from generic.media import Image
from generic.constants import LOGIN_URL, SPACE_BANNER_PATH
from generic.views import invalid_request, json_response
from generic.crypto import get_api_token

from home.models import (Favorite,PinnedProduct, Notification,
	_NOTIFICATION_LABEL_DIC as NDIC )

from space.manage.forms import SpaceCreateForm,SpaceUpdateForm
from space.models import Space,Product,Status,Banner



@login_required(login_url=LOGIN_URL)
def index(request, space_name):
	try:
		space = Space.objects.get(name__iexact=space_name)
		status = Status.objects.get(space_id=space.id)

		banners = Banner.objects.filter(space_id=space.id)
		token = get_api_token(request)
		
		context = {}
		context['space'] = space
		context['banners'] = banners
		context['status'] = status
		context['has_favorite'] = False
		context['token'] = token
		try:
			favorite = Favorite.objects.get(user_id=request.user.id, space_id=space.id)
			context['has_favorite'] = True
		except ObjectDoesNotExist as e:
			pass

		return render(request, 'space/manage/index.html', context)
	except ObjectDoesNotExist as e:
		return invalid_request(request)


@login_required(login_url=LOGIN_URL)
def create(request):
	print('i am here')
	if request.user.has_space:
		return invalid_request(request)
	context = {}

	if request.method == 'POST':
		if request.user.has_space:
			return invalid_request(request)
		form = SpaceCreateForm(request.POST, request.FILES, request=request)
		if form.is_valid():
			space = form.save()
			status = Status.objects.create(space=space)
			request.user.has_space=True
			request.user.save()
			return redirect('/'+space.name+'/')

		else:
			print(form.errors)
	else:
		form = SpaceCreateForm(request=request)
	context['form'] = form
	return render(request, 'space/manage/create.html', context)


@login_required(login_url=LOGIN_URL)
def update(request, space_name):
	context = {}
	try:
		space = Space.objects.get(name__iexact=space_name)
		if request.user == space.owner:
			tab = request.GET.get('tab', 'information')
			tab = tab.lower()

			if tab == 'banner':
				banners = Banner.objects.filter(space_id=space.id)
				context['banners'] = banners
				token = get_api_token(request)
				context['token'] = token
			elif tab == 'logo':
				token = get_api_token(request)
				context['token'] = token
			else:
				tab = 'information'
				if request.method == 'POST':
					form = SpaceUpdateForm(request.POST, space=space)
					if form.is_valid():
						space = form.save()
						return redirect('/'+space.name+'/')
				else:
					form = SpaceUpdateForm(space=space)
				context['form'] = form

			context['tab'] = tab
			context['space'] = space
			return render(request, 'space/manage/update.html', context)

	except ObjectDoesNotExist as e:
		pass
	return invalid_request(request, context)
