from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.constants import (LOGIN_URL, PRODUCTS_FILE_PATH, ACTIVITY_POINT,
	MIN_RATE_FOR_SPACE_TRENDING)
from generic.forms import PasswordConfirmForm
from generic.media import Image
from generic.views import json_response, invalid_request, password_confirmation
from generic.variables import get_api_token

from home.models import PinnedProduct

from space.product.forms import ProductPostForm,ProductUpdateForm
from space.models import Product, ProductMedia, ProductReact,Status,Category


@login_required(login_url=LOGIN_URL)
def route(request):
	return redirect('/space/product/all/')


@login_required(login_url=LOGIN_URL)
def view(request, uid):
	context = {}
	try:
		product = Product.objects.get(uid = uid)
		media = ProductMedia.objects.filter(product_id=product.uid)
		related_products = Product.objects.filter(category_id=product.category_id).values(
			'uid', 'title','price', 'space__name', 'react_good', 'react_bad', 'react_fake',
			'logo_url').order_by('-time_date')[:10]


		react_obj = ProductReact.objects.filter(product_id=product.uid, user_id=request.user.id).first()
		if react_obj is not None:
			context['has_react'] = True
			context['current_react'] = react_obj.react
		else:
			context['has_react'] = False
			context['current_react'] = 'N'

		if request.user.id == product.space.owner_id:
			context['is_owner'] = True
		else:
			context['is_owner'] = False


		pin = PinnedProduct.objects.filter(product_id=product.uid, user_id=request.user.id).first()
		if pin is not None:
			context['has_pin'] = True
		else:
			context['has_pin'] = False

		token = get_api_token(request)
		context['token'] = token


		context['product'] = product
		context['media'] = media
		
		context['related_products'] = related_products

		current_site = get_current_site(request)
		context['current_site'] = current_site

		return render(request, 'space/product/single.html', context)
		
	except ObjectDoesNotExist as e:
		return invalid_request(request=request)


@login_required(login_url=LOGIN_URL)
def manager(request):
	context = {}
	has_attribute = False

	if request.method == 'GET':
		category = request.GET.get('category', None)
		pinned_by = request.GET.get('pinned_by', None)
		query = request.GET.get('query', None)

		user = request.user

		token = get_api_token(request)
		context['token'] = token


		if category is not None:
			has_attribute = True
			context['category'] = category

		elif pinned_by is not None:
			has_attribute = True
			context['pinned_by'] = True		
			context['user_name'] = user.name

	context['has_attribute'] = has_attribute

	return render(request, 'space/product/list.html', context)



@login_required(login_url=LOGIN_URL)
def create(request):
	context = {}
	if request.method == 'POST':
		form = ProductPostForm(request.POST, request.FILES ,request=request)
		if form.is_valid():
			form.load_images()
			post = form.save()

			status = Status.objects.get(space=post.space)
			status.total_post += 1
			status.save()

			category = Category.objects.get(id=post.category_id)
			category.total_products += 1
			category.save()

			return redirect('/space/product/'+str(post.uid)+'/')

	else:
		form = ProductPostForm(request=request)

	context['form'] = form

	return render(request, 'space/product/create.html',context)


@login_required(login_url=LOGIN_URL)
def update(request, uid):
	try:
		product = Product.objects.get(uid=uid)
		if product.space.owner == request.user:
			context = {}

			if request.method == 'POST':
				form = ProductUpdateForm(request.POST, product=product)
				if form.is_valid():
					product = form.save()
					return redirect('/space/product/'+uid+'/')

			tab = request.GET.get('tab', 'details')
			tab = tab.lower()
			if tab == 'images':
				media = ProductMedia.objects.filter(product=product)
				context['media'] = media
			else:
				tab = 'details'
				form = ProductUpdateForm(product=product)
				context['form'] = form

			token = get_api_token(request)
			context['token'] = token
			context['tab'] = tab
			context['product'] = product

			return render(request, 'space/product/update.html', context) 

	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request)


@login_required(login_url=LOGIN_URL)
def delete(request, uid):
	context = {}
	if request.method == 'POST':
		form = PasswordConfirmForm(request.POST, user=request.user)
		if form.is_valid():
			return _delete_data(request, uid)

	else:
		form = PasswordConfirmForm(user=request.user)

	context['form'] = form

	print(context)
	return password_confirmation(request, context)



def _delete_data(request, uid):
	try:
		product = Product.objects.get(uid=uid)
		if product.space.owner == request.user:
			space_name = product.space.name
			
			# count of total
			total_pin = PinnedProduct.objects.filter(product_id=product.uid).count()
			PinnedProduct.objects.filter(product_id=product.uid).delete()
			ProductReact.objects.filter(product_id=product.uid).delete()

			status = Status.objects.get(space_id=product.space_id)
			status.total_good_react -= product.react_good
			status.total_bad_react -=product.react_bad
			status.total_fake_react -=product.react_fake
			status.total_post -= 1
			status.total_pinned -= total_pin

			remove_point = ((ACTIVITY_POINT['GOOD']*product.react_good)+(ACTIVITY_POINT['PIN']*total_pin)+
				(ACTIVITY_POINT['BAD']*product.react_bad)+(ACTIVITY_POINT['FAKE']*product.react_fake))

			status.rating -= remove_point
			status.save()


			media = ProductMedia.objects.filter(product_id=product.uid)
			# delete image sources
			for item in media:
				Image.delete(item.location)
			# delete database objects
			media.delete()

			category = Category.objects.get(id=product.category_id)
			category.total_products -= 1
			category.save()

			product.delete()

			return redirect('/space/'+space_name+'/')
	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request)