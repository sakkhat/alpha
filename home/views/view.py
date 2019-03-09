from django.shortcuts import render

from space.models import Product

def index(request):
	# filter limited order
	products = Product.objects.all()
	trending_products = products
	recent_products = products
	pinned_products = products
	related_products = products

	context = {
		'trending_products' : trending_products,
		'recent_products' : recent_products,
		'pinned_products' : pinned_products,
		'related_products' : related_products}
	return render(request, 'home/index.html', context)