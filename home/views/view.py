from django.shortcuts import render

from generic.query import pinned_product_objects
from home.models import Favorite, PinnedProduct
from space.models import Product

def index(request):
	# filter limited order
	context = {}

	products = Product.objects.all()
	trending_products = products
	recent_products = Product.objects.all().order_by('-uid')[:10]
	pinned_products = products
	related_products = products

	if request.user.is_authenticated:
		favorite = Favorite.objects.filter(user=request.user).order_by('-uid')[:7]
		context['favorite'] = favorite
		
		pinned_products = pinned_product_objects(request.user, 10)
		context['pinned_products'] = pinned_products

	context['trending_products'] = trending_products
	context['recent_products'] = recent_products
	context['related_products'] = related_products

	return render(request, 'home/index.html', context)


def manager(request):
	if request.method == 'GET':
		what = request.GET.get('filter',None)
		if what is not None:
			what = what.lower()
			if what == 'pinned-products':
				return render(request, 'home/filter_products.html', {})

	return index(request)