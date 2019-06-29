from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.constants import (LOGIN_URL, PRODUCTS_FILE_PATH, ACTIVITY_POINT,
	MIN_RATE_FOR_SPACE_TRENDING)
from generic.crypto import get_api_token, is_valid_uuid
from generic.forms import PasswordConfirmForm
from generic.media import Image
from generic.views import json_response, invalid_request, password_confirmation

from home.models import PinnedProduct

from space.product.forms import ProductPostForm,ProductUpdateForm
from space.models import Product, ProductMedia, ProductReact,Status,Category



@login_required(login_url=LOGIN_URL)
def view(request, space_name, product_uid):
	product_uid = is_valid_uuid(product_uid)
	if product_uid is None:
		return invalid_request(request)
	try:
		product = Product.objects.get(uid = product_uid, space__name__iexact=space_name)
		media = ProductMedia.objects.filter(product_id=product.uid)

		# related product
		related_products = Product.objects.filter(category_id=product.category_id).values(
			'uid', 'title','price', 'space__name', 'react_good', 'react_bad', 'react_fake',
			'logo_url').order_by('-time_date')[:10]

		context = {}

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
def create(request, space_name):
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

			return redirect('/'+space_name+'/product/'+str(post.uid)+'/')

	else:
		form = ProductPostForm(request=request)
	context = {}
	context['form'] = form

	return render(request, 'space/product/create.html',context)


@login_required(login_url=LOGIN_URL)
def update(request, space_name, product_uid):
	product_uid = is_valid_uuid(product_uid)
	if product_uid is None:
		return invalid_request(request)
	try:
		product = Product.objects.get(uid=product_uid, space__name__iexact=space_name)
		if product.space.owner == request.user:
			context = {}

			if request.method == 'POST':
				form = ProductUpdateForm(request.POST, product=product)
				if form.is_valid():
					product = form.save()
					return redirect('/'+space_name+'/product/'+str(product_uid)+'/')

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
			context['space_name'] = space_name

			return render(request, 'space/product/update.html', context) 

	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request)


@login_required(login_url=LOGIN_URL)
def delete(request, space_name, product_uid):
	product_uid = is_valid_uuid(product_uid)
	if product_uid is None:
		return invalid_request(request)

	context = {}
	if request.method == 'POST':
		form = PasswordConfirmForm(request.POST, user=request.user)
		if form.is_valid():
			return _delete_data(request, space_name, product_uid)

	else:
		form = PasswordConfirmForm(user=request.user)

	context['form'] = form

	print(context)
	return password_confirmation(request, context)


def _delete_data(request, space_name, product_uid):
	try:
		product = Product.objects.get(uid=product_uid, space__name__iexact=space_name)
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

			return redirect('/'+space_name+'/')
	except ObjectDoesNotExist as e:
		pass
	return invalid_request(request)