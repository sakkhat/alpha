from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from space.forms import SpaceCreateForm
from space.models import Space

from generic.variables import LOGIN_URL
from generic.views import invalid_request


def index(request, name):
	context = {}
	try:
		space = Space.objects.get(name=name)
		context['space'] = space
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

			return redirect('/space/')

	else:
		form = SpaceCreateForm(request=request)

	context['form'] = form

	return render(request, 'space/manage/create.html', context)