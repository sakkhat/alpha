from django.shortcuts import render
from generic.views import invalid_request
from home.models import TrendingSpaceStatus
from space.models import Product

def trending(request):
	trending_status = TrendingSpaceStatus.objects.all()
	context = {
		'trending_status' : trending_status
	}

	return render(request, 'home/filtering/trending.html', context)


def recent(request):
	products = Product.objects.all().order_by('-time_date')[:12]
	context = {
		'products' : products
	}

	return render(request, 'space/product/list.html', context)
