from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from home.models import Favorite

from space.forms import SpaceCreateForm
from space.models import Space,Product

from generic.variables import LOGIN_URL, now_str
from generic.views import invalid_request, json_response

from space.api.views import ProductListView
def index(request, name):

	context = {}
	try:
		space = Space.objects.get(name__iexact=name)

		if request.user.is_authenticated and request.method == 'GET':
			favorite = request.GET.get('favorite', None)
			if favorite is not None:
				favorite = favorite.lower()
				if favorite == 'add':
					handle_favorite(request, space, True)
				elif favorite == 'remove':
					handle_favorite(request, space, False)

		products = Product.objects.filter(space = space)
		context['space'] = space
		context['products'] = products
		context['has_favorite'] = False

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
	context = {}

	if request.method == 'POST':
		form = SpaceCreateForm(request.POST, request=request)
		if form.is_valid():
			form.save()
			name = form.cleaned_data['name']
			return redirect('/space/'+name+'/')

	else:
		form = SpaceCreateForm(request=request)

	context['form'] = form

	return render(request, 'space/manage/create.html', context)




def handle_favorite(request, space, add):
	try:
		row = Favorite.objects.get(user=request.user, space = space)
	except ObjectDoesNotExist as e:
		row = None

	if add:
		if row is None:
			row = Favorite(user=request.user, space=space)
			row.uid = now_str(3)
			row.save()
		
	else:
		if row is not None:
			row.delete()
			
	return json_response(request, {}, 'done')