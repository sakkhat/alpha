from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.variables import LOGIN_URL, now_str
from generic.views import json_response, invalid_request

from home.models import PinnedProduct

from space.forms import ProductPostForm
from space.models import Product, ProductMedia, ProductReact


def view(request, uid):
	context = {}
	try:
		product = Product.objects.get(uid = uid)
		media = ProductMedia.objects.filter(product=product)
		related_products = Product.objects.filter(category=product.category).order_by('-uid')[:10]

		if request.user.is_authenticated:
	
			react_obj = ProductReact.objects.filter(product=product, user=request.user).first()
			if react_obj is not None:
				context['has_react'] = True
				context['current_react'] = react_obj.react
			else:
				context['has_react'] = False


			pin = PinnedProduct.objects.filter(product=product, user=request.user).first()
			if pin is not None:
				context['has_pin'] = True
			else:
				context['has_pin'] = False


		context['product'] = product
		context['media'] = media
		context['related_products'] = related_products

		return render(request, 'space/product/single.html', context)
		
	except ObjectDoesNotExist as e:
		return invalid_request(request=request)



@login_required(login_url=LOGIN_URL)
def handle_pin(request, uid, add):
	try:
		product = Product.objects.get(uid = uid)

		if add:
			try:
				pin = PinnedProduct.objects.get(user=request.user, product=product)
				return json_response(request, {}, 'invalid')
			except ObjectDoesNotExist as e:
				pin = PinnedProduct(user=request.user, product=product)
				pin.uid = now_str(3)
				pin.save()
				return json_response(request, {}, 'done')
		else:
			try:
				pin = PinnedProduct.objects.get(user = request.user, product=product)
				pin.delete()
				return json_response(request, {}, 'done')
			except ObjectDoesNotExist as e:
				return json_response(request, {}, 'invalid')

	except ObjectDoesNotExist as e:
		return json_response(request, {}, 'invalid')



@login_required(login_url=LOGIN_URL)
def handle_react(request, uid, what):
	
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
			react_obj = ProductReact(user=user, product=product, react=at)
			react_obj.uid = now_str(mul=3)
			react_obj.save()

		else:
			if has == 'F' or has == 'B' or has == 'G':
				react_obj.delete()

				new_react_obj = ProductReact(user=user, product=product, react=at)
				new_react_obj.uid = now_str(3)
				new_react_obj.save()


		return json_response(request=request, json_data='done')
	except ObjectDoesNotExist as e:
		return json_response(request=request, json_data='invalid request')



def manager(request, uid):

	if request.user.is_authenticated and request.method=='GET':
		pin = request.GET.get('pin', None)
		if pin is not None:
			pin = pin.lower()
			if pin == 'add':
				return handle_pin(request, uid, True)
			elif pin == 'remove':
				return handle_pin(request, uid, False)


		react = request.GET.get('react', None)
		if react is not None:
			if len(react) == 2:
				return handle_react(request, uid, react)

	
	return view(request, uid)
	


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

