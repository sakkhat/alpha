from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.variables import LOGIN_URL, now_md5_hashed
from generic.views import json_response, invalid_request

from space.forms import ProductPostForm
from space.models import Product, ProductMedia, ProductReact

def single(request, uid):

	context = {}
	try:
		product = Product.objects.get(uid = uid)
		media = ProductMedia.objects.filter(product=product)
		related_products = Product.objects.all()

		if request.user.is_authenticated:
			try:
				react_obj = ProductReact.objects.get(product=product, user=request.user)
				context['has_react'] = True
				context['current_react'] = react_obj.react

			except ObjectDoesNotExist as e:
				context['has_react'] = False


		context['product'] = product
		context['media'] = media
		context['related_products'] = related_products

		return render(request, 'space/product/single.html', context)
		
	except ObjectDoesNotExist as e:
		return invalid_request(request=request)
	


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
def react(request, uid):
	
	what = request.GET.get('what', None)


	if what is None:
		return json_response(request=request, json_data='invalid request')

	if len(what) != 2:
		return json_response(request=request, json_data='invalid request')

	what = what.upper()
	at = what[0]
	has = what[1]
	if at == has:
		return json_response(request=request, json_data='invalid request')

	try:
		product = Product.objects.get(uid=uid)
		user = request.user
		
		react_obj = None
		try:
			react_obj = ProductReact.objects.get(user = user, product=product)
		except ObjectDoesNotExist as e:
			react_obj = None
		

		if at == 'G':
			product.react_good = product.react_good + 1
			if has == 'F':
				product.react_fake = product.react_fake - 1
			elif has == 'B':
				product.react_bad = product.react_bad -1
			product.save()

		elif at == 'B':
			product.react_bad = product.react_bad + 1
			if has == 'G':
				product.react_good = product.react_good - 1
			elif has == 'F':
				product.react_fake = product.react_fake - 1
			product.save()

		elif at == 'F':
			product.react_fake = product.react_fake + 1
			if has == 'G':
				product.react_good = product.react_good - 1
			elif has == 'B':
				product.react_bad = product.react_bad - 1
			product.save()


		if react_obj is None:
			react_obj = ProductReact(product = product, user = user)
			react_obj.react = at
			react_obj.uid = now_md5_hashed(mul=5)
			react_obj.save()

		else:
			if has == 'F' or has == 'B' or has == 'G':
				react_obj.react = at
				react_obj.save()


		return json_response(request=request, json_data='done')
	except ObjectDoesNotExist as e:
		return json_response(request=request, json_data='invalid request')
	