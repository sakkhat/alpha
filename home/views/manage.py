from api.handler.tokenization import encode as token_encode
from api.handler.tokenization import decode as token_decode

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from generic.variables import LOGIN_URL
from generic.views import invalid_request

from home.models import Favorite, PinnedProduct,Notification
from space.models import Product,Category,Status, _PRODDUCT_CATEGORY_KEY_DIC

from uuid import uuid1


def index(request):
	context = {}

	categories = Category.objects.all()
	context['categories'] = categories

	mens_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['men-fashion'])
	womens_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['women-fashion'])
	gadets_category = categories.get(name=_PRODDUCT_CATEGORY_KEY_DIC['gadget'])

	recent_products = Product.objects.filter(in_stock=True).values(
		'uid', 'title', 'price', 'react_good', 'react_bad', 'react_fake', 'logo_url', 'space__name').order_by(
		'-time_date')[:8]

	most_goods_products = Product.objects.values(
		'uid', 'title', 'price', 'react_good', 'react_bad', 'react_fake', 'logo_url', 'space__name').order_by(
		'-react_good')[:4]


	top_mens_products = Product.objects.filter(category_id=mens_category.id).values(
		'uid', 'title', 'price', 'react_good', 'react_bad', 'react_fake', 'logo_url', 'space__name').order_by(
		'-react_good')[:4]


	top_womens_products = Product.objects.filter(category_id=womens_category.id).values(
		'uid', 'title', 'price', 'react_good', 'react_bad', 'react_fake', 'logo_url', 'space__name').order_by(
		'-react_good')[:4]


	top_gadgets_products = Product.objects.filter(category_id=gadets_category.id).values(
		'uid', 'title', 'price', 'react_good', 'react_bad', 'react_fake', 'logo_url', 'space__name').order_by(
		'-react_good')[:4]


	top_spaces = Status.objects.values('space__name', 'rating', 'total_post').order_by('-rating')[:8]

	if request.user.is_authenticated:
		favorite = Favorite.objects.filter(user=request.user).order_by('-time_date')[:5]
		token = token_encode({'user_id' : request.user.id })

		context['favorite'] = favorite
		context['token'] = token

	else:
		token = token_encode({'guest_uid' : uuid1().hex })
		context['token'] = token


	context['recent_products'] = recent_products
	context['most_goods_products'] = most_goods_products
	context['top_mens_products'] = top_mens_products
	context['top_womens_products'] = top_womens_products
	context['top_gadgets_products'] = top_gadgets_products
	context['top_spaces'] = top_spaces

	# response = render -> set new guest cockie
	
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
	if request.method == 'GET':
		query = request.GET.get('query', None)
		if query:
			query = query.lower()
			context['query'] = query
		else:
			context['query'] = 'all'

	token = token_encode({'user_id' : request.user.id })
	context['token'] = token
	return render(request, 'home/manage/notification.html', context)




@login_required(login_url=LOGIN_URL)
def notification_route(request, uid):
	if request.method != 'GET':
		return invalid_request(request)

	token = request.GET.get('token', None)
	action = request.GET.get('action', None)

	if token is None or action is None:
		return invalid_request(request)

	data = token_decode(token)
	if data is None:
		return invalid_request(request)

	user_id = data['user_id']
	if request.user.id != user_id:
		return invalid_request(request)

	item = Notification.objects.filter(uid=uid, user_id=user_id).first()
	if item is None:
		return invalid_request(request)

	item.seen = True
	item.save()

	remain_notification = Notification.objects.filter(seen=False, user_id=user_id).count()
	if remain_notification == 0:
		request.user.has_notification = False
		request.user.save()

	return redirect(action)
