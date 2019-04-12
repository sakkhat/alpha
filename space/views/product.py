from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from generic.media import Image
from generic.variables import (LOGIN_URL, now_str, PRODUCTS_FILE_PATH, ACTIVITY_POINT,
	MIN_RATE_FOR_SPACE_TRENDING)
from generic.views import json_response, invalid_request

from home.models import PinnedProduct

from space.forms import ProductPostForm,ProductUpdateForm
from space.models import Product, ProductMedia, ProductReact,Status,Category


def route(request):
	return redirect('/space/product/all/')


def view(request, uid):
	context = {}
	try:
		product = Product.objects.get(uid = uid)
		media = ProductMedia.objects.filter(product_id=product.uid)
		related_products = Product.objects.filter(category_id=product.category_id).order_by('-time_date')[:10]

		if request.user.is_authenticated:
	
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


def manager(request):
	context = {}
	has_attribute = False

	if request.method == 'GET':
		category = request.GET.get('category', None)
		pinned_by = request.GET.get('pinned_by', None)
		query = request.GET.get('query', None)


		if category is not None:
			has_attribute = True
			context['category'] = category
	

		elif pinned_by is not None:
			if request.user.is_authenticated:
				has_attribute = True
				context['pinned_by'] = True

		elif query is not None:
			has_attribute = True
			context['query'] = query
		

	context['has_attribute'] = has_attribute
	if has_attribute:
		return render(request, 'space/product/list.html', context)
	
	products = Product.objects.all().order_by('-time_date')
	context['products'] = products

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
					
					product.title = form.cleaned_data['title']
					product.description = form.cleaned_data['description']
					product.price = form.cleaned_data['price']
					product.category = form.cleaned_data['category']
					product.in_stock = form.cleaned_data['in_stock']
					product.phone_request = form.cleaned_data['phone_request']
					product.email_request = form.cleaned_data['email_request']

					product.save()

					return redirect('/space/product/'+uid+'/')


			form = ProductUpdateForm(product=product)
			media = ProductMedia.objects.filter(product=product)

			context['form'] = form
			context['media'] = media
			context['product'] = product

			return render(request, 'space/product/update.html', context) 


	except ObjectDoesNotExist as e:
		pass

	return invalid_request(request)


@login_required(login_url=LOGIN_URL)
def delete(request, uid):
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

			return json_response(request, json_data='product deleted')

	except ObjectDoesNotExist as e:
		pass
	return json_response(request, json_data='something went wrong')





@login_required(login_url=LOGIN_URL)
def update_product_media(request, uid, media_id):
	if request.method == 'POST':
		try:
			product = Product.objects.get(uid=uid)
			media = ProductMedia.objects.get(uid=media_id)

			if media.product == product:
				file = request.FILES.get('image', None)

				if file is not None:
					img_src = Image.load(file_stream=file)

					if img_src is not None:
						img_path = Image.save(PRODUCTS_FILE_PATH, img_src)

						Image.delete(media.location)
						media.delete()

						new_media = ProductMedia(location = img_path, product=product)
						new_media.uid = random()
						new_media.save()

						product.logo_url = new_media.location
						product.save()


		except ObjectDoesNotExist as e:
			pass


	return redirect('/space/product/'+uid+'/update/')

