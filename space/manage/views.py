from api.handler.tokenization import encode as token_encode

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from generic.media import Image
from generic.constants import LOGIN_URL, SPACE_BANNER_PATH
from generic.views import invalid_request, json_response

from home.models import (Favorite,PinnedProduct, Notification,
	_NOTIFICATION_LABEL_DIC as NDIC )

from space.manage.forms import SpaceCreateForm,SpaceUpdateForm
from space.models import Space,Product,Status,Banner


@login_required(login_url=LOGIN_URL)
def route(request):
	return redirect('/space/all/')


@login_required(login_url=LOGIN_URL)
def manager(request):

	space_list = Space.objects.all()
	token = token_encode({'user_id' : request.user.id })
	context = {
		'space_list' : space_list,
		'token' : token
	}

	return render(request, 'space/manage/list.html', context)


@login_required(login_url=LOGIN_URL)
def index(request, name):

	context = {}
	try:
		space = Space.objects.get(name__iexact=name)
		status = Status.objects.get(space=space)

		banners = Banner.objects.filter(space=space)

		token = token_encode({
			'user_id' : request.user.id, 
			'space_id' : space.id,	
		})

		context['space'] = space
		context['banners'] = banners
		context['status'] = status
		context['total_react'] = (status.total_good_react+status.total_bad_react+status.total_fake_react)
		context['has_favorite'] = False
		context['token'] = token

		try:
			favorite = Favorite.objects.get(user_id=request.user.id, space_id=space.id)
			context['has_favorite'] = True
		except ObjectDoesNotExist as e:
			pass

		return render(request, 'space/manage/index.html', context)
	except ObjectDoesNotExist as e:
		return invalid_request(request, context)

	
@login_required(login_url=LOGIN_URL)
def create(request):
	if request.user.has_space:
		return invalid_request(request)
		
	context = {}

	if request.method == 'POST':
		if request.user.has_space:
			return invalid_request(request)
		form = SpaceCreateForm(request.POST, request=request)
		if form.is_valid():
			space = form.save()
			status = Status.objects.create(space=space)
			request.user.has_space=True
			_notify(user)
			request.user.save()

			return redirect('/space/'+space.name+'/')

	else:
		form = SpaceCreateForm(request=request)

	context['form'] = form

	return render(request, 'space/manage/create.html', context)


def _notify(user):
	Notification.objects.create(
		user=user,
		label=NDIC['offer'],
		title='Congrates!',
		message='You got 1 free product post for your space',
		action='/account/'
		)
	user.has_notification = True


@login_required(login_url=LOGIN_URL)
def update(request, name):
	context = {}
	try:
		space = Space.objects.get(name__iexact=name)
		if request.user == space.owner:

			if request.method == 'POST':
				form = SpaceUpdateForm(request.POST, space=space)
				if form.is_valid():
					description = form.cleaned_data['description']
					space.description = description
					space.save()

					return redirect('/space/'+space.name+'/')

			tab = request.GET.get('tab', 'information')
			tab = tab.lower()

			if tab == 'banner':
				banners = Banner.objects.filter(space_id=space.id)
				context['banners'] = banners
			else:
				tab = 'information'
				form = SpaceUpdateForm(space=space)
				context['form'] = form

			token = token_encode({'user_id' : request.user.id })
			context['tab'] = tab
			context['space'] = space
			context['token'] = token

			return render(request, 'space/manage/update.html', context)

	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request, context)
