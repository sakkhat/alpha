from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from generic.constants import LOGIN_URL
from generic.variables import get_api_token
from generic.views import invalid_request

from space.models import Product

@login_required(login_url=LOGIN_URL)
def trending(request):
	context = {}
	print(request.session.get('user_api_token'))
	token = get_api_token(request)
	context['token'] = token
	return render(request, 'home/filtering/trending.html', context)


@login_required(login_url=LOGIN_URL)
def search(request):
	context = {}
	query = None

	if request.method != 'GET':
		return invalid_request(request)

	query = request.GET.get('query', None)
	what = request.GET.get('what', 'product')

	if query is None:
		return redirect('/')

	token = get_api_token(request)
	context['token'] = token
	context['query'] = query
	context['what'] = what.lower()

	return render(request, 'home/filtering/search.html', context)
