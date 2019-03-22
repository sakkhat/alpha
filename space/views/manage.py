from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from generic.media import Image
from generic.variables import LOGIN_URL, now_str, random, SPACE_BANNER_PATH
from generic.views import invalid_request, json_response

from home.models import Favorite,PinnedProduct,TrendingSpaceStatus

from space.forms import SpaceCreateForm,SpaceUpdateForm
from space.models import Space,Product,Status,Banner



def index(request, name):

	context = {}
	try:
		space = Space.objects.get(name__iexact=name)
		status = Status.objects.get(space=space)

		if request.user.is_authenticated and request.method == 'GET':
			favorite = request.GET.get('favorite', None)
			if favorite is not None:
				favorite = favorite.lower()
				if favorite == 'add':
					handle_favorite(request, space, True)
				elif favorite == 'remove':
					handle_favorite(request, space, False)


		banners = Banner.objects.filter(space=space)
		products = Product.objects.filter(space = space)

		context['space'] = space
		context['banners'] = banners
		context['status'] = status
		context['total_react'] = (status.total_good_react+status.total_bad_react+status.total_fake_react)
		context['products'] = products
		context['has_favorite'] = False

		in_trending = TrendingSpaceStatus.objects.filter(status=status)
		if in_trending is not None:
			context['in_trending'] = True
		else:
			context['in_trending'] = False

		if request.user.is_authenticated:
			try:
				favorite = Favorite.objects.get(user=request.user, space=space)
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
		form = SpaceCreateForm(request.POST, request=request)
		if form.is_valid():
			space = form.save()
			status = Status.objects.create(space=space)
			request.user.has_space=True
			request.user.save()

			return redirect('/space/'+space.name+'/')

	else:
		form = SpaceCreateForm(request=request)

	context['form'] = form

	return render(request, 'space/manage/create.html', context)


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

			banners = Banner.objects.filter(space=space)
			context['space'] = space
			context['banners'] = banners
			form = SpaceUpdateForm(space=space)
			context['form'] = form

			return render(request, 'space/manage/update.html', context)

	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request, context)



@login_required(login_url=LOGIN_URL)
def update_space_banner(request, name , uid):
	if request.method == 'POST':
		try:
			space = Space.objects.get(name__iexact=name)
			if request.user == space.owner:
				try:
					banner = Banner.objects.get(uid=uid)
					if banner.space == space:
						file = request.FILES.get('banner', None)
						if file is not None:
							img_src = Image.load(file_stream=file)
							img_path = Image.save(SPACE_BANNER_PATH, img_src)

							Image.delete(banner.location)
							banner.delete()

							new_banner = Banner(space=space, location=img_path)
							new_banner.uid = random()
							new_banner.save()

							return redirect('/space/'+space.name+'/update/')


				except ObjectDoesNotExist as e:
					pass
		except ObjectDoesNotExist as e:
			pass

	return invalid_request(request)
