from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from generic.views import invalid_request
from generic.variables import LOGIN_URL

from space.models import Product

@login_required(login_url=LOGIN_URL)
def trending(request):
	context = {}

	return render(request, 'home/filtering/trending.html', context)


@login_required(login_url=LOGIN_URL)
def recent(request):
	products = Product.objects.all().order_by('-time_date')[:12]
	context = {
		'products' : products
	}

	return render(request, 'space/product/list.html', context)
