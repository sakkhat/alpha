from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from generic.variables import LOGIN_URL
from generic.views import json_response

from home.models import Favorite, PinnedProduct,Notification
from space.models import Product,Category,Status, _PRODDUCT_CATEGORY_KEY_DIC


def index(request):
	context = {}

	categories = Category.objects.all()
	context['categories'] = categories

	mens_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['men-fashion'])
	womens_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['women-fashion'])
	gadets_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['gadget'])

	recent_products = Product.objects.order_by('-time_date')[:8]
	most_goods_products = Product.objects.order_by('-react_good')[:4]
	top_mens_products = Product.objects.filter(category_id=mens_category.id).order_by('-react_good')[:4]
	top_womens_products = Product.objects.filter(category_id=womens_category.id).order_by('-react_good')[:4]
	top_gadgets_products = Product.objects.filter(category_id=gadets_category.id).order_by('-react_good')[:4]

	if request.user.is_authenticated:
		favorite = Favorite.objects.filter(user=request.user).order_by('-unix_time')[:5]
		context['favorite'] = favorite
		

	context['recent_products'] = recent_products
	context['most_goods_products'] = most_goods_products
	context['top_mens_products'] = top_mens_products
	context['top_womens_products'] = top_womens_products
	context['top_gadgets_products'] = top_gadgets_products


	return render(request, 'home/manage/index.html', context)


def manager(request):
	if request.method == 'GET' and request.user.is_authenticated:
		what = request.GET.get('filter',None)
		if what is not None:
			what = what.lower()
			if what == 'pinned-products':
				return render(request, 'home/filtering/pinned.html', {})

	return index(request)


@login_required(login_url=LOGIN_URL)
def notification(request):
	context = {}
	return render(request, 'home/manage/notification.html', context)


@login_required(login_url=LOGIN_URL)
def notification_status_changle(request, uid):
	try:
		notification = Notification.objects.get(uid=uid)

		if notification.user.phone == request.user.phone:
			seen = request.GET.get('seen', None)

			if seen is not None:
				seen = seen.lower()
				if seen == 'false':
					notification.seen = False
					return _update_user_notification_status(request, notification)

				elif seen == 'true':
					notification.seen = True
					return _update_user_notification_status(request, notification)
					
	except ObjectDoesNotExist as e:
		pass

	return json_response(request, {}, 'invalid')


@login_required(login_url=LOGIN_URL)
def _update_user_notification_status(request, notification):
	notification.save()

	user_unseen_notification = Notification.objects.filter(user=request.user, seen=False)
	if user_unseen_notification.exists():
		request.user.has_notification = True
		request.user.save()

	else:
		request.user.has_notification = False
		request.user.save()

	return json_response(request, {}, 'done')
