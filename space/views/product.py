from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.variables import LOGIN_URL
from generic.views import json_response

from space.forms import ProductPostForm
from space.models import Product, ProductMedia

def single(request, uid):

	context = {}
	try:
		product = Product.objects.get(uid = uid)
		media = ProductMedia.objects.filter(product=product)
		context['product'] = product
		context['media'] = media

		print(media)

		#filter some related product
	except ObjectDoesNotExist as e:
		pass
	return render(request, 'space/product/single.html', context)


@login_required(login_url=LOGIN_URL)
def create(request):
	context = {}
	if request.method == 'POST':
		form = ProductPostForm(request.POST, request.FILES ,request=request)
		if form.is_valid():
			form.load_images()
			post = form.save()
			return redirect('/space/product/'+post.uid+'/')

	else:
		form = ProductPostForm(request=request)

	context['form'] = form

	return render(request, 'space/product/create.html',context)



@login_required(login_url=LOGIN_URL)
def react(request):
	what = request.GET.get('what', None)
	key = request.GET.get('key', None)
	if what is None or key is None:
		return json_response(request=request, json_data='invalid request')
	try:
		product = Product.objects.get(key=key)
		what = what.lower()
		if what == 'good':
			product.react_good = product.react_good+1
			what = None

		elif what == 'bad':
			product.react_bad = product.react_bad+1
			what = None

		elif what == 'fake':
			product.react_fake = product.react_fake+1
			what = None

		if what is None:
			product.save()
			return json_response(request=request, json_data='done')

	except ObjectDoesNotExist as e:
		pass
	return json_response(request=request, json_data='invalid request')
	