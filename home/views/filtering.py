from django.shortcuts import render
from generic.views import invalid_request

from space.models import Product

def trending(request):
	context = {}

	return render(request, 'home/filtering/trending.html', context)


def recent(request):
	products = Product.objects.all().order_by('-time_date')[:12]
	context = {
		'products' : products
	}

	return render(request, 'space/product/list.html', context)
