from api.handler.tokenization import encode as token_encode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from generic.views import invalid_request
from generic.variables import LOGIN_URL

from space.models import Product

@login_required(login_url=LOGIN_URL)
def trending(request):
	context = {}
	token = token_encode({'user_id' : request.user.id })
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

	token = token_encode({'user_id' : request.user.id })

	context['token'] = token
	context['query'] = query
	context['what'] = what.lower()

	return render(request, 'home/filtering/search.html', context)
